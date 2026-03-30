from tkinter import ttk

GEOMETRY = "1080x520"
STATUS_COLOR = "#8bffbb"

PADDING = 6
PADX = 6
PADY_HEADER = (0, 4)
PADY_PORTS = (0, 4)
PADY_STATUS = (4, 0)

FONTS = {
    "TLabel": ("Helvetica", 11),

    "Value.TLabel": ("Menlo", 11),

    "Header.TLabel": ("Helvetica", 12, "bold"),
}

def apply_styles():
    style = ttk.Style()
    style.theme_use("clam")

    for name, font in FONTS.items():
        style.configure(name, font=font)

    # Row styling
    style.configure("TLabel", padding=(2, 1))
    style.configure("Value.TLabel", padding=(2, 1))

    style.configure("Value.TLabel", anchor="e")  # right-align values

    # Header styling
    style.configure("Header.TLabel", padding=(2, 2))

    # Scrollbar styling
    style.configure("Vertical.TScrollbar", gripcount=0, arrowsize=10)

    style.configure("TButton", padding=(6, 2))
    style.configure("TCombobox", padding=(4, 2))