"""Config flow for ANWS AOAWS integration."""
import logging

import voluptuous as vol

from homeassistant import config_entries, core, exceptions
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback
from homeassistant.const import CONF_API_KEY, CONF_LATITUDE, CONF_LONGITUDE, CONF_NAME
from homeassistant.helpers import config_validation as cv

from .const import (
    CONF_LANGUAGE,
    CONF_LOCATION_NAME,
    CONFIG_FLOW_VERSION,
    DEFAULT_LANGUAGE,
    DOMAIN,
    LANGUAGES,
    SITES
)
from .data import AnwsAoawseData

_LOGGER = logging.getLogger(__name__)


async def validate_input(hass: core.HomeAssistant, data):
    """Validate that the user input allows us to connect to DataPoint.

    Data has the keys from DATA_SCHEMA with values provided by the user.
    """

    site_name = data[CONF_LOCATION_NAME]
    language = data[CONF_LANGUAGE]

    anws_aoaws_data = AnwsAoawseData(hass, site_name, language)
    await anws_aoaws_data.async_update_site()
    if anws_aoaws_data.site_name is None:
        raise CannotConnect()

    return {"site_name": anws_aoaws_data.site_name}


class AnwsAoawsConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for ANWS AOAWS weather integration."""

    VERSION = CONFIG_FLOW_VERSION
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry):
        """ get option flow """
        return AnwsAoawsOptionsFlow(config_entry)

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            await self.async_set_unique_id(
                f"{user_input[CONF_LOCATION_NAME]}"
            )
            self._abort_if_unique_id_configured()

            try:
                info = await validate_input(self.hass, user_input)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                user_input[CONF_NAME] = info["site_name"]
                return self.async_create_entry(
                    title=user_input[CONF_NAME], data=user_input
                )

        data_schema = vol.Schema(
            {
                vol.Required(CONF_LOCATION_NAME): vol.In(
                    SITES
                ),
                vol.Optional(CONF_LANGUAGE, default=DEFAULT_LANGUAGE): vol.In(
                    LANGUAGES
                ),
            }
        )

        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )


class AnwsAoawsOptionsFlow(config_entries.OptionsFlow):
    """Handle options."""

    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=self._get_options_schema(),
        )

    def _get_options_schema(self):
        return vol.Schema(
            {
                vol.Optional(
                    CONF_LANGUAGE,
                    default=self.config_entry.options.get(
                        CONF_LANGUAGE, DEFAULT_LANGUAGE
                    ),
                ): vol.In(LANGUAGES),
            }
        )


class CannotConnect(exceptions.HomeAssistantError):
    """Error to indicate we cannot connect."""
