"""
Payload: Payload uart driver for the ARGUS-1 CubeSat

This module provides a driver for the payload uart on the ARGUS-1 CubeSat. The
payload uart is used to communicate with the payload board. The driver provides
methods to send and receive data over the uart.

Author(s): Harry Rosmann
"""

from digitalio import DigitalInOut
from hal.drivers.middleware.errors import Errors
from hal.drivers.middleware.generic_driver import Driver


class PayloadUART(Driver):
    """Payload: Payload uart driver for the ARGUS-1 CubeSat"""

    def __init__(self, uart, enable_pin=None):
        self.__uart = uart

        if enable_pin is not None:
            self.__enable = DigitalInOut(enable_pin)
            self.__enable.switch_to_output(value=True)
        else:
            self.__enable = None

        super().__init__(self.__enable)

    def write(self, bytes: bytearray) -> None:
        self.__uart.write(bytes)

    def read(self, num_bytes: int) -> bytearray:
        return self.__uart.read(num_bytes)

    def in_waiting(self) -> int:
        return self.__uart.in_waiting

    def reset_input_buffer(self) -> None:
        self.__uart.reset_input_buffer()

    def crc5(self, data):
        crc = 0x1F
        polynomial = 0x05

        for byte in data:
            crc ^= byte
            for _ in range(8):
                if crc & 0x10:
                    crc = (crc << 1) ^ polynomial
                else:
                    crc <<= 1
                crc &= 0x1F

        return crc

    """
    ----------------------- HANDLER METHODS -----------------------
    """

    def get_flags(self):
        return {}

    def run_diagnostics(self) -> list[int] | None:
        """run_diagnostic_test: Run all tests for the component"""
        return [Errors.NOERROR]
