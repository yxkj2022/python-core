"""Support for Fibaro switches."""
from __future__ import annotations

from homeassistant.components.switch import DOMAIN, SwitchEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.util import convert

from . import FIBARO_DEVICES, FibaroDevice


def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the Fibaro switches."""
    if discovery_info is None:
        return

    add_entities(
        [FibaroSwitch(device) for device in hass.data[FIBARO_DEVICES]["switch"]], True
    )


class FibaroSwitch(FibaroDevice, SwitchEntity):
    """Representation of a Fibaro Switch."""

    def __init__(self, fibaro_device):
        """Initialize the Fibaro device."""
        self._state = False
        super().__init__(fibaro_device)
        self.entity_id = f"{DOMAIN}.{self.ha_id}"

    def turn_on(self, **kwargs):
        """Turn device on."""
        self.call_turn_on()
        self._state = True

    def turn_off(self, **kwargs):
        """Turn device off."""
        self.call_turn_off()
        self._state = False

    @property
    def current_power_w(self):
        """Return the current power usage in W."""
        if "power" in self.fibaro_device.interfaces:
            return convert(self.fibaro_device.properties.power, float, 0.0)
        return None

    @property
    def today_energy_kwh(self):
        """Return the today total energy usage in kWh."""
        if "energy" in self.fibaro_device.interfaces:
            return convert(self.fibaro_device.properties.energy, float, 0.0)
        return None

    @property
    def is_on(self):
        """Return true if device is on."""
        return self._state

    def update(self):
        """Update device state."""
        self._state = self.current_binary_state
