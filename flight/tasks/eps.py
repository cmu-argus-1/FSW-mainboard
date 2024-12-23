# Electrical Power Subsystem Task

import time

from apps.telemetry.constants import EPS_IDX
from core import DataHandler as DH
from core import TemplateTask
from core import state_manager as SM
from core.states import STATES
from hal.configuration import SATELLITE


class Task(TemplateTask):

    name = "EPS"
    ID = 0x01

    # To be removed - kept until proper logging is implemented
    """data_keys = [
        "TIME",
        "MAINBOARD_VOLTAGE",
        "MAINBOARD_CURRENT",
        "BATTERY_PACK_REPORTED_SOC",
        "BATTERY_PACK_REPORTED_CAPACITY",
        "BATTERY_PACK_CURRENT",
        "BATTERY_PACK_VOLTAGE",
        "BATTERY_PACK_MIDPOINT_VOLTAGE",
        "BATTERY_CYCLES",
        "BATTERY_PACK_TTE",
        "BATTERY_PACK_TTF",
        "BATTERY_TIME_SINCE_POWER_UP",
        "XP_COIL_VOLTAGE",
        "XP_COIL_CURRENT",
        "XM_COIL_VOLTAGE",
        "XM_COIL_CURRENT",
        "YP_COIL_VOLTAGE",
        "YP_COIL_CURRENT",
        "YM_COIL_VOLTAGE",
        "YM_COIL_CURRENT",
        "ZP_COIL_VOLTAGE",
        "ZP_COIL_CURRENT",
        "ZM_COIL_VOLTAGE",
        "ZM_COIL_CURRENT",
        "JETSON_INPUT_VOLTAGE",
        "JETSON_INPUT_CURRENT",
        "RF_LDO_OUTPUT_VOLTAGE",
        "RF_LDO_OUTPUT_CURRENT",
        "GPS_VOLTAGE",
        "GPS_CURRENT",
        "XP_SOLAR_CHARGE_VOLTAGE",
        "XP_SOLAR_CHARGE_CURRENT",
        "XM_SOLAR_CHARGE_VOLTAGE",
        "XM_SOLAR_CHARGE_CURRENT",
        "YP_SOLAR_CHARGE_VOLTAGE",
        "YP_SOLAR_CHARGE_CURRENT",
        "YM_SOLAR_CHARGE_VOLTAGE",
        "YM_SOLAR_CHARGE_CURRENT",
        "ZP_SOLAR_CHARGE_VOLTAGE",
        "ZP_SOLAR_CHARGE_CURRENT",
        "ZM_SOLAR_CHARGE_VOLTAGE",
        "ZM_SOLAR_CHARGE_CURRENT",
    ]"""

    log_data = [0] * 42  # - use mV for voltage and mA for current (h = short integer 2 bytes)

    def __init__(self, id):
        super().__init__(id)
        self.name = "EPS"

    def read_vc(self, sensor):
        return sensor.read_voltage_current() if sensor else (-1, -1)

    async def main_task(self):

        if SM.current_state == STATES.STARTUP:
            pass

        elif SM.current_state == STATES.NOMINAL:

            if not DH.data_process_exists("eps"):
                data_format = "Lhhb" + "h" * 38  # - use mV for voltage and mA for current (h = short integer 2 bytes)
                DH.register_data_process("eps", data_format, True, data_limit=100000)

            # Get power system readings

            (board_voltage, board_current) = self.read_vc(SATELLITE.BOARD_POWER_MONITOR)
            (jetson_voltage, jetson_current) = self.read_vc(SATELLITE.JETSON_POWER_MONITOR)

            self.log_data[EPS_IDX.TIME_EPS] = int(time.time())
            self.log_data[EPS_IDX.MAINBOARD_VOLTAGE] = int(board_voltage * 1000)  # mV - max 8.4V
            self.log_data[EPS_IDX.MAINBOARD_CURRENT] = int(board_current * 1000)  # mA
            self.log_data[EPS_IDX.JETSON_INPUT_VOLTAGE] = int(jetson_voltage * 1000)
            self.log_data[EPS_IDX.JETSON_INPUT_CURRENT] = int(jetson_current * 1000)

            DH.log_data("eps", self.log_data)
            self.log_info(
                f"Board Voltage: {self.log_data[EPS_IDX.MAINBOARD_VOLTAGE]} mV, "
                + f"Board Current: {self.log_data[EPS_IDX.MAINBOARD_CURRENT]} mA, "
                + f"Jetson Voltage: {self.log_data[EPS_IDX.JETSON_INPUT_VOLTAGE]} mV, "
                + f"Jetson Current: {self.log_data[EPS_IDX.JETSON_INPUT_CURRENT]} mA"
            )
