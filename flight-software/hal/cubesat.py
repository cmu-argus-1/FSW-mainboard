import board
import time
import digitalio

from bitflags import bitFlag, multiBitFlag 
from micropython import const
from drivers.diagnostics import Diagnostics

# NVM register numbers
_BOOTCNT  = const(0)
_VBUSRST  = const(6)
_STATECNT = const(7)
_TOUTS    = const(9)
_GSRSP    = const(10)
_ICHRG    = const(11)
_FLAG     = const(16)

class CubeSat:
    # General NVM counters
    c_boot      = multiBitFlag(register=_BOOTCNT, lowest_bit=0,num_bits=8)
    c_vbusrst   = multiBitFlag(register=_VBUSRST, lowest_bit=0,num_bits=8)
    c_state_err = multiBitFlag(register=_STATECNT,lowest_bit=0,num_bits=8)
    c_gs_resp   = multiBitFlag(register=_GSRSP,   lowest_bit=0,num_bits=8)
    c_ichrg     = multiBitFlag(register=_ICHRG,   lowest_bit=0,num_bits=8)

    # Define NVM flags
    f_lowbatt  = bitFlag(register=_FLAG,bit=0)
    f_solar    = bitFlag(register=_FLAG,bit=1)
    f_gpson    = bitFlag(register=_FLAG,bit=2)
    f_lowbtout = bitFlag(register=_FLAG,bit=3)
    f_gpsfix   = bitFlag(register=_FLAG,bit=4)
    f_shtdwn   = bitFlag(register=_FLAG,bit=5)

    instance = None

    def __new__(cls):
        """
        Override to ensure this class has only one instance.
        """
        if not cls.instance:
            cls.instance = object.__new__(cls)
            cls.instance = super(CubeSat, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        # List of successfully initialized devices
        self._device_list: list[Diagnostics] = []

        # List of errors from most recent system diagnostic test
        self._recent_errors: list[int] = [Diagnostics.NOERROR]
        
        # Interfaces
        self._uart1 = None
        self._uart2 = None
        self._spi = None
        self._i2c1 = None
        self._i2c2 = None

        # Devices
        self._gps = None
        self._battery_monitor = None
        self._jetson_monitor = None
        self._imu = None
        self._charger = None
        self._torque_xp = None
        self._torque_xm = None
        self._torque_yp = None
        self._torque_ym = None
        self._torque_z = None
        self._sun_sensor_xp = None
        self._sun_sensor_xm = None
        self._sun_sensor_yp = None
        self._sun_sensor_ym = None
        self._sun_sensor_zp = None
        self._sun_sensor_zm = None
        self._rtc = None
        self._radio = None
        self._sd_card = None
        self._burn_wires = None

        # Debugging
        self._neopixel = None
    
    ## ABSTRACT METHOD ##
    def boot_sequence(self) -> None:
        """boot_sequence: Boot sequence for the CubeSat.
        """
        raise NotImplementedError("CubeSats must implement boot method")
    
    ## ABSTRACT METHOD ##
    def run_system_diagnostics(self) -> list[int] | None:
        """run_diagnostic_test: Run all tests for the component
        """
        raise NotImplementedError("CubeSats must implement diagnostics method")
    
    def get_recent_errors(self) -> list[int]:
        """get_recent_errors: Get the most recent errors from the system
        """
        return self._recent_errors
    
    ######################### INTERFACES #########################
    
    @property
    def UART1(self):
        """UART: Returns the UART object
        """
        return self._uart1
    
    @property
    def UART2(self):
        """UART2: Returns the UART2 object
        """
        return self._uart2
    
    @property
    def SPI(self):
        """SPI: Returns the SPI object
        """
        return self._spi
    
    @property
    def I2C1(self):
        """I2C: Returns the I2C object
        """
        return self._i2c1
    
    @property
    def I2C2(self):
        """I2C2: Returns the I2C2 object
        """
        return self._i2c2
    
    ######################### DEVICES #########################

    @property
    def GPS(self):
        """GPS: Returns the gps object
        """
        return self._gps
    
    @property
    def BATTERY_POWER_MONITOR(self):
        """BATTERY_POWER_MONITOR: Returns the battery power monitor object
        """
        return self._battery_monitor
    
    @property
    def JETSON_POWER_MONITOR(self):
        """JETSON_MONITOR: Returns the Jetson monitor object
        """
        return self._jetson_monitor
    
    @property
    def IMU(self):
        """IMU: Returns the IMU object
        """
        return self._imu
    
    @property
    def CHARGER(self):
        """CHARGER: Returns the charger object
        """
        return self._charger
    
    @property
    def TORQUE_XP(self):
        """TORQUE_XP: Returns the torque driver in the x+ direction
        """
        return self._torque_xp
    
    @property
    def TORQUE_XM(self):
        """TORQUE_XM: Returns the torque driver in the x- direction
        """
        return self._torque_xm
    
    @property
    def TORQUE_YP(self):
        """TORQUE_YP: Returns the torque driver in the y+ direction
        """
        return self._torque_yp
    
    @property
    def TORQUE_YM(self):
        """TORQUE_YM: Returns the torque driver in the y- direction
        """
        return self._torque_ym
    
    @property
    def TORQUE_Z(self):
        """TORQUE_Z: Returns the torque driver in the z direction
        """
        return self._torque_z
    
    @property
    def SUN_SENSOR_XP(self):
        """SUN_SENSOR_XP: Returns the sun sensor in the x+ direction
        """
        return self._sun_sensor_xp
    
    @property
    def SUN_SENSOR_XM(self):
        """SUN_SENSOR_XM: Returns the sun sensor in the x- direction
        """
        return self._sun_sensor_xm
    
    @property
    def SUN_SENSOR_YP(self):
        """SUN_SENSOR_YP: Returns the sun sensor in the y+ direction
        """
        return self._sun_sensor_yp
    
    @property
    def SUN_SENSOR_YM(self):
        """SUN_SENSOR_YM: Returns the sun sensor in the y- direction
        """
        return self._sun_sensor_ym
    
    @property
    def SUN_SENSOR_ZP(self):
        """SUN_SENSOR_ZP: Returns the sun sensor in the z+ direction
        """
        return self._sun_sensor_zp
    
    @property
    def SUN_SENSOR_ZM(self):
        """SUN_SENSOR_ZM: Returns the sun sensor in the z- direction
        """
        return self._sun_sensor_zm
    
    @property
    def RTC(self):
        """RTC: Returns the RTC object
        """
        return self._rtc
    
    @property
    def RADIO(self):
        """RADIO: Returns the radio object
        """
        return self._radio
    
    @property
    def NEOPIXEL(self):
        """NEOPIXEL: Returns the neopixel object
        """
        return self._neopixel
    
    @property
    def BURN_WIRES(self):
        """BURN_WIRES: Returns the burn wire object
        """
        return self._burn_wires