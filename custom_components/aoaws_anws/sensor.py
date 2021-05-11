"""Support for UK Met Office weather service."""
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import ATTR_ATTRIBUTION
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.typing import ConfigType

from .const import (
    ATTRIBUTION,
    ATTR_LAST_UPDATE,
    ATTR_SENSOR_ID,
    ATTR_SITE_ID,
    ATTR_SITE_NAME,
    CONDITION_CLASSES,
    DOMAIN,
    ANWS_AOAWS_COORDINATOR,
    ANWS_AOAWS_DATA,
    ANWS_AOAWS_NAME,
    SENSOR_TYPES,
    VISIBILITY_CLASSES
)
import logging
_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigType, async_add_entities
) -> None:
    """Set up the Met Office weather sensor platform."""
    hass_data = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        [
            AnwsAoawsCurrentSensor(entry.data, hass_data, sensor_type)
            for sensor_type in SENSOR_TYPES
        ],
        False,
    )


class AnwsAoawsCurrentSensor(SensorEntity):
    """Implementation of a Met Office current weather condition sensor."""

    def __init__(self, entry_data, hass_data, sensor_type):
        """Initialize the sensor."""
        self._data = hass_data[ANWS_AOAWS_DATA]
        self._coordinator = hass_data[ANWS_AOAWS_COORDINATOR]

        self._type = sensor_type
        self._name = f"{hass_data[ANWS_AOAWS_NAME]} {SENSOR_TYPES[self._type][0]}"
        self._unique_id = f"{SENSOR_TYPES[self._type][0]}_{self._data.site_name}"

        self.anws_aoaws_site_id = None
        self.anws_aoaws_site_name = None
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
    def state(self):
        """Return the state of the sensor."""
        value = None
        if self._type == "visibility_distance" and hasattr(
            self.anws_aoaws_now, "visibility"
        ):
            value = self.anws_aoaws_now.visibility.value

        if self._type == "visibility" and hasattr(self.anws_aoaws_now, "visibility"):
            _visibility = self.anws_aoaws_now.visibility.value
            value = "Very Poor"
            for k, v in VISIBILITY_CLASSES.items():
                if _visibility <= v:
                    value = k
                    break

        elif self._type == "weather" and hasattr(self.anws_aoaws_now, self._type):
            value = [
                k
                for k, v in CONDITION_CLASSES.items()
                if self.anws_aoaws_now.weather.value in v
            ][0]

        elif hasattr(self.anws_aoaws_now, self._type):
            value = getattr(self.anws_aoaws_now, self._type)

            if value and not isinstance(value, int):
                value = value.value

        return value

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return SENSOR_TYPES[self._type][2]

    @property
    def icon(self):
        """Return the icon for the entity card."""
        value = SENSOR_TYPES[self._type][3]
        if self._type == "weather":
            value = self.state
            if value is None:
                value = "sunny"
            elif value == "partlycloudy":
                value = "partly-cloudy"
            value = f"mdi:weather-{value}"

        return value

    @property
    def device_class(self):
        """Return the device class of the sensor."""
        return SENSOR_TYPES[self._type][1]

    @property
    def extra_state_attributes(self):
        """Return the state attributes of the device."""
        return {
            ATTR_ATTRIBUTION: ATTRIBUTION,
            ATTR_LAST_UPDATE: self.anws_aoaws_now.date if self.anws_aoaws_now else None,
            ATTR_SENSOR_ID: self._type,
            ATTR_SITE_NAME: self.anws_aoaws_site_name
            if self.anws_aoaws_site_name
            else None,
        }

    async def async_added_to_hass(self) -> None:
        """Set up a listener and load data."""
        self.async_on_remove(
            self._coordinator.async_add_listener(self._update_callback)
        )
        self._update_callback()

    async def async_update(self):
        """Schedule a custom update via the common entity update service."""
        await self._coordinator.async_request_refresh()

    @callback
    def _update_callback(self) -> None:
        """Load data from integration."""
        self.anws_aoaws_site_name = self._data.site_name
        self.anws_aoaws_now = self._data.now
        self.async_write_ha_state()

    @property
    def should_poll(self) -> bool:
        """Entities do not individually poll."""
        return False

    @property
    def entity_registry_enabled_default(self) -> bool:
        """Return if the entity should be enabled when first added to the entity registry."""
        return SENSOR_TYPES[self._type][4]

    @property
    def available(self):
        """Return if state is available."""
        return self.anws_aoaws_now is not None
