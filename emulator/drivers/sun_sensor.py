from hal.drivers.middleware.generic_driver import Driver


class LightSensor(Driver):
    def __init__(self, lux, id, simulator=None) -> None:
        self.__simulator = simulator
        self.__lux = lux
        self.__id = id
        super().__init__(None)

    def lux(self):
        if self.__simulator is not None:
            return self.__simulator.sun_lux()[self.__id]
        return self.__lux

    def run_diagnostics(self):
        return []

    def get_flags(self) -> dict:
        return {}


class LightSensorArray:
    def __init__(self, simulator=None) -> None:
        self.light_sensors = {
            "XP": LightSensor(4500, 0, simulator),
            "XM": LightSensor(48000, 1, simulator),
            "YP": LightSensor(85000, 2, simulator),
            "YM": LightSensor(0, 3, simulator),
            "ZM": LightSensor(0, 4, simulator),
        }

    def __getitem__(self, face):
        return self.light_sensors.get(face, None)
