# Sun Vector Tasks

import time

from apps.sun import read_light_sensors, compute_body_sun_vector, in_eclipse
from core import TemplateTask
from core import state_manager as SM
from core.data_handler import DataHandler as DH
from hal.configuration import SATELLITE


class Task(TemplateTask):

    name = "SUN"
    ID = 0x11

    data_keys = ["time", "status", "x", "y", "z", "eclipse"]

    # Fake starting sun vector
    status = False
    sun_vector = [1, 0, 0]
    eclipse_state = False

    async def main_task(self):

        if SM.current_state == "NOMINAL":

            if not DH.data_process_exists("sun"):
                DH.register_data_process(
                    "sun", self.data_keys, "fbfffb", True, line_limit=50
                )

            # Access Sun Sensor Readings - Satellite must return the array directly
            lux_readings = read_light_sensors()


            self.status, self.sun_vector = compute_body_sun_vector(lux_readings)
            self.eclipse_state = in_eclipse(lux_readings)

            readings = {
                "time": time.time(),
                "status": self.status,
                "x": self.sun_vector[0],
                "y": self.sun_vector[1],
                "z": self.sun_vector[2],
                "eclipse": self.eclipse_state,
            }

            DH.log_data("sun", readings)
            print(f"[{self.ID}][{self.name}] Data: {readings}")
