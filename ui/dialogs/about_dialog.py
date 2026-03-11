"""
Image Converter Pro — About dialog.
Displays application information.
"""

import tkinter as tk
from tkinter import ttk
from config.constants import APP_NAME, APP_VERSION, APP_AUTHOR


class AboutDialog:
    """About dialog window."""

    @staticmethod
    def show(parent):
        """Show the About dialog.

        Args:
            parent: Parent window
        """
        dialog = tk.Toplevel(parent)
        dialog.title(f"About {APP_NAME}")
        dialog.geometry("350x200")
        dialog.resizable(False, False)
        dialog.transient(parent)
        dialog.grab_set()

        ttk.Label(dialog, text=APP_NAME,
                 font=("Segoe UI", 16, "bold")).pack(pady=(20, 5))
        ttk.Label(dialog, text=f"Version {APP_VERSION}").pack()
        ttk.Label(dialog, text=f"Author: {APP_AUTHOR}").pack(pady=5)
        ttk.Label(dialog, text="Professional image converter & editor").pack()
        ttk.Label(dialog, text="License: MIT (unrestricted)").pack(pady=5)

        ttk.Button(dialog, text="Close", command=dialog.destroy).pack(pady=15)
