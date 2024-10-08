from time import struct_time

from hal.drivers.middleware.generic_driver import Driver


class RTC(Driver):
    def __init__(self, date_input: struct_time) -> None:
        self.datetime = date_input
        super().__init__(None)

    def datetime(self):
        return self.datetime

    def set_datetime(self, date_input: struct_time):
        self.datetime = date_input

    def run_diagnostics(self):
        return []

    def get_flags(self) -> dict:
        return {}
