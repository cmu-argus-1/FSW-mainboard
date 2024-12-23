from hal.configuration import SATELLITE

# ---------- MAIN CODE STARTS HERE! ---------- ##

boot_errors = SATELLITE.boot_sequence()
print("ARGUS-1 booted.")
print(f"Boot Errors: {boot_errors}")

# # Board Power Monitor Test
# # while True:
# #     if SATELLITE.BOARD_POWER_MONITOR is not None:
# #         print(SATELLITE.BOARD_POWER_MONITOR.read_voltage_current())

# # charger test
# # while True:
# #     if SATELLITE.CHARGER is not None:
# #         print(SATELLITE.CHARGER.charger_status1())

# imu test
# while True:
#     if SATELLITE.IMU is not None:
#         print(SATELLITE.IMU.gyro())

# rtc test
# while True:
#    if SATELLITE.RTC is not None:
#        print(SATELLITE.RTC.datetime())
