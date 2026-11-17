from homeassistant.components.climate.const import HVACMode
from homeassistant.const import UnitOfTemperature

from ..const import ROTENSO_ELIS_PAYLOAD
from ..helpers import assert_device_properties_set
from .base_device_tests import TuyaDeviceTestCase

POWER_DPS = "1"
TEMPERATURE_DPS = "2"
CURRENTTEMP_DPS = "3"
MODE_DPS = "4"
FAN_DPS = "5"


class TestRotensoElisAircon(TuyaDeviceTestCase):
    __test__ = True

    def setUp(self):
        self.setUpForConfig("rotenso_elis_aircon.yaml", ROTENSO_ELIS_PAYLOAD)
        self.subject = self.entities.get("climate")

    def test_temperature_unit_returns_celsius(self):
        self.assertEqual(self.subject.temperature_unit, UnitOfTemperature.CELSIUS)

    def test_target_temperature(self):
        self.assertEqual(self.subject.target_temperature, 26.0)

    def test_current_temperature(self):
        self.assertEqual(self.subject.current_temperature, 24.0)

    def test_hvac_mode(self):
        self.assertEqual(self.subject.hvac_mode, HVACMode.COOL)
        self.dps[MODE_DPS] = "4"
        self.assertEqual(self.subject.hvac_mode, HVACMode.HEAT)
        self.dps[POWER_DPS] = False
        self.assertEqual(self.subject.hvac_mode, HVACMode.OFF)

    async def test_set_hvac_mode_cool(self):
        async with assert_device_properties_set(
            self.subject._device,
            {POWER_DPS: True, MODE_DPS: "1"},
        ):
            await self.subject.async_set_hvac_mode(HVACMode.COOL)

    async def test_turn_off(self):
        async with assert_device_properties_set(
            self.subject._device, {POWER_DPS: False}
        ):
            await self.subject.async_set_hvac_mode(HVACMode.OFF)

    async def test_set_target_temperature(self):
        async with assert_device_properties_set(
            self.subject._device, {TEMPERATURE_DPS: 2250}
        ):
            await self.subject.async_set_target_temperature(22.5)

    def test_fan_mode(self):
        self.assertEqual(self.subject.fan_mode, "auto")
        self.dps[FAN_DPS] = "7"
        self.assertEqual(self.subject.fan_mode, "turbo")
