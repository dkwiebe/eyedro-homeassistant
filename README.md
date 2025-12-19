# Eyedro Home Assistant Integration

**⚠️ UNOFFICIAL INTEGRATION** - This is a custom, unofficial Home Assistant integration for Eyedro energy monitoring devices. It is not developed, endorsed, or supported by Eyedro or Home Assistant.

**🚧 UNDER ACTIVE DEVELOPMENT** - This integration is currently under active development and **does not work yet**. The code structure is in place, but it has not been tested and may contain bugs or incomplete functionality. Use at your own risk.

## About

Custom Home Assistant integration for Eyedro energy monitoring devices. This project is currently in development and not yet functional.

## Features

- **Total Power** (kW): Sum of power consumption from both channels
- **Total Current** (A): Sum of current from both channels
- **Average Voltage** (V): Average voltage across both channels
- **Average Power Factor** (%): Average power factor across both channels

## Installation

**Note: This integration is not yet functional. Installation instructions are for reference only.**

### HACS Installation (Recommended)

Once development is complete, you can install this integration via HACS:

1. Make sure [HACS](https://hacs.xyz/) is installed in your Home Assistant instance

2. In HACS, go to **Integrations**

3. Click the three dots (⋮) in the top right corner and select **Custom repositories**

4. Add this repository:
   - Repository: `https://github.com/dkwiebe/eyedro-homeassistant`
   - Category: **Integration**
   - Click **ADD**

5. Search for "Eyedro" in HACS and click **Download**

6. Restart Home Assistant

7. Go to Settings → Devices & Services → Add Integration and search for "Eyedro"

### Manual Installation

Alternatively, you can install manually:

1. Copy the `custom_components/eyedro` directory to your Home Assistant `custom_components` directory:
   ```
   <config directory>/custom_components/eyedro/
   ```

2. Restart Home Assistant

3. Go to Settings → Devices & Services → Add Integration

4. Search for "Eyedro" and follow the setup wizard

### Configuration

The integration can be configured through the Home Assistant UI:

1. **Host IP Address**: The IP address of your Eyedro device (e.g., `192.168.2.66`)
2. **Port**: The port number (default: `8080`)
3. **Scan Interval**: How often to poll the device in seconds (default: `10`, range: 5-300)

## API Details

The integration connects to the Eyedro device's local API endpoint:
- **Endpoint**: `http://<IP_ADDRESS>:<PORT>/getdata`
- **Response Format**: JSON with two-channel data array containing power factor, voltage, current, and power values

### Data Units

The Eyedro API returns data in the following units (per [official API documentation](https://eyedro.com/eyefi-getdata-api-command-sample-code/)):
- Power Factor: Milli-units (e.g., 988 = 0.988, converted to % by dividing by 10)
- Voltage: Centivolts (e.g., 11665 = 116.65V, converted to volts by dividing by 100)
- Current: Milliamps (e.g., 11800 = 11.8A, converted to amps by dividing by 1000)
- Power: Watts (e.g., 1360 = 1360W, converted to kW by dividing by 1000)

## Creating Energy Sensors

To track total energy consumption over time, you can create an energy sensor using Home Assistant's integration platform:

```yaml
sensor:
  - platform: integration
    source: sensor.eyedro_total_power
    name: "Eyedro Total Energy"
    unique_id: eyedro_total_energy
    round: 2
```

## Requirements

- Home Assistant 2023.1.0 or later
- aiohttp (installed automatically via manifest requirements)

## Development

This integration follows the standard Home Assistant custom component structure and best practices as outlined in the [Home Assistant Developer Documentation](https://developers.home-assistant.io/docs/creating_component_index/).

### Testing the API

A test script is included to validate the Eyedro API response format. This can help verify that your device's response matches the expected format before using the integration. The script uses only Python standard library (no external dependencies required).

```bash
python3 test_eyedro_api.py <IP_ADDRESS> [PORT]
```

**Example:**
```bash
python3 test_eyedro_api.py 192.168.2.66 8080
```

The test script will:
- Query the Eyedro device at the specified IP and port
- Validate the response structure matches the expected format
- Display all channel data with unit conversions
- Show calculated sensor values (as the integration would compute them)
- Display the raw JSON response

This is useful for debugging and verifying API compatibility.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

This is an unofficial integration and is provided as-is without warranty.

