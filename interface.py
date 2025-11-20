# talks to the CAN bus and gets the data from the sensors
import can
import platform

SENSOR_IDS = {
    0x151: "S1_A", 0x152: "S1_B",
    0x251: "S2_A", 0x252: "S2_B",
    0x351: "S3_A", 0x352: "S3_B",
    0x451: "S4_A", 0x452: "S4_B",
    0x551: "S5_A", 0x552: "S5_B",
    0x651: "S6_A", 0x652: "S6_B",
}

class Interface:
    def __init__(self):
        chan = ""
        
        if platform.system() == "Windows":
            chan = "COM3"
        elif platform.system() == "Darwin":
            chan = "/dev/tty.usbserial-DN9TMGGL"
        elif platform.system() == "Linux":
            chan = "/dev/ttyUSB0"
        
        # initialize the bus object
        bus = can.interface.Bus(
            bustype="slcan",
            channel=chan,
            bitrate=500000
        )

        self.bus = bus
        self.channel = chan
        self.bitrate = 500000
        print(f"Connected to the CAN bus on {self.channel} at {self.bitrate}kbps successfully!!")

    # receive a message from the CAN bus
    def receive(self):
        msg = self.bus.recv(timeout=1)
        return msg
    
    def close(self):
        self.bus.shutdown()
        print("CAN bus connection closed.")
