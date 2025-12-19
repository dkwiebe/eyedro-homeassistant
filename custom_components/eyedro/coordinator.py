"""DataUpdateCoordinator for Eyedro integration."""
from datetime import timedelta
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import EyedroAPI
from .const import DEFAULT_SCAN_INTERVAL, DOMAIN

_LOGGER = logging.getLogger(__name__)


class EyedroDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the Eyedro API."""

    def __init__(
        self,
        hass: HomeAssistant,
        api: EyedroAPI,
        update_interval: timedelta | None = None,
    ) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=update_interval or DEFAULT_SCAN_INTERVAL,
        )
        self.api = api

    async def _async_update_data(self) -> dict:
        """Fetch data from Eyedro API."""
        try:
            data = await self.api.async_get_data()
            return data
        except Exception as err:
            raise UpdateFailed(f"Error communicating with Eyedro API: {err}") from err

