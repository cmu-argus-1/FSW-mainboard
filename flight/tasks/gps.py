# GPS Task

import time

from apps.telemetry.constants import GPS_IDX
from apps.gps import GPS
from core import TemplateTask
from core import state_manager as SM
from core.data_handler import DataHandler as DH
from core.states import STATES


class Task(TemplateTask):

    data_keys = [
        "TIME",
        "GPS_MESSAGE_ID",
        "GPS_FIX_MODE",
        "GPS_NUMBER_OF_SV",
        "GPS_GNSS_WEEK",
        "GPS_GNSS_TOW",  # Time of week
        "GPS_LATITUDE",
        "GPS_LONGITUDE",
        "GPS_ELLIPSOID_ALT",
        "GPS_MEAN_SEA_LVL_ALT",
        "GPS_GDOP",
        "GPS_PDOP",
        "GPS_HDOP",
        "GPS_VDOP",
        "GPS_TDOP",
        "GPS_ECEF_X",
        "GPS_ECEF_Y",
        "GPS_ECEF_Z",
        "GPS_ECEF_VX",
        "GPS_ECEF_VY",
        "GPS_ECEF_VZ",
    ]

    data_format = "LBBBHIiiiiHHHHHiiiiii"
    log_data = [0] * 21

    async def main_task(self):

        if SM.current_state == STATES.STARTUP:
            pass
        elif SM.current_state == STATES.NOMINAL:
            if not DH.data_process_exists("gps"):
                DH.register_data_process("gps", self.data_keys, self.data_format, True, line_limit=500)

            # TODO GPS frame parsing - get ECEF in (cm) and ECEF velocity in cm/s
            nav_data = GPS.get_nav_data()

            self.log_data[GPS_IDX.TIME_GPS] = int(time.time())
            self.log_data[GPS_IDX.GPS_MESSAGE_ID] = nav_data[0]
            self.log_data[GPS_IDX.GPS_FIX_MODE] = nav_data[1]
            self.log_data[GPS_IDX.GPS_NUMBER_OF_SV] = nav_data[2]
            self.log_data[GPS_IDX.GPS_GNSS_WEEK] = nav_data[3]
            self.log_data[GPS_IDX.GPS_GNSS_TOW] = nav_data[4]
            self.log_data[GPS_IDX.GPS_LATITUDE] = nav_data[5]
            self.log_data[GPS_IDX.GPS_LONGITUDE] = nav_data[6]
            self.log_data[GPS_IDX.GPS_ELLIPSOID_ALT] = nav_data[7]
            self.log_data[GPS_IDX.GPS_MEAN_SEA_LVL_ALT] = nav_data[8]
            self.log_data[GPS_IDX.GPS_GDOP] = nav_data[9]
            self.log_data[GPS_IDX.GPS_PDOP] = nav_data[10]
            self.log_data[GPS_IDX.GPS_HDOP] = nav_data[11]
            self.log_data[GPS_IDX.GPS_VDOP] = nav_data[12]
            self.log_data[GPS_IDX.GPS_TDOP] = nav_data[13]
            self.log_data[GPS_IDX.GPS_ECEF_X] = nav_data[14] # cm
            self.log_data[GPS_IDX.GPS_ECEF_Y] = nav_data[15] # cm   
            self.log_data[GPS_IDX.GPS_ECEF_Z] = nav_data[16] # cm
            self.log_data[GPS_IDX.GPS_ECEF_VX] = nav_data[17] # cm/s
            self.log_data[GPS_IDX.GPS_ECEF_VY] = nav_data[18] # cm/s
            self.log_data[GPS_IDX.GPS_ECEF_VZ] = nav_data[19] # cm/s

        DH.log_data("gps", self.log_data)
        self.log_info(f"{dict(zip(self.data_keys[-6:], self.log_data[-6:]))}")
