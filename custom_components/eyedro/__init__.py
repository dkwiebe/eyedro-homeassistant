"""The Eyedro integration."""
from __future__ import annotations

from datetime import timedelta

import aiohttp

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_PORT, CONF_SCAN_INTERVAL
from homeassistant.core import HomeAssistant

from .const import DEFAULT_PORT, DEFAULT_SCAN_INTERVAL, DOMAIN
from .coordinator import EyedroDataUpdateCoordinator
from .api import EyedroAPI

PLATFORMS: list[str] = ["sensor"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Eyedro from a config entry."""
    host = entry.data[CONF_HOST]
    port = entry.data.get(CONF_PORT, DEFAULT_PORT)
    # Get scan interval from options first, then fall back to data
    scan_interval = timedelta(
        seconds=entry.options.get(
            CONF_SCAN_INTERVAL,
            entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL.seconds),
        )
    )

    # Create aiohttp session
    session = aiohttp.ClientSession()

    try:
        # Initialize API client
        api = EyedroAPI(host=host, port=port, session=session)

        # Initialize coordinator
        coordinator = EyedroDataUpdateCoordinator(hass, api, update_interval=scan_interval)

        # Fetch initial data so we have data when the entities are added
        await coordinator.async_config_entry_first_refresh()

        # Store coordinator in hass data
        hass.data.setdefault(DOMAIN, {})
        hass.data[DOMAIN][entry.entry_id] = coordinator

        # Set up platforms
        await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

        # Set up options update listener
        entry.async_on_unload(
            entry.add_update_listener(async_update_options)
        )

        return True
    except Exception:
        # Clean up session if setup fails
        await session.close()
        raise


async def async_update_options(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Handle options update."""
    # Update coordinator's update interval if scan_interval changed
    coordinator: EyedroDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    new_scan_interval = timedelta(
        seconds=entry.options.get(
            CONF_SCAN_INTERVAL,
            entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL.seconds),
        )
    )
    coordinator.update_interval = new_scan_interval


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        coordinator: EyedroDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
        # Close the aiohttp session
        if coordinator.api._session and not coordinator.api._session.closed:
            await coordinator.api._session.close()
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok

