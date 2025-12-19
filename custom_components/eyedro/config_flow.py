"""Config flow for Eyedro integration."""
from __future__ import annotations

import logging
import re
from typing import Any

import aiohttp
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PORT, CONF_SCAN_INTERVAL
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import config_validation as cv

from .const import API_PATH_GETDATA, DEFAULT_PORT, DEFAULT_SCAN_INTERVAL, DOMAIN

_LOGGER = logging.getLogger(__name__)

# IP address validation pattern
IP_ADDRESS_PATTERN = re.compile(
    r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
)


def validate_ip_address(ip: str) -> bool:
    """Validate IP address format."""
    return IP_ADDRESS_PATTERN.match(ip) is not None


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect."""
    host = data[CONF_HOST].strip()
    port = data.get(CONF_PORT, DEFAULT_PORT)
    
    # Validate IP address format
    if not validate_ip_address(host):
        raise ValueError("Invalid IP address format")
    
    url = f"http://{host}:{port}{API_PATH_GETDATA}"

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                response.raise_for_status()
                json_data = await response.json()
                # Official API returns: {"data": [[...], [...]]}
                # See: https://eyedro.com/eyefi-getdata-api-command-sample-code/
                if "data" not in json_data or not isinstance(json_data.get("data"), list):
                    raise ValueError("Invalid response format from Eyedro device")
        except aiohttp.ClientError as err:
            raise CannotConnect from err
        except (ValueError, KeyError) as err:
            raise InvalidAuth from err

    return {"title": f"Eyedro {host}"}


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Eyedro."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
            except ValueError as err:
                if "Invalid IP address" in str(err):
                    errors[CONF_HOST] = "invalid_ip"
                else:
                    errors["base"] = "invalid_auth"
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                # Check for existing entries with the same host:port combination
                await self.async_set_unique_id(
                    f"{user_input[CONF_HOST]}:{user_input.get(CONF_PORT, DEFAULT_PORT)}"
                )
                self._abort_if_unique_id_configured()
                
                # Store the validated and cleaned host
                entry_data = {
                    CONF_HOST: user_input[CONF_HOST].strip(),
                    CONF_PORT: user_input.get(CONF_PORT, DEFAULT_PORT),
                    CONF_SCAN_INTERVAL: user_input.get(
                        CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL.seconds
                    ),
                }
                
                return self.async_create_entry(title=info["title"], data=entry_data)

        data_schema = vol.Schema(
            {
                vol.Required(CONF_HOST, default=""): str,
                vol.Optional(CONF_PORT, default=DEFAULT_PORT): cv.port,
                vol.Optional(
                    CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL.seconds
                ): vol.All(vol.Coerce(int), vol.Range(min=5, max=300)),
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
        )


class CannotConnect(config_entries.ConfigFlowError):
    """Error to indicate we cannot connect."""


class InvalidAuth(config_entries.ConfigFlowError):
    """Error to indicate there is invalid auth."""

