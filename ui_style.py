from tkinter import ttk

GEOMETRY = "620x420"
PADDING = 8
PADX = 6
PADY_HEADER = (0, 6)
PADY_PORTS = (0, 6)
PADY_STATUS = (6, 0)
STATUS_COLOR = "#777777"

FONTS = {
    "TLabel": ("Helvetica", 12),
    "Value.TLabel": ("Menlo", 12),
    "Header.TLabel": ("Helvetica", 13, "bold"),
}

def apply_styles():
    style = ttk.Style()
    style.theme_use("clam")
    for name, font in FONTS.items():
        style.configure(name, font=font)
