"""
Image Converter Pro — Entry point.
"""

import sys
import os
import tkinter as tk

# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.constants import APP_NAME, APP_VERSION
from ui.app import ImageConverterApp


def main():
    """Launch the application."""
    root = tk.Tk()
    root.withdraw()  # Hide until fully loaded

    app = ImageConverterApp(root)

    root.deiconify()  # Show window
    root.mainloop()


if __name__ == "__main__":
    main()
