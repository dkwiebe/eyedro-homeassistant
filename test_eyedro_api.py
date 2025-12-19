#!/usr/bin/env python3
"""Test script to validate Eyedro API response format.

This script queries an Eyedro device and validates that the response
matches the expected format from the official API documentation.
Uses only Python standard library (no external dependencies).

Usage:
    python3 test_eyedro_api.py <IP_ADDRESS> [PORT]

Example:
    python3 test_eyedro_api.py 192.168.2.66
    python3 test_eyedro_api.py 192.168.2.66 8080
"""
import argparse
import json
import sys
import urllib.request
import urllib.error
from typing import Any


def test_eyedro_api(host: str, port: int = 8080) -> None:
    """Test the Eyedro API endpoint and validate response format."""
    url = f"http://{host}:{port}/getdata"
    print(f"Testing Eyedro API at: {url}")
    print("-" * 60)

    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            status = response.getcode()
            json_data = json.loads(response.read().decode())

            print("✓ Successfully received response")
            print(f"✓ Response status: {status}")
            print()

            # Validate response structure
            print("Validating response structure...")
            if "data" not in json_data:
                print("✗ ERROR: Missing 'data' key in response")
                print(f"  Response keys: {list(json_data.keys())}")
                return

            print("✓ Response has 'data' key at root level")

            data = json_data["data"]
            if not isinstance(data, list):
                print(f"✗ ERROR: 'data' is not a list, got {type(data)}")
                return

            print(f"✓ 'data' is a list with {len(data)} channel(s)")

            if len(data) < 1:
                print("✗ ERROR: 'data' list is empty")
                return

            if len(data) < 2:
                print("⚠ WARNING: Only one channel found (expected 2 for EYEFI-2)")

            # Validate each channel
            print()
            print("Channel data validation:")
            for i, channel_data in enumerate(data):
                print(f"\n  Channel {i}:")
                if not isinstance(channel_data, list):
                    print(f"    ✗ ERROR: Channel {i} data is not a list, got {type(channel_data)}")
                    continue

                print(f"    ✓ Is a list with {len(channel_data)} element(s)")

                if len(channel_data) < 4:
                    print(f"    ✗ ERROR: Channel {i} has fewer than 4 elements (need at least 4)")
                    continue

                # Parse and display values
                power_factor = channel_data[0]
                voltage = channel_data[1]
                current = channel_data[2]
                power = channel_data[3]
                ignore = channel_data[4] if len(channel_data) > 4 else None

                print(f"    [0] Power Factor: {power_factor} (milli-units, {power_factor/10:.1f}%)")
                print(f"    [1] Voltage: {voltage} (centivolts, {voltage/100:.2f}V)")
                print(f"    [2] Current: {current} (milliamps, {current/1000:.3f}A)")
                print(f"    [3] Power: {power} (watts, {power/1000:.3f}kW)")
                if ignore is not None:
                    print(f"    [4] Ignored field: {ignore}")

            # Test calculations (like our sensors do)
            if len(data) >= 2:
                print()
                print("Calculated sensor values (as integration would compute):")
                ch0 = data[0]
                ch1 = data[1]

                # Total Power (kW)
                total_power_w = ch0[3] + ch1[3]
                total_power_kw = total_power_w / 1000
                print(f"  Total Power: {total_power_w}W = {total_power_kw:.3f}kW")

                # Total Current (A)
                total_current_ma = ch0[2] + ch1[2]
                total_current_a = total_current_ma / 1000
                print(f"  Total Current: {total_current_ma}mA = {total_current_a:.3f}A")

                # Average Voltage (V)
                total_voltage_cv = ch0[1] + ch1[1]
                avg_voltage_v = total_voltage_cv / 200
                print(f"  Average Voltage: {total_voltage_cv}cV / 200 = {avg_voltage_v:.2f}V")

                # Average Power Factor (%)
                total_pf_mu = ch0[0] + ch1[0]
                avg_pf_pct = total_pf_mu / 20
                print(f"  Average Power Factor: {total_pf_mu}mu / 20 = {avg_pf_pct:.2f}%")

            print()
            print("=" * 60)
            print("Raw JSON response:")
            print(json.dumps(json_data, indent=2))

    except urllib.error.URLError as err:
        print(f"✗ ERROR: Failed to connect to device: {err}")
        if hasattr(err, 'reason'):
            print(f"  Reason: {err.reason}")
        sys.exit(1)
    except json.JSONDecodeError as err:
        print(f"✗ ERROR: Invalid JSON response: {err}")
        sys.exit(1)
    except Exception as err:
        print(f"✗ ERROR: Unexpected error: {err}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Test script to validate Eyedro API response format"
    )
    parser.add_argument(
        "host",
        help="IP address of the Eyedro device (e.g., 192.168.2.66)",
    )
    parser.add_argument(
        "port",
        nargs="?",
        type=int,
        default=8080,
        help="Port number (default: 8080)",
    )
    args = parser.parse_args()

    test_eyedro_api(args.host, args.port)


if __name__ == "__main__":
    main()

