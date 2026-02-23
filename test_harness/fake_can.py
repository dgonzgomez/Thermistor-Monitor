#!/usr/bin/env python3
import os
import pty
import time
import select
import termios

# This is the stable name your GUI will connect to
LINK_NAME = "/tmp/ttySLCAN0"


def make_slcan_frame(can_id, data):
    """Format a CAN frame as an SLCAN ASCII packet."""
    can_id_str = f"{can_id:03X}"
    dlc = len(data)
    data_str = "".join(f"{b:02X}" for b in data)
    return f"t{can_id_str}{dlc}{data_str}\r".encode()


def setup_virtual_serial():
    """Create a PTY and expose it like a real serial port."""
    master_fd, slave_fd = pty.openpty()
    slave_name = os.ttyname(slave_fd)

    # Put terminal into RAW mode (important for binary-style traffic)
    attrs = termios.tcgetattr(slave_fd)
    attrs[3] &= ~(termios.ICANON | termios.ECHO)  # raw input
    termios.tcsetattr(slave_fd, termios.TCSANOW, attrs)

    # Create a stable symlink so your GUI can find it
    try:
        os.unlink(LINK_NAME)
    except FileNotFoundError:
        pass

    os.symlink(slave_name, LINK_NAME)

    print("Fake SLCAN device ready")
    print(f"Real PTY : {slave_name}")
    print(f"Use Port : {LINK_NAME}")

    # Make reads non-blocking
    os.set_blocking(master_fd, False)

    return master_fd


def main():
    master_fd = setup_virtual_serial()

    counter = 0
    last_tx = time.time()

    while True:
        # --- Handle incoming commands from your CAN app ---
        r, _, _ = select.select([master_fd], [], [], 0.1)
        if master_fd in r:
            try:
                data = os.read(master_fd, 1024)
                if data:
                    print("RX:", data.strip())

                    # Acknowledge common SLCAN commands
                    if data[:1] in b"OSC":  # Open, Speed, Close
                        os.write(master_fd, b"\r")

            except BlockingIOError:
                pass

        # --- Periodically transmit a CAN frame ---
        if time.time() - last_tx > 1.0:
            payload = [(counter + i) & 0xFF for i in range(8)]
            frame = make_slcan_frame(0x0C0, payload)
            os.write(master_fd, frame)
            print("TX:", frame.strip())

            counter += 1
            last_tx = time.time()


if __name__ == "__main__":
    main()