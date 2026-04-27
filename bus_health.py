from collections import deque
import time
from customtkinter import (
    CTkToplevel,
    CTkFrame,
    CTkLabel,
    StringVar,
)
from ui_style import FONTS, APP_BG, TABLE_HEADER_BG, TABLE_TEXT, PADX, PADDING

BAUD_RATE = 500_000
FRAME_OVERHEAD_BITS = 47
STUFFING_FACTOR = 1.2
WINDOW_SECONDS = 1.0

_frame_log = deque()
_start_time = None
_health_window = None


def start():
    global _start_time
    _start_time = time.time()

def log_frame(msg):
    data_bits = len(msg.data) * 8
    bit_length = int((FRAME_OVERHEAD_BITS + data_bits) * STUFFING_FACTOR)
    _frame_log.append((time.time(), bit_length))

def get_bus_load():
    now = time.time()
    cutoff = now - WINDOW_SECONDS
    while _frame_log and _frame_log[0][0] < cutoff:
        _frame_log.popleft()
    bits_used = sum(bl for _, bl in _frame_log)
    return (bits_used / BAUD_RATE) * 100


def get_runtime():
    if _start_time is None:
        return "00:00:00"
    elapsed = int(time.time() - _start_time)
    h = elapsed // 3600
    m = (elapsed % 3600) // 60
    s = elapsed % 60
    return f"{h:02d}:{m:02d}:{s:02d}"

# styling for bus health window
def show_bus_health():
    global _health_window

    if _health_window is not None and _health_window.winfo_exists():
        _health_window.focus()
        return

    win = CTkToplevel()
    win.title("Bus Health")
    win.geometry("320x220")
    win.configure(fg_color=APP_BG)
    win.resizable(False, False)
    _health_window = win

    frame = CTkFrame(win, fg_color=TABLE_HEADER_BG, corner_radius=10)
    frame.pack(fill="both", expand=True, padx=PADDING, pady=PADDING)

    def row(label_text, var, row_idx):
        CTkLabel(
            frame,
            text=label_text,
            font=FONTS["table_header"],
            text_color=TABLE_TEXT,
            anchor="w",
        ).grid(row=row_idx, column=0, sticky="w", padx=16, pady=8)
        CTkLabel(
            frame,
            textvariable=var,
            font=FONTS["value"],
            text_color=TABLE_TEXT,
            anchor="e",
        ).grid(row=row_idx, column=1, sticky="e", padx=16, pady=8)
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

    load_var = StringVar(value="0.0%")
    runtime_var = StringVar(value="00:00:00")
    baud_var = StringVar(value=f"{BAUD_RATE // 1000} kbps")

    row("Bus Load", load_var, 0)
    row("Baud Rate", baud_var, 1)
    row("Runtime", runtime_var, 2)

    def refresh():
        if not win.winfo_exists():
            return
        load_var.set(f"{get_bus_load():.1f}%")
        runtime_var.set(get_runtime())
        win.after(500, refresh)

    refresh()
