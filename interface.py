# talks to the CAN bus and gets the data from the sensors
import can
import platform
from serial.tools import list_ports

# get the list of available ports
def get_ports():
    ports = list_ports.comports()
    return [port.device for port in ports]


SENSOR_IDS = {
    0x151: "S1_A", 0x152: "S1_B",
    0x251: "S2_A", 0x252: "S2_B",
    0x351: "S3_A", 0x352: "S3_B",
    0x451: "S4_A", 0x452: "S4_B",
    0x551: "S5_A", 0x552: "S5_B",
    0x651: "S6_A", 0x652: "S6_B",
}

class Interface:
    def __init__(self, channel, bitrate=500000):
        self.channel = channel
        self.bitrate = bitrate

        # initialize the bus object
        bus = can.interface.Bus(
            bustype="slcan",
            channel=self.channel,
            bitrate=self.bitrate
        )

        self.bus = bus
        print(f"Connected to the CAN bus on {self.channel} at {self.bitrate}kbps successfully!!")

    # receive a message from the CAN bus
    def receive(self, timeout=1):
        msg = self.bus.recv(timeout=timeout)
        return msg
    
    def close(self):
        self.bus.shutdown()
        print("CAN bus connection closed.")
