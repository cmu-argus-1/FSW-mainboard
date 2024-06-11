"""
jetson_comms.py 
================
Task to interact with Jetson over UART
"""

import gc
import struct
import sys
import time

from apps.data_handler import DataHandler as DH
from apps.jetson_comms.argus_comm import *
from apps.jetson_comms.message_id import *

# PyCubed Board Lib
from hal.configuration import SATELLITE

# State manager and OBDH
from state_manager import state_manager as SM

# Template task from taskio
from tasks.template_task import DebugTask


class Task(DebugTask):

    name = "JETSON"
    ID = 0x13

    argus_comms = ArgusComm(SATELLITE.PAYLOADUART)

    data_keys = [
        "ram",
        "disk",
        "cpu_temp",
        "gpu_temp",
    ]

    async def main_task(self):
        # Only communicate if SAT in NOMINAL state
        if SM.current_state == "NOMINAL":
            if DH.data_process_exists("jetson") == False:
                DH.register_data_process(
                    "jetson", self.data_keys, "ffff", True, line_limit=40
                )

            # Register image process
            if DH.data_process_exists("img") == False:
                DH.register_image_process()

            # Ask Jetson for image
            print(f"[{self.ID}][{self.name}] Requesting Jetson for image")
            # msg = Message(TRANSMIT_IMAGE, struct.pack(b, 0))

            # Wait for Jetson comms for 0.1s
            if self.argus_comms.receive_message() == False:
                # No message received
                print(
                    f"[{self.ID}][{self.name}] No message received from Jetson"
                )

            # Image received successfully
            else:
                DH.image_completed()
                print(
                    f"[{self.ID}][{self.name}] Image successfully received from Jetson"
                )