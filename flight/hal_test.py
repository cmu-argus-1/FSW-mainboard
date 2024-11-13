import time

from hal.configuration import SATELLITE

# ---------- MAIN CODE STARTS HERE! ---------- ##

boot_errors = SATELLITE.boot_sequence()
print("ARGUS-1 booted.")
print(f"Boot Errors: {boot_errors}")

# SPDX-FileCopyrightText: 2020 Bryan Siepert, written for Adafruit Industries

# SPDX-License-Identifier: Unlicense


# Board Power Monitor Test
# while True:
#     if SATELLITE.POWER_MONITORS != {}:
#         for key in SATELLITE.POWER_MONITORS:
#             print(SATELLITE.POWER_MONITORS[key].read_voltage_current())

# charger test
# while True:
#     if SATELLITE.CHARGER is not None:
#         print(SATELLITE.CHARGER.charger_status1())

# imu test
# while True:
#     if SATELLITE.IMU is not None:
#         print(SATELLITE.IMU.gyro())

# rtc test
# SATELLITE.RTC.datetime = time.struct_time((2024, 11, 12, 18, 37, 0, 1, 304, -1))
while True:
    if SATELLITE.RTC is not None:
        print(SATELLITE.RTC.datetime)
        time.sleep(10)
