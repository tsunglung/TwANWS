"""Common ANWS AOAWS Data class used by both sensor and entity."""

import logging
import re
import time
from datetime import datetime, timedelta
from http import HTTPStatus
from aiohttp.hdrs import USER_AGENT
import requests
from bs4 import BeautifulSoup
from homeassistant.const import (
    LENGTH_KILOMETERS,
    LENGTH_METERS,
    TEMP_CELSIUS,
    SPEED_KILOMETERS_PER_HOUR
)
from .const import (
    BASE_URL,
    REQUEST_TIMEOUT
)

_LOGGER = logging.getLogger(__name__)


class Element():
    def __init__(self, field_code=None, value=None, units=None, text=None):

        self.field_code = field_code
        self.value = value
        self.units = units

        # For elements which can also have a text value
        self.text = text

    def __str__(self):
        return str(self.value) + ' ' + str(self.units)


class Observation:
    def __init__(self):
        self.name = None
        self.date = None
        self.weather = None
        self.temperature = None
        self.wind_speed = None
        self.wind_direction = None
        self.wind_gust = None
        self.visibility = None
        self.uv = None
        self.precipitation = None
        self.humidity = None
        self.pressure = None
        self.pressure_tendency = None
        self.dew_point = None

    def __iter__(self):
        for attr, value in self.__dict__.items():
            yield attr, value

    def elements(self):
        """Return a list of the Elements which are not None"""
        elements = [el[1] for el in self.__dict__.items() if isinstance(el[1], Element)]

        return elements


class AnwsAoawseData:
    """Get current AOAWS from ANWS.

    Use API calls have had to be wrapped with the standard hassio helper
    async_add_executor_job.
    """

    def __init__(self, hass, site_name, language):
        """Initialize the data object."""
        self._hass = hass
        self._site = site_name

        # Holds the current data from the ANWS AOAWS
        self.data = None
        self.site_name = None
        self.language = language
        self.now = None
        self.uri = BASE_URL.format(language)

    async def async_update_site(self):
        """Async wrapper for getting the update."""
        return await self._hass.async_add_executor_job(self._update_site)

    def get_observations_for_site(self, site, data):
        """ return observation """
        self._update_site()
        return self._convert_to_observation(site, data)

    def _convert_to_observation(self, site, data):
        """ converter  """
        for i in data:
            for j in i:
                if j == site:
                    metar = i[26].split(" ")
                    for k in range(len(i)):
                        i[k] = re.sub(
                            "<font color=\\#999999\\>|<font color=\\\\#999999\\\\>|</font>", "", i[k])

                    observation = Observation()
                    # date
                    timestamp = int(time.mktime((datetime.strptime(
                        i[10].strip(), "%Y-%m-%d %H:%M %Z") + timedelta(hours=8)).timetuple()))
                    observation.date = datetime.fromtimestamp(
                        timestamp).strftime('%Y-%m-%d %H:%M:%S')

                    # wether
                    value = ''.join(c for c in i[16] if c.isalpha() or c.isspace()).strip()
                    observation.weather = Element("W", value=value, text=i[15])

                    # temperature
                    value = int(''.join(c for c in i[19] if c.isdigit()))
                    #unit = ''.join(c for c in i[19] if not c.isdigit()).replace("&nbsp;", " ")
                    unit = TEMP_CELSIUS
                    observation.temperature = Element("T", value=value, units=unit.strip())

                    # wind speed
                    if 'Gust' in i[13]:
                        value = ''.join(c for c in i[13].lstrip().split("Gust")[0] if c.isdigit())
                        value = int(value) if len(value) >= 1 else 0
                    elif '陣風' in i[13]:
                        value = ''.join(c for c in i[13].lstrip().split("陣風")[0] if c.isdigit())
                        value = int(value) if len(value) >= 1 else 0
                    else:
                        value = int(''.join(c for c in i[13] if c.isdigit()))
                    #unit = ''.join(c for c in i[13] if not c.isdigit()).replace("&nbsp;", " ")
                    if "浬/時" in unit or "KT" in unit:
                        value = value * 1.85
                    unit = SPEED_KILOMETERS_PER_HOUR
                    observation.wind_speed = Element("W", value=value, units=unit.strip())

                    # wind direction
                    if ''.join(c for c in i[12] if c.isdigit()):
                        value = ''.join(c for c in i[12] if c.isdigit())
                        value = int(value) if len(value) >= 1 else 0
                    else:
                        value = i[12]
                    unit = ''.join(c for c in i[12] if not c.isdigit()).replace("&nbsp;", " ")
                    observation.wind_direction = Element("W", value=value, units=unit.strip())

                    # visibility
                    i[14] = i[14].replace("&nbsp;", " ")
                    unit = ''.join(c for c in i[14] if not c.isdigit()).replace("&nbsp;", " ")
                    if "公里" in unit or "KM" in unit.upper():
                        unit = LENGTH_KILOMETERS
                    if "公尺" in unit or "M" in unit.upper():
                        unit = LENGTH_METERS
                    if "Over" in unit and " KM" in unit:
                        unit = LENGTH_KILOMETERS
                    if " M" in i[14] or "公尺" in i[14]:
                        value = float(''.join(c for c in i[14] if c.isdigit())) / 1000.0
                    else:
                        value = float(''.join(c for c in i[14] if c.isdigit()))
                    if "公里以上" in unit or "Over " in unit:
                        value = value + 10
                    observation.visibility = Element("W", value=value, units=unit.strip())
                    for k in metar:
                        if "/" in k:
                            observation.dew_point = Element("T", value=k.split("/")[1])
                        if len(k) >= 1 and "Q" == k[0]:
                            observation.pressure = Element("P", value=k[1:])

                    return observation
        return None

    def _parser_html(self, text):
        """ parser html """
        data = []
        soup = BeautifulSoup(text, 'html.parser')
        icaos = soup.find(id="select_icao")
        if icaos:
            results = icaos.find_all(language="JavaScript")
            if results:
                results2 = [re.sub(
                    "addarray(|)|'", "", i.string) for i in results]
                for i in results2:
                    value = i.split(",")
                    data.append(value)
        return data

    def _update_site(self):
        """Return the nearest DataPoint Site to the held latitude/longitude."""
        try:
            req = requests.post(
                self.uri,
                timeout=REQUEST_TIMEOUT)

        except requests.exceptions.RequestException:
            _LOGGER.error("Failed fetching data for %s", self.site_name)
            return

        if req.status_code == HTTPStatus.OK:
            self.data = self._parser_html(req.text)
            for i in self.data:
                for j in i:
                    if self._site in j:
                        self.site_name = self._site
        else:
            _LOGGER.error("Received error from ANWS AOAWS: %s", self.site_name)
            self.site_name = None
            self.now = None

        return self._site

    async def async_update(self):
        """Async wrapper for update method."""
        return await self._hass.async_add_executor_job(self._update)

    def _update(self):
        """Get the latest data from AOAWS."""
        if self.site_name is None:
            _LOGGER.error("No ANWS AOAWS observations site held, check logs for problems")
            return

        try:
            observations = self.get_observations_for_site(
                self._site, self.data
            )
            self.now = observations
        except (ValueError) as err:
            _LOGGER.error("Check ANWS AOAWS connection: %s", err.args)
            self.now = None
