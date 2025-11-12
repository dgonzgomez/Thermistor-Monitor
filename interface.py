# talks to the CAN bus and gets the data from the sensors
import can
import platform

class Interface:
    def __init__(self):
        chan = ""
        
        if platform.system() == "Windows":
            chan = "COM3"
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
