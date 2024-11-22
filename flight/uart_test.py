import time

import board
import busio
import sdcardio
import storage
from hal.drivers.payload import PayloadUART

JET_UART_CTS = board.CLK1  # GPIO10
JET_UART_RX = board.JETSON_CS  # GPIO11
JET_UART_TX = board.MISO1  # GPIO08
JET_UART_RTS = board.MOSI1  # GPIO07
uart = busio.UART(JET_UART_TX, JET_UART_RX, baudrate=115200, timeout=0.1)

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
chunk_size = 254

with open(photo_path, "rb") as photo_file:
    total_bytes_sent = 0
    while True:
        chunk = photo_file.read(chunk_size)
        if not chunk:
            print("Photo sent successfully.")
            break
        crc = payload_uart.crc5(chunk)
        packet = chunk + bytes([crc])
        timeout = 0
        while True:
            payload_uart.write(packet)
            response = ""
            while response != b"ACK" and response != b"NAK":
                response = payload_uart.read(3)
            if response == b"ACK":
                total_bytes_sent += len(chunk)
                print(f"Total bytes sent: {total_bytes_sent}")
                break
            elif response == b"NAK":
                print("Resending chunk")
            time.sleep(0.01)
while response != b"EOT":
    payload_uart.write(b"EOT")
    response = payload_uart.read(3)
print("Photo transfer complete.")
