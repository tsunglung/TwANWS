"""Support for ANWS AOAWS service."""
from homeassistant.components.weather import WeatherEntity
from homeassistant.const import LENGTH_KILOMETERS, TEMP_CELSIUS
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.typing import ConfigType

from .const import (
    ATTRIBUTION,
    CONDITION_CLASSES,
    DEFAULT_NAME,
    DOMAIN,
    ANWS_AOAWS_COORDINATOR,
    ANWS_AOAWS_DATA,
    ANWS_AOAWS_NAME,
)


async def async_setup_entry(
    hass: HomeAssistant, config_entry: ConfigType, async_add_entities
) -> None:
    """Set up the Anws Aoaws weather sensor platform."""
    hass_data = hass.data[DOMAIN][config_entry.entry_id]

    async_add_entities(
        [
            AnwsAoawsWeather(
                config_entry.data,
                hass_data,
            )
        ],
        False,
    )


class AnwsAoawsWeather(WeatherEntity):
    """Implementation of a Anws Aoaws weather condition."""

    def __init__(self, entry_data, hass_data):
        """Initialise the platform with a data instance."""
        self._data = hass_data[ANWS_AOAWS_DATA]
        self._coordinator = hass_data[ANWS_AOAWS_COORDINATOR]

        self._name = f"{DEFAULT_NAME} {hass_data[ANWS_AOAWS_NAME]}"
        self._unique_id = f"{self._data.site_name}"

        self.anws_aoaws_now = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def unique_id(self):
        """Return the unique of the sensor."""
        return self._unique_id

    @property
    def condition(self):
        """Return the current condition."""
        return (
            [
                k
                for k, v in CONDITION_CLASSES.items()
                if self.anws_aoaws_now.weather.value in v
            ][0]
            if self.anws_aoaws_now
            else None
        )

    @property
    def temperature(self):
        """Return the platform temperature."""
        return (
            self.anws_aoaws_now.temperature.value
            if self.anws_aoaws_now and self.anws_aoaws_now.temperature
            else None
        )

    @property
    def temperature_unit(self):
        """Return the unit of measurement."""
        return TEMP_CELSIUS

    @property
    def visibility(self):
        """Return the platform visibility."""
        return (
            self.anws_aoaws_now.visibility.value
            if self.anws_aoaws_now and self.anws_aoaws_now.visibility
            else None
        )

    @property
    def visibility_unit(self):
        """Return the unit of measurement."""
        return self.anws_aoaws_now.visibility.units

    @property
    def pressure(self):
        """Return the mean sea-level pressure."""
        return (
            self.anws_aoaws_now.pressure.value
            if self.anws_aoaws_now and self.anws_aoaws_now.pressure
            else None
        )

    @property
    def humidity(self):
        """Return the relative humidity."""
        return (
            self.anws_aoaws_now.humidity.value
            if self.anws_aoaws_now and self.anws_aoaws_now.humidity
            else None
        )

    @property
    def wind_speed(self):
        """Return the wind speed."""
        return (
            self.anws_aoaws_now.wind_speed.value
            if self.anws_aoaws_now and self.anws_aoaws_now.wind_speed
            else None
        )

    @property
    def wind_bearing(self):
        """Return the wind bearing."""
        return (
            self.anws_aoaws_now.wind_direction.value
            if self.anws_aoaws_now and self.anws_aoaws_now.wind_direction
            else None
        )

    @property
    def attribution(self):
        """Return the attribution."""
        return ATTRIBUTION

    async def async_added_to_hass(self) -> None:
        """Set up a listener and load data."""
        self.async_on_remove(
            self._coordinator.async_add_listener(self._update_callback)
        )
        self._update_callback()

    @callback
    def _update_callback(self) -> None:
        """Load data from integration."""
        self.anws_aoaws_now = self._data.now
        self.async_write_ha_state()

    @property
    def should_poll(self) -> bool:
        """Entities do not individually poll."""
        return False

    @property
    def available(self):
        """Return if state is available."""
        return self.anws_aoaws_now is not None
