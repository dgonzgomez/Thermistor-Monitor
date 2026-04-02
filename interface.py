# talks to the CAN bus and gets the data from the sensors
import os
import can
import platform
from serial.tools import list_ports

# get the list of available ports
def get_ports():
    ports = [p.device for p in list_ports.comports()] #list_ports.comports()

    # testing
    #fake_port = "/tmp/ttySLCAN0"
    #if os.path.exists(fake_port):
    #    ports.append(fake_port)
    return ports #[port.device for port in ports]

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
