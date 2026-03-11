"""
Image Converter Pro — Image info panel widget.
Displays detailed information about the selected image.
"""

import os
import tkinter as tk
from tkinter import ttk
from PIL import Image

from config.constants import FONT_FAMILY


class ImageInfoPanel(ttk.LabelFrame):
    """Panel showing selected image information."""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, text="📸 Image Info", **kwargs)

        self._labels = {}
        fields = [
            ("filename", "📄 File:"),
            ("dimensions", "📐 Size:"),
            ("filesize", "💾 Filesize:"),
            ("format", "📦 Format:"),
            ("mode", "🎨 Mode:"),
            ("dpi", "🔍 DPI:"),
        ]

        for i, (key, label_text) in enumerate(fields):
            ttk.Label(self, text=label_text, font=(FONT_FAMILY, 9)).grid(
                row=i, column=0, sticky="w", padx=(10, 5), pady=1
            )
            value_label = ttk.Label(self, text="—", font=(FONT_FAMILY, 9))
            value_label.grid(row=i, column=1, sticky="w", padx=5, pady=1)
            self._labels[key] = value_label

        self.columnconfigure(1, weight=1)

    def update_info(self, image_path):
        """Update displayed information.

        Args:
            image_path: Image file path
        """
        try:
            img = Image.open(image_path)
            filesize = os.path.getsize(image_path)

            self._labels["filename"].config(text=os.path.basename(image_path))
            self._labels["dimensions"].config(text=f"{img.width} × {img.height} px")
            self._labels["filesize"].config(text=self._format_size(filesize))
            self._labels["format"].config(text=img.format or "N/A")
            self._labels["mode"].config(text=img.mode)

            dpi = img.info.get("dpi", (72, 72))
            if isinstance(dpi, tuple):
                self._labels["dpi"].config(text=f"{int(dpi[0])} × {int(dpi[1])}")
            else:
                self._labels["dpi"].config(text=str(int(dpi)))

            img.close()

        except Exception:
            self.clear()

    def clear(self):
        """Clear all displayed information."""
        for label in self._labels.values():
            label.config(text="—")

    @staticmethod
    def _format_size(size_bytes):
        """Format file size in human-readable form."""
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        else:
            return f"{size_bytes / (1024 * 1024):.2f} MB"
