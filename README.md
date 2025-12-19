# Eyedro Home Assistant Integration

**⚠️ UNOFFICIAL INTEGRATION** - This is a custom, unofficial Home Assistant integration for Eyedro energy monitoring devices. It is not developed, endorsed, or supported by Eyedro or Home Assistant.

## About

Custom Home Assistant integration for Eyedro energy monitoring devices.

## Features

- **Total Power** (kW): Sum of power consumption from both channels
- **Total Current** (A): Sum of current from both channels
- **Average Voltage** (V): Average voltage across both channels
- **Average Power Factor** (%): Average power factor across both channels

## Installation

### Manual Installation

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

The Eyedro API returns data in the following units:
- Power Factor: Tenths of percent (converted to % by dividing by 10)
- Voltage: Tens of millivolts (converted to volts by dividing by 100)
- Current: Milliamps (converted to amps by dividing by 1000)
- Power: Watts (converted to kW by dividing by 1000)

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

## License

This project is licensed under the MIT License. See the LICENSE file for details.

This is an unofficial integration and is provided as-is without warranty.

