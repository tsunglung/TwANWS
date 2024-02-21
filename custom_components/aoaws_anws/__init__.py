"""The Taiwan ANWS integration."""
import asyncio
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_API_KEY, CONF_LATITUDE, CONF_LONGITUDE, CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo

from .const import (
    CONF_LANGUAGE,
    CONF_LOCATION_NAME,
    DEFAULT_SCAN_INTERVAL,
    DEFAULT_LANGUAGE,
    DOMAIN,
    ANWS_AOAWS_COORDINATOR,
    ANWS_AOAWS_DATA,
    ANWS_AOAWS_NAME,
    PLATFORMS,
    UPDATE_LISTENER,
)
from .data import AnwsAoawseData

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry):
    """Set up a ANWS AOAWS entry."""

    site_name = config_entry.data[CONF_LOCATION_NAME]
    language = _get_config_value(config_entry, CONF_LANGUAGE, DEFAULT_LANGUAGE)

    anws_aoaws_data = AnwsAoawseData(hass, site_name, language)
    await anws_aoaws_data.async_update_site()
    if anws_aoaws_data.site_name is None:
        raise ConfigEntryNotReady()

    anws_aoaws_coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=f"ANWS AOAWS for {site_name}",
        update_method=anws_aoaws_data.async_update,
        update_interval=DEFAULT_SCAN_INTERVAL,
    )

    anws_aoaws_hass_data = hass.data.setdefault(DOMAIN, {})
    anws_aoaws_hass_data[config_entry.entry_id] = {
        ANWS_AOAWS_DATA: anws_aoaws_data,
        ANWS_AOAWS_COORDINATOR: anws_aoaws_coordinator,
        ANWS_AOAWS_NAME: site_name,
    }

    # Fetch initial data so we have data when entities subscribe
    await anws_aoaws_coordinator.async_refresh()
    if anws_aoaws_data.now is None:
        raise ConfigEntryNotReady()

    for platform in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(config_entry, platform)
        )

    update_listener = config_entry.add_update_listener(async_update_options)
    hass.data[DOMAIN][config_entry.entry_id][UPDATE_LISTENER] = update_listener

    return True


async def async_update_options(hass: HomeAssistant, config_entry: ConfigEntry):
    """Update options."""
    await hass.config_entries.async_reload(config_entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry):
    """Unload a config entry."""
    unload_ok = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(config_entry, platform)
                for platform in PLATFORMS
            ]
        )
    )
    if unload_ok:
        update_listener = hass.data[DOMAIN][config_entry.entry_id][UPDATE_LISTENER]
        update_listener()
        hass.data[DOMAIN].pop(config_entry.entry_id)
        if not hass.data[DOMAIN]:
            hass.data.pop(DOMAIN)
    return unload_ok


def _get_config_value(config_entry, key, default):
    if config_entry.options:
        return config_entry.options.get(key, default)
    return config_entry.data.get(key, default)

def device_info(config_entry: ConfigEntry) -> DeviceInfo:
    """Build and return the device info for EC."""
    return DeviceInfo(
        entry_type=DeviceEntryType.SERVICE,
        identifiers={(DOMAIN, config_entry.entry_id)},
        manufacturer="Taiwan ANWS",
        name=config_entry.title,
        configuration_url="https://aoaws.anws.gov.tw/AWS",
    )
