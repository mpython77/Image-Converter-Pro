"""
Image Converter Pro — Status bar widget.
Displays status message, file count, and additional info.
"""

import tkinter as tk
from tkinter import ttk


class StatusBar(ttk.Frame):
    """Application status bar with multiple sections."""

    def __init__(self, parent, **kwargs):
        """Create StatusBar.

        Args:
            parent: Parent widget
        """
        super().__init__(parent, **kwargs)

        # Status message (left)
        self._status_label = ttk.Label(self, text="✅ Ready", anchor="w")
        self._status_label.pack(side="left", fill="x", expand=True, padx=5)

        # File count (center)
        self._file_count_label = ttk.Label(self, text="📁 Files: 0", anchor="center")
        self._file_count_label.pack(side="left", padx=10)

        # Info (right)
        self._info_label = ttk.Label(self, text="", anchor="e")
        self._info_label.pack(side="right", padx=5)

    def set_status(self, message, level="info"):
        """Update status message.

        Args:
            message: Status text
            level: Severity level (info, success, warning, error)
        """
        icons = {
            "info": "ℹ️",
            "success": "✅",
            "warning": "⚠️",
            "error": "❌",
        }
        icon = icons.get(level, "ℹ️")
        self._status_label.config(text=f"{icon} {message}")

    def set_file_count(self, count):
        """Update file count display.

        Args:
            count: Number of selected files
        """
        self._file_count_label.config(text=f"📁 Files: {count}")

    def set_info(self, text):
        """Update info section.

        Args:
            text: Information text
        """
        self._info_label.config(text=text)
