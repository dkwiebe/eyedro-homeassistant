"""Constants for the Eyedro integration."""
from datetime import timedelta

DOMAIN = "eyedro"

# Default values
DEFAULT_PORT = 8080
DEFAULT_SCAN_INTERVAL = timedelta(seconds=10)
DEFAULT_TIMEOUT = 10

# API endpoint path
API_PATH_GETDATA = "/getdata"

# Sensor types
SENSOR_TOTAL_POWER = "total_power"
SENSOR_TOTAL_CURRENT = "total_current"
SENSOR_AVERAGE_VOLTAGE = "average_voltage"
SENSOR_AVERAGE_POWER_FACTOR = "average_power_factor"

# Data array indices
IDX_POWER_FACTOR = 0
IDX_VOLTAGE = 1
IDX_CURRENT = 2
IDX_POWER = 3

