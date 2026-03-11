"""
Image Converter Pro — Constants and default settings.
"""

# Application
APP_NAME = "Image Converter Pro"
APP_VERSION = "2.0.0"
APP_AUTHOR = "mpython77"

# Window
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 950
WINDOW_MIN_WIDTH = 800
WINDOW_MIN_HEIGHT = 700

# Image defaults
DEFAULT_WIDTH = 800
DEFAULT_HEIGHT = 600
DEFAULT_QUALITY = 85
MAX_QUALITY = 100
MIN_QUALITY = 1
MAX_IMAGE_DIMENSION = 20000  # Maximum image dimension (px)

# Supported formats
SUPPORTED_FORMATS = ["JPEG", "PNG", "BMP", "GIF", "TIFF", "WEBP", "ICO"]
SUPPORTED_EXTENSIONS = ("*.png", "*.jpg", "*.jpeg", "*.bmp", "*.gif", "*.tiff", "*.webp", "*.ico")
FILE_FILTER = [("Image files", " ".join(SUPPORTED_EXTENSIONS)), ("All files", "*.*")]

# Format -> Extension mapping
FORMAT_EXTENSIONS = {
    "JPEG": ".jpg",
    "PNG": ".png",
    "BMP": ".bmp",
    "GIF": ".gif",
    "TIFF": ".tiff",
    "WEBP": ".webp",
    "ICO": ".ico",
}

# Rotation presets
ROTATION_ANGLES = ["0", "90", "180", "270", "Custom"]

# Filter names
FILTER_NAMES = [
    "Blur", "Sharpen", "Edge Enhance", "Emboss", "Contour",
    "Grayscale", "Sepia", "Vignette", "Auto Enhance"
]

# Watermark positions
WATERMARK_POSITIONS = ["top-left", "top-right", "bottom-left", "bottom-right", "center"]

# Rename patterns
RENAME_PLACEHOLDERS = {
    "{num}": "Sequential number (001, 002, ...)",
    "{orig}": "Original filename",
    "{date}": "Today's date (2024-01-15)",
    "{time}": "Current time (14-30-00)",
    "{w}": "Image width",
    "{h}": "Image height",
}

# Batch processing
MAX_WORKERS = 4
BATCH_TIMEOUT = 300  # Max time per image (seconds)

# History (Undo/Redo)
MAX_HISTORY_STEPS = 20

# Preview
PREVIEW_MAX_WIDTH = 600
PREVIEW_MAX_HEIGHT = 500

# DPI
DEFAULT_DPI = 72
PRINT_DPI = 300

# Fonts
FONT_FAMILY = "Segoe UI"
FONT_SIZE_NORMAL = 10
FONT_SIZE_TITLE = 11
FONT_SIZE_SMALL = 9

# Keyboard shortcuts
SHORTCUTS = {
    "open": "<Control-o>",
    "save": "<Control-s>",
    "undo": "<Control-z>",
    "redo": "<Control-y>",
    "quit": "<Control-q>",
    "process": "<Control-Return>",
    "clear": "<Control-Delete>",
    "preview": "<Control-p>",
    "theme_toggle": "<Control-t>",
    "select_all": "<Control-a>",
}

# Drag & Drop extensions
DND_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp", ".gif", ".tiff", ".webp", ".ico"}
