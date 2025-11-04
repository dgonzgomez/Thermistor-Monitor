# talks to the CAN bus and gets the data from the sensors
import can

SENSOR_IDS = {
    0x151: "S1_A", 0x152: "S1_B",
    0x251: "S2_A", 0x252: "S2_B",
    0x351: "S3_A", 0x352: "S3_B",
    0x451: "S4_A", 0x452: "S4_B",
    0x551: "S5_A", 0x552: "S5_B",
    0x651: "S6_A", 0x652: "S6_B",
}

canif.recv()

class Interface:
    def __init__(self):
        # i gotta adjust these to the actual hardware later
        self.bus_type = "socketcan"
        self.channel = "COM1"
        self.bitrate = 500000

        # initialize the bus object
        self.bus = can.interface.Bus(
            bustype=self.bus_type,
            channel=self.channel,
            bitrate=self.bitrate
        )

        print(f"Connected to the CAN bus on {self.channel} at {self.bitrate}kbps successfully!!")

    # receive a message from the CAN bus
    def receive(self):
        msg = self.bus.recv(timeout=1)
        return msg