import time

# import circuitpython_csv as csv

# from hal.configuration import SATELLITE

# ---------- MAIN CODE STARTS HERE! ---------- ##

# boot_errors = SATELLITE.boot_sequence()
# print("ARGUS-2 booted.")
# print(f"Boot Errors: {boot_errors}")
import board
import busio
import sdcardio
import storage
from hal.drivers.payload import PayloadUART

# Initialize UART
JET_UART_CTS = board.CLK1  # GPIO10
JET_UART_RX = board.JETSON_CS  # GPIO11
JET_UART_TX = board.MISO1  # GPIO08
JET_UART_RTS = board.MOSI1  # GPIO07
uart = busio.UART(JET_UART_TX, JET_UART_RX, baudrate=921600, timeout=0.1)

# Initialize SD card (assuming the photo is stored on an SD card)
SPI_SCK = board.CLK0  # GPIO18
SPI_MOSI = board.MOSI0  # GPIO19
SPI_MISO = board.MISO0  # GPIO16
SPI = busio.SPI(SPI_SCK, MOSI=SPI_MOSI, MISO=SPI_MISO)
SD_CARD_CS = board.SD_CS  # GPIO26_ADC0

sdcard = sdcardio.SDCard(SPI, SD_CARD_CS)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")


payload_uart = PayloadUART(uart)


# Read photo from SD card
photo_path = "/sd/image.png"
chunk_size = 255  # Size of each chunk to send

with open(photo_path, "rb") as photo_file:
    total_bytes_sent = 0
    while True:
        chunk = photo_file.read(chunk_size)
        if not chunk:
            break
        checksum = payload_uart.checksum(chunk)
        packet = chunk + bytes([checksum])
        while True:
            payload_uart.write(packet)
            response = ""
            while response != b"ACK" and response != b"NAK":
                response = payload_uart.read(3)
            print(f"Response: {response}")
            if response == b"ACK":
                total_bytes_sent += len(chunk)
                print(f"Total bytes sent: {total_bytes_sent}")
                break
            elif response == b"NAK":
                print("Resending chunk")
            time.sleep(0.1)  # Small delay to ensure data is sent

print("Photo sent successfully.")
# import board
# import busio

# # Initialize UART
# JET_UART_CTS = board.CLK1  # GPIO10
# JET_UART_RX = board.JETSON_CS  # GPIO11
# JET_UART_TX = board.MISO1  # GPIO08
# JET_UART_RTS = board.MOSI1  # GPIO07
# uart = busio.UART(JET_UART_TX, JET_UART_RX, baudrate=961600, timeout=0.1)


# def uart_send(data):
#     uart.write(data.encode("utf-8"))


# def uart_receive():
#     if uart.in_waiting > 0:
#         return uart.read(uart.in_waiting).decode("utf-8")
#     return None


# # Main loop to send and receive data
# try:
#     while True:
#         # Send data to the Jetson
#         send_data = "Hello from RP2040"
#         uart_send(send_data)
#         print(f"Sent: {send_data}")

#         # Wait for a short period before checking for received data
#         time.sleep(1)

#         # Receive data from the Jetson
#         received_data = uart_receive()
#         if received_data:
#             print(f"Received: {received_data}")

#         # Wait for a short period before the next transfer
#         time.sleep(1)

# except KeyboardInterrupt:
#     print("UART communication stopped.")

## IMU Data Logging

# if SATELLITE.IMU is None:
#     raise RuntimeError("IMU not initialized")

# last_time = time.monotonic_ns()
# with open("/sd/imu_data.csv", mode="w") as file:
#     writer = csv.writer(file)
#     writer.writerow(["Time", "Gyro_X", "Gyro_Y", "Gyro_Z"])
#     while True:
#         if SATELLITE.IMU is not None:
#             # Get the current time
#             current_time = time.monotonic_ns()

#             # Read the gyro data
#             gyro_x, gyro_y, gyro_z = SATELLITE.IMU.gyro()

#             # Write the data to the CSV file
#             writer.writerow([current_time, gyro_x, gyro_y, gyro_z])
#             print(f"Time: {current_time}, Gyro_X: {gyro_x}, Gyro_Y: {gyro_y}, Gyro_Z: {gyro_z}")

#             if current_time - last_time > 60000000000:
#                 file.flush()
#                 last_time = current_time

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
# while True:
#     if SATELLITE.RTC is not None:
#         print(SATELLITE.RTC.datetime)
#         time.sleep(10)

# import digitalio
# import board

# RADIO_CS = digitalio.DigitalInOut(board.LORA_CS)  # GPIO17
# RADIO_RESET = digitalio.DigitalInOut(board.LORA_nRST)  # GPIO21
# RADIO_ENABLE = digitalio.DigitalInOut(board.LORA_EN)  # GPIO28_ADC2
# RADIO_TX_EN = digitalio.DigitalInOut(board.LORA_TX_EN)  # GPIO22
# RADIO_RX_EN = digitalio.DigitalInOut(board.LORA_RX_EN)  # GPIO20
# RADIO_BUSY = digitalio.DigitalInOut(board.LORA_BUSY)  # GPIO23
# RADIO_IRQ = digitalio.DigitalInOut(board.GPS_EN)  # GPIO27_ADC1

# RADIO_CS.direction = digitalio.Direction.OUTPUT
# RADIO_RESET.direction = digitalio.Direction.OUTPUT
# RADIO_ENABLE.direction = digitalio.Direction.OUTPUT
# RADIO_TX_EN.direction = digitalio.Direction.OUTPUT
# RADIO_RX_EN.direction = digitalio.Direction.OUTPUT
# RADIO_BUSY.direction = digitalio.Direction.OUTPUT
# RADIO_IRQ.direction = digitalio.Direction.OUTPUT

# while True:
#     cs.value = True
#     SPI_SCK.value = True
#     SPI_MOSI.value = True
#     SPI_MISO.value = True

#     RADIO_CS.value = True
#     RADIO_RESET.value = True
#     RADIO_ENABLE.value = True
#     RADIO_TX_EN.value = True
#     RADIO_RX_EN.value = True
#     RADIO_BUSY.value = True
#     RADIO_IRQ.value = True
