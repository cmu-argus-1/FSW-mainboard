"""

GPS Module from the Communications Subsystem.

This module is responsible for handling the GPS receiver (SkyTraq Orion-B16 GNSS receiver).
The GPS receiver provides the satellite's position and velocity in ECEF coordinates.

"""
import struct


class GPS:
    # Mock data for message ID 0xA8 (NAVIGATION DATA MESSAGE)
    _MOCK_DATA = (
        b"\xa0\xa1\x00\x3b\xa8\x02\x07\x08\x6a\x03\x21\x7a\x1f\x1b\x1f\x16\xf1\xb6\xe1"
        b"\x3c\x1c\x00\x00\x0f\x6f\x00\x00\x17\xb7\x01\x0d\x00\xe4\x00\x7e\x00\xbd\x00"
        b"\x8f\xf1\x97\x18\xd2\xe9\x88\x7d\x90\x1a\xfb\x26\xf7\x03\xF5\x09\xFE\x01\x79"
        b"\x7C\x4A\xFB\x9B\xA8\x40\x68\x0d\x0a"
    )

    # Message fields for latest message
    _payload_len = 0
    _msg_id = 0
    _msg_cs = 0

    # Payload for latest message 
    _payload = bytearray([0]*58)

    # Navigation data tuple 
    _nav_data = (0,) * 19

    @classmethod
    def read(self):
        """
        Read incoming message from GNSS receiver, get
        message metadata and payload. 

        Format:
            [0xA0A1][PL][ID][P][CS][0x0D0A]
            PL = Payload Length
            ID = Message ID
            P  = Payload
            CS = Checksum
        """

        # TODO: Driver communicates with GPS module and 
        msg = self._MOCK_DATA

        # Check packet validity 
        if(len(msg) <= 7):
            raise RuntimeError("Message length too short")

        if((msg[0] != 0xA0) or (msg[1] != 0xA1)):
            raise RuntimeError("Invalid message")

        if((msg[-2] != 0x0D) or (msg[-1] != 0x0A)):
            raise RuntimeError("Invalid message")

        # Get PL, ID, and CS
        self._payload_len = ((msg[2] & 0xFF) << 8) | msg[3]
        self._msg_id = msg[4]
        self.__msg_cs = msg[-3]

        # Get payload
        self._payload = msg[4 : -3]

    @classmethod
    def decode_nav_data(self):
        """
        Decode data in NMEA format from GPS navigation data
        message. 

        Navigation data is message 0xA8 from GNSS receiver.
        """
        self._nav_data = struct.unpack(">3BHI2i2I5H6i", self._payload)
    
    @classmethod
    def get_nav_data(self) -> tuple:
        """
        Returns navigation data tuple in ordering of NMEA format
        """

        # Read message 
        self.read()

        # If message is nav data, decode message, else skip 
        if(self._msg_id == 0xA8 and self._payload_len == 59):
            self.decode_nav_data()

        # Return current nav_data
        return self._nav_data