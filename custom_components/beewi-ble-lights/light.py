"""Light platform for BeewiPy integration."""
from homeassistant.components.light import (
    LightEntity,
    SUPPORT_BRIGHTNESS,
    SUPPORT_COLOR,
    SUPPORT_COLOR_TEMP,
    ATTR_BRIGHTNESS,
    ATTR_HS_COLOR,
    ATTR_COLOR_TEMP,
)
import colorsys
from BeewiPy import BeewiSmartBulb
from . import DOMAIN


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the Beewi light platform from a config entry."""
    mac_address = config_entry.data.get("mac_address")
    async_add_entities([BeewiSmartLight(mac_address)], True)


class BeewiSmartLight(LightEntity):
    def __init__(self, mac_address):
        """Initialize the Beewi light."""
        self._bulb = BeewiSmartBulb(mac_address)
        self._is_on = self._bulb.isOn
        self._brightness = self._bulb.brightness
        self._color_temp = self._bulb.temperature
        self._hs_color = colorsys.rgb_to_hsv(
            self._bulb.red, self._bulb.green, self._bulb.blue
        )

    @property
    def name(self):
        """Return the display name of this light."""
        return "Beewi Smart Bulb"

    @property
    def is_on(self):
        """Return True if light is on."""
        return self._is_on

    @property
    def brightness(self):
        """Return the brightness of this light."""
        return self._brightness

    @property
    def hs_color(self):
        """Return the hs color value."""
        return self._hs_color

    @property
    def color_temp(self):
        """Return the color temperature."""
        return self._color_temp

    @property
    def supported_features(self):
        """Flag supported features."""
        return SUPPORT_BRIGHTNESS | SUPPORT_COLOR | SUPPORT_COLOR_TEMP

    def turn_on(self, **kwargs):
        """Instruct the light to turn on."""
        self._bulb.turnOn()
        self._is_on = True

        if ATTR_BRIGHTNESS in kwargs:
            brightness = kwargs[ATTR_BRIGHTNESS]
            self._bulb.setBrightness(brightness)
            self._brightness = brightness

        if ATTR_HS_COLOR in kwargs:
            hs_color = kwargs[ATTR_HS_COLOR]
            rgb_color = colorsys.hsv_to_rgb(*hs_color)
            self._bulb.setColor(*rgb_color)
            self._hs_color = hs_color

        if ATTR_COLOR_TEMP in kwargs:
            color_temp = kwargs[ATTR_COLOR_TEMP]
            self._bulb.setTemperature(color_temp)
            self._color_temp = color_temp

    def turn_off(self, **kwargs):
        """Instruct the light to turn off."""
        self._bulb.turnOff()
        self._is_on = False

    def update(self):
        """Fetch new state data for this light."""
        self._bulb.getSettings()
        self._is_on = self._bulb.isOn
        self._brightness = self._bulb.brightness
        self._color_temp = self._bulb.temperature
        self._hs_color = colorsys.rgb_to_hsv(
            self._bulb.red, self._bulb.green, self._bulb.blue
        )


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Beewi light platform."""
    mac_address = discovery_info.get("mac_address")
    add_entities([BeewiSmartLight(mac_address)])
