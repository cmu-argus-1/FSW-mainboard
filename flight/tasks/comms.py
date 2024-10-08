# Communication task which uses the radio to transmit and receive messages.

from apps.comms.rf_mcu import SATELLITE_RADIO
from apps.telemetry import TelemetryPacker
from core import TemplateTask
from core import state_manager as SM
from core.states import STATES


class Task(TemplateTask):
    tx_msg_id = 0x00
    rq_msg_id = 0x00

    frequency_set = False
    TX_heartbeat_frequency = 0.2  # 5 seconds

    def __init__(self, id):
        super().__init__(id)
        self.name = "COMMS"
        self.TX_COUNT_THRESHOLD = 0
        self.TX_COUNTER = 0

        SATELLITE_RADIO.listen()  # RX mode

    async def main_task(self):

        if not self.frequency_set:
            self.TX_COUNTER = 0
            if self.TX_heartbeat_frequency > self.frequency:
                self.log_error("TX heartbeat frequency faster than task frequency")
            self.TX_COUNT_THRESHOLD = int(self.frequency / self.TX_heartbeat_frequency)
            self.frequency_set = True

        if SM.current_state == STATES.NOMINAL:

            self.TX_COUNTER += 1

            if self.TX_COUNTER >= self.TX_COUNT_THRESHOLD:

                if TelemetryPacker.TM_AVAILABLE:
                    SATELLITE_RADIO.tm_frame = TelemetryPacker.FRAME()

                self.tx_msg_id = SATELLITE_RADIO.transmit_message()
                self.log_info(f"Sent message with ID: {self.tx_msg_id}")
                self.TX_COUNTER = 0

                SATELLITE_RADIO.listen()  # RX mode

            # self.log_info(f"data here?: {SATELLITE_RADIO.data_available()}")
            if SATELLITE_RADIO.data_available():
                self.rq_msg_id = SATELLITE_RADIO.receive_message()
                if self.rq_msg_id != 0x00:
                    self.log_info(f"GS requested message ID: {self.rq_msg_id}")
                else:
                    self.log_info("No response from GS")
