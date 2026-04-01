from customtkinter import set_appearance_mode, set_default_color_theme

GEOMETRY = "1080x520"
STATUS_COLOR = "#FF6B6B"
TABLE_HEADER_BG = "#1F2937"
TABLE_ROW_BG = "#111827"
TABLE_ROW_ALT_BG = "#0B1220"
TABLE_BORDER = "#374151"
TABLE_TEXT = "#E5E7EB"
APP_BG = "#0F172A"

PADDING = 12
PADX = 6
PADY_HEADER = (0, 4)
PADY_PORTS = (0, 4)
PADY_STATUS = (4, 0)

FONTS = {
    "label": ("Helvetica", 11),
    "value": ("Menlo", 11),
    "header": ("Helvetica", 12, "bold"),
    "table_header": ("Helvetica", 11, "bold"),
}

def apply_styles():
    set_appearance_mode("dark")
    set_default_color_theme("green")