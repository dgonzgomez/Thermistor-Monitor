import time

from interface import Interface
from parser import parse

def main() -> None:
    while True:
        msg = interface.receive()
        if msg is not None:
            parse(msg)
        else:
            print("No message received")
        time.sleep(1)

if __name__ == "__main__":
    main()