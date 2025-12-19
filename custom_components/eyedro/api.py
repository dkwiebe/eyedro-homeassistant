"""API client for Eyedro device."""
import aiohttp
import logging
from typing import Any

from .const import API_PATH_GETDATA, DEFAULT_TIMEOUT

_LOGGER = logging.getLogger(__name__)


class EyedroAPI:
    """API client for Eyedro energy monitoring device."""

    def __init__(self, host: str, port: int, session: aiohttp.ClientSession) -> None:
        """Initialize the API client."""
        self._host = host
        self._port = port
        self._session = session
        self._base_url = f"http://{host}:{port}"

    async def async_get_data(self) -> dict[str, Any]:
        """
        Fetch data from the Eyedro device.

        Returns:
            Dictionary with parsed data structure containing channels with
            power_factor, voltage, current, and power values.

        Raises:
            aiohttp.ClientError: If the request fails
        """
        url = f"{self._base_url}{API_PATH_GETDATA}"
        timeout = aiohttp.ClientTimeout(total=DEFAULT_TIMEOUT)

        try:
            async with self._session.get(url, timeout=timeout) as response:
                response.raise_for_status()
                json_data = await response.json()

                # Parse the response structure
                # {"response": {"data": [[pf, voltage, current, power], [pf, voltage, current, power]]}}
                if "response" not in json_data:
                    raise ValueError("Missing 'response' key in API response")

                response_data = json_data["response"]
                if "data" not in response_data:
                    raise ValueError("Missing 'data' key in API response")

                data = response_data["data"]
                if not isinstance(data, list) or len(data) < 2:
                    raise ValueError(
                        f"Expected data array with at least 2 channels, got {len(data) if isinstance(data, list) else type(data)}"
                    )

                # Structure the data for easier access
                channels = []
                for i, channel_data in enumerate(data[:2]):  # Process first 2 channels
                    if not isinstance(channel_data, list) or len(channel_data) < 4:
                        raise ValueError(
                            f"Channel {i} data should be an array with 4 elements"
                        )

                    channels.append(
                        {
                            "power_factor": channel_data[0],
                            "voltage": channel_data[1],
                            "current": channel_data[2],
                            "power": channel_data[3],
                        }
                    )

                return {"channels": channels}

        except aiohttp.ClientError as err:
            _LOGGER.error("Error fetching data from Eyedro device: %s", err)
            raise
        except (ValueError, KeyError, TypeError) as err:
            _LOGGER.error("Error parsing Eyedro API response: %s", err)
            raise ValueError(f"Invalid API response format: {err}") from err

