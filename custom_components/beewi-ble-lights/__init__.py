from __future__ import annotations

from homeassistant.components import bluetooth
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

from .const import DOMAIN
from .light import BeewiSmartLight  # Assuming this is your light entity class

PLATFORMS: list[str] = ["light"]


class Hub:
    def __init__(self, hass: HomeAssistant, address: str) -> None:
        """Initialize the Beewi hub."""
        self.address = address
        self.bulb = BeewiSmartLight(address)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Beewi Smart Bulb from a config entry."""
    address = entry.unique_id
    assert address is not None
    ble_device = bluetooth.async_ble_device_from_address(hass, address.upper(), True)
    if not ble_device:
        raise ConfigEntryNotReady(
            f"Could not find Beewi BLE device with address {address}"
        )

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = Hub(hass, address=address)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
