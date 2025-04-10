"""Support for Taiwan ANWS service."""
from homeassistant.components.weather import WeatherEntityFeature, SingleCoordinatorWeatherEntity
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.typing import ConfigType
from homeassistant.const import UnitOfTemperature, UnitOfSpeed

from . import device_info
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
    """Set up the Taiwan ANWS weather sensor platform."""
    hass_data = hass.data[DOMAIN][config_entry.entry_id]
    weather_coordinator = hass_data[ANWS_AOAWS_COORDINATOR]

    async_add_entities(
        [
            AnwsAoawsWeather(
                config_entry,
                hass_data,
                weather_coordinator
            )
        ],
        False,
    )


class AnwsAoawsWeather(SingleCoordinatorWeatherEntity):
    """Implementation of a Anws Aoaws weather condition."""
    _attr_supported_features = WeatherEntityFeature.FORECAST_HOURLY

    def __init__(self, config_entry, hass_data, coordinator):
        """Initialise the platform with a data instance."""
        super().__init__(coordinator)
        self._data = hass_data[ANWS_AOAWS_DATA]
        self._coordinator = coordinator

        self._name = f"{DEFAULT_NAME} {hass_data[ANWS_AOAWS_NAME]}"
        self._unique_id = f"{self._data.site_name}"
        self._attr_device_info = device_info(config_entry)

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
        for k, v in CONDITION_CLASSES.items():
            if self.anws_aoaws_now.weather.value.lower().strip() in v:
                return k
        return None

    @property
    def cloud_coverage(self) -> float | None:
        """Return the Cloud coverage in %."""
        return (
            self.anws_aoaws_now.cloud_coverage.value
            if self.anws_aoaws_now and self.anws_aoaws_now.cloud_coverage
            else None
        )

    @property
    def native_apparent_temperature(self) -> float | None:
        """Return the apparent temperature."""
        return (
            self.anws_aoaws_now.temperature.value
            if self.anws_aoaws_now and self.anws_aoaws_now.temperature
            else None
        )

    @property
    def native_temperature(self) -> float | None:
        """Return the temperature."""
        return (
            self.anws_aoaws_now.temperature.value
            if self.anws_aoaws_now and self.anws_aoaws_now.temperature
            else None
        )

    @property
    def native_pressure(self) -> float | None:
        """Return the pressure."""
        return (
            self.anws_aoaws_now.pressure.value
            if self.anws_aoaws_now and self.anws_aoaws_now.pressure
            else None
        )

    @property
    def humidity(self) -> float | None:
        """Return the humidity."""
        return (
            self.anws_aoaws_now.humidity.value
            if self.anws_aoaws_now and self.anws_aoaws_now.humidity
            else None
        )

    @property
    def native_dew_point(self) -> float | None:
        """Return the dew point."""
        return (
            self.anws_aoaws_now.dew_point.value
            if self.anws_aoaws_now and self.anws_aoaws_now.dew_point
            else None
        )

    @property
    def native_wind_gust_speed(self) -> float | None:
        """Return the wind gust speed."""
        return (
            self.anws_aoaws_now.wind_speed.value
            if self.anws_aoaws_now and self.anws_aoaws_now.wind_speed
            else None
        )

    @property
    def native_wind_speed(self) -> float | None:
        """Return the wind speed."""
        return (
            self.anws_aoaws_now.wind_speed.value
            if self.anws_aoaws_now and self.anws_aoaws_now.wind_speed
            else None
        )

    @property
    def wind_bearing(self) -> float | str | None:
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
        self._attr_temperature_unit = self.anws_aoaws_now.temperature.units if self.anws_aoaws_now.temperature else UnitOfTemperature.CELSIUS
#        self._attr_visibility_unit = self.anws_aoaws_now.visibility.units
        self._attr_wind_speed_unit = self.anws_aoaws_now.wind_speed.units if self.anws_aoaws_now.wind_speed else UnitOfSpeed.KILOMETERS_PER_HOUR
        self._attr_temperature = (
            self.anws_aoaws_now.temperature.value
            if self.anws_aoaws_now and self.anws_aoaws_now.temperature
            else None
        )
        self._attr_pressure = (
            self.anws_aoaws_now.pressure.value
            if self.anws_aoaws_now and self.anws_aoaws_now.pressure
            else None
        )
        self._attr_wind_speed = (
            self.anws_aoaws_now.wind_speed.value
            if self.anws_aoaws_now and self.anws_aoaws_now.wind_speed
            else None
        )
        self._attr_visibility =  (
            self.anws_aoaws_now.visibility.value
            if self.anws_aoaws_now and self.anws_aoaws_now.visibility
            else None
        )
        self._attr_humidity = (
            self.anws_aoaws_now.humidity.value
            if self.anws_aoaws_now and self.anws_aoaws_now.humidity
            else None
        )
        self._attr_wind_bearing =  (
            self.anws_aoaws_now.wind_direction.value
            if self.anws_aoaws_now and self.anws_aoaws_now.wind_direction
            else None
        )

        self.async_write_ha_state()

    @property
    def should_poll(self) -> bool:
        """Entities do not individually poll."""
        return False

    @property
    def available(self):
        """Return if state is available."""
        return self.anws_aoaws_now is not None
