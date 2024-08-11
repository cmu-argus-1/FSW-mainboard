# Index constants for accessing data in the Data Handler

from micropython import const


class EPS_IDX:
    TIME = const(0)
    MAINBOARD_VOLTAGE = const(1)
    MAINBOARD_CURRENT = const(2)
    BATTERY_PACK_SOC = const(3)
    BATTERY_PACK_REMAINING_CAPACITY_PERC = const(4)
    BATTERY_PACK_CURRENT = const(5)
    BATTERY_PACK_VOLTAGE = const(6)
    BATTERY_PACK_MIDPOINT_VOLTAGE = const(7)
    BATTERY_CYCLES = const(8)
    BATTERY_PACK_TTE = const(9)
    BATTERY_PACK_TTF = const(10)
    BATTERY_TIME_SINCE_POWER_UP = const(11)
    XP_COIL_VOLTAGE = const(12)
    XP_COIL_CURRENT = const(13)
    XM_COIL_VOLTAGE = const(14)
    XM_COIL_CURRENT = const(15)
    YP_COIL_VOLTAGE = const(16)
    YP_COIL_CURRENT = const(17)
    YM_COIL_VOLTAGE = const(18)
    YM_COIL_CURRENT = const(19)
    ZP_COIL_VOLTAGE = const(20)
    ZP_COIL_CURRENT = const(21)
    ZM_COIL_VOLTAGE = const(22)
    ZM_COIL_CURRENT = const(23)
    JETSON_INPUT_VOLTAGE = const(24)
    JETSON_INPUT_CURRENT = const(25)
    RF_LDO_OUTPUT_VOLTAGE = const(26)
    RF_LDO_OUTPUT_CURRENT = const(27)
    GPS_VOLTAGE = const(28)
    GPS_CURRENT = const(29)
    XP_SOLAR_CHARGE_VOLTAGE = const(30)
    XP_SOLAR_CHARGE_CURRENT = const(31)
    XM_SOLAR_CHARGE_VOLTAGE = const(32)
    XM_SOLAR_CHARGE_CURRENT = const(33)
    YP_SOLAR_CHARGE_VOLTAGE = const(34)
    YP_SOLAR_CHARGE_CURRENT = const(35)
    YM_SOLAR_CHARGE_VOLTAGE = const(36)
    YM_SOLAR_CHARGE_CURRENT = const(37)
    ZP_SOLAR_CHARGE_VOLTAGE = const(38)
    ZP_SOLAR_CHARGE_CURRENT = const(39)
    ZM_SOLAR_CHARGE_VOLTAGE = const(40)
    ZM_SOLAR_CHARGE_CURRENT = const(41)


class CDH_IDX:
    TIME = const(0)
    SC_STATE = const(1)
    SD_AVAILABLE_STORAGE = const(2)
    CURRENT_RAM_USAGE = const(3)
    REBOOT_COUNT = const(4)
    WATCHDOG_TIMER = const(5)
    HAL_BITFLAGS = const(6)
    COMMUNICATION_STATUS = const(7)
    ADCS_STATUS = const(8)
    EPS_STATUS = const(9)


class ADCS_IDX:
    TIME = const(0)
    ADCS_STATUS = const(1)
    GYRO_X = const(2)
    GYRO_Y = const(3)
    GYRO_Z = const(4)
    MAG_X = const(5)
    MAG_Y = const(6)
    MAG_Z = const(7)
    SUN_VEC_X = const(8)
    SUN_VEC_Y = const(9)
    SUN_VEC_Z = const(10)
    ECLIPSE = const(11)
    LIGHT_SENSOR_XP = const(12)
    LIGHT_SENSOR_XM = const(13)
    LIGHT_SENSOR_YP = const(14)
    LIGHT_SENSOR_YM = const(15)
    LIGHT_SENSOR_ZP1 = const(16)
    LIGHT_SENSOR_ZP2 = const(17)
    LIGHT_SENSOR_ZP3 = const(18)
    LIGHT_SENSOR_ZP4 = const(19)
    LIGHT_SENSOR_ZM = const(20)
    XP_COIL_STATUS = const(21)
    XM_COIL_STATUS = const(22)
    YP_COIL_STATUS = const(23)
    YM_COIL_STATUS = const(24)
    ZP_COIL_STATUS = const(25)
    ZM_COIL_STATUS = const(26)
    COARSE_ATTITUDE_QW = const(27)
    COARSE_ATTITUDE_QX = const(28)
    COARSE_ATTITUDE_QY = const(29)
    COARSE_ATTITUDE_QZ = const(30)
    STAR_TRACKER_STATUS = const(31)
    STAR_TRACKER_ATTITUDE_QW = const(32)
    STAR_TRACKER_ATTITUDE_QX = const(33)
    STAR_TRACKER_ATTITUDE_QY = const(34)
    STAR_TRACKER_ATTITUDE_QZ = const(35)


class SUN_IDX:
    TIME = const(0)
    STATUS = const(1)
    X = const(2)
    Y = const(3)
    Z = const(4)
    ECLIPSE = const(5)


class IMU_IDX:
    TIME = const(0)
    ACCEL_X = const(1)
    ACCEL_Y = const(2)
    ACCEL_Z = const(3)
    MAG_X = const(4)
    MAG_Y = const(5)
    MAG_Z = const(6)
    GYRO_X = const(7)
    GYRO_Y = const(8)
    GYRO_Z = const(9)


class GPS_IDX:
    TIME = const(0)
    GPS_MESSAGE_ID = const(1)
    GPS_FIX_MODE = const(2)
    GPS_NUMBER_OF_SV = const(3)
    GPS_GNSS_WEEK = const(4)
    GPS_GNSS_TOW = const(5)
    GPS_LATITUDE = const(6)
    GPS_LONGITUDE = const(7)
    GPS_ELLIPSOID_ALT = const(8)
    GPS_MEAN_SEA_LVL_ALT = const(9)
    GPS_GDOP = const(10)
    GPS_PDOP = const(11)
    GPS_HDOP = const(12)
    GPS_VDOP = const(13)
    GPS_TDOP = const(14)
    GPS_ECEF_X = const(15)
    GPS_ECEF_Y = const(16)
    GPS_ECEF_Z = const(17)
    GPS_ECEF_VX = const(18)
    GPS_ECEF_VY = const(19)
    GPS_ECEF_VZ = const(20)


class THERMAL_IDX:
    TIME = const(0)
    IMU_TEMPERATURE = const(1)
    CPU_TEMPERATURE = const(2)
    BATTERY_PACK_TEMPERATURE = const(3)
