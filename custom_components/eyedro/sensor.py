"""Sensor platform for Eyedro integration."""
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfPower, UnitOfElectricCurrent, UnitOfElectricPotential, PERCENTAGE
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DOMAIN,
    SENSOR_AVERAGE_POWER_FACTOR,
    SENSOR_AVERAGE_VOLTAGE,
    SENSOR_TOTAL_CURRENT,
    SENSOR_TOTAL_POWER,
)
from .coordinator import EyedroDataUpdateCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Eyedro sensors from a config entry."""
    coordinator: EyedroDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    sensors = [
        EyedroTotalPowerSensor(coordinator, SENSOR_TOTAL_POWER),
        EyedroTotalCurrentSensor(coordinator, SENSOR_TOTAL_CURRENT),
        EyedroAverageVoltageSensor(coordinator, SENSOR_AVERAGE_VOLTAGE),
        EyedroAveragePowerFactorSensor(coordinator, SENSOR_AVERAGE_POWER_FACTOR),
    ]

    async_add_entities(sensors)


class EyedroSensor(CoordinatorEntity, SensorEntity):
    """Base class for Eyedro sensors."""

    def __init__(self, coordinator: EyedroDataUpdateCoordinator, unique_id_suffix: str) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{DOMAIN}_{coordinator.api._host}_{unique_id_suffix}"


class EyedroTotalPowerSensor(EyedroSensor):
    """Sensor for total power consumption."""

    _attr_native_unit_of_measurement = UnitOfPower.KILO_WATT
    _attr_device_class = SensorDeviceClass.POWER
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, coordinator: EyedroDataUpdateCoordinator, unique_id_suffix: str) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, unique_id_suffix)
        self._attr_name = "Eyedro Total Power"

    @property
    def native_value(self) -> float | None:
        """Return the state of the sensor."""
        if not self.coordinator.data or "channels" not in self.coordinator.data:
            return None

        channels = self.coordinator.data["channels"]
        if len(channels) < 2:
            return None

        # Power is in watts, convert to kW by dividing by 1000
        total_power_watts = channels[0]["power"] + channels[1]["power"]
        return round(total_power_watts / 1000, 3)


class EyedroTotalCurrentSensor(EyedroSensor):
    """Sensor for total current."""

    _attr_native_unit_of_measurement = UnitOfElectricCurrent.AMPERE
    _attr_device_class = SensorDeviceClass.CURRENT
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, coordinator: EyedroDataUpdateCoordinator, unique_id_suffix: str) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, unique_id_suffix)
        self._attr_name = "Eyedro Total Current"

    @property
    def native_value(self) -> float | None:
        """Return the state of the sensor."""
        if not self.coordinator.data or "channels" not in self.coordinator.data:
            return None

        channels = self.coordinator.data["channels"]
        if len(channels) < 2:
            return None

        # Current is in milliamps, convert to amps by dividing by 1000
        total_current_ma = channels[0]["current"] + channels[1]["current"]
        return round(total_current_ma / 1000, 3)


class EyedroAverageVoltageSensor(EyedroSensor):
    """Sensor for average voltage."""

    _attr_native_unit_of_measurement = UnitOfElectricPotential.VOLT
    _attr_device_class = SensorDeviceClass.VOLTAGE
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, coordinator: EyedroDataUpdateCoordinator, unique_id_suffix: str) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, unique_id_suffix)
        self._attr_name = "Eyedro Average Voltage"

    @property
    def native_value(self) -> float | None:
        """Return the state of the sensor."""
        if not self.coordinator.data or "channels" not in self.coordinator.data:
            return None

        channels = self.coordinator.data["channels"]
        if len(channels) < 2:
            return None

        # Voltage is in tens of millivolts, convert to volts by dividing by 100
        # Average of two values: (v1 + v2) / 200
        total_voltage_tens_mv = channels[0]["voltage"] + channels[1]["voltage"]
        return round(total_voltage_tens_mv / 200, 2)


class EyedroAveragePowerFactorSensor(EyedroSensor):
    """Sensor for average power factor."""

    _attr_native_unit_of_measurement = PERCENTAGE
    _attr_device_class = SensorDeviceClass.POWER_FACTOR
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, coordinator: EyedroDataUpdateCoordinator, unique_id_suffix: str) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, unique_id_suffix)
        self._attr_name = "Eyedro Average Power Factor"

    @property
    def native_value(self) -> float | None:
        """Return the state of the sensor."""
        if not self.coordinator.data or "channels" not in self.coordinator.data:
            return None

        channels = self.coordinator.data["channels"]
        if len(channels) < 2:
            return None

        # Power factor is in milli-units (988 = 0.988), convert to percent by dividing by 10
        # Average of two values: (pf1 + pf2) / 20 = (pf1/10 + pf2/10) / 2
        total_pf_milli_units = channels[0]["power_factor"] + channels[1]["power_factor"]
        return round(total_pf_milli_units / 20, 2)

