"""
Image Converter Pro — Toolbar widget.
Customizable toolbar with buttons, separators, and tooltips.
"""

import tkinter as tk
from tkinter import ttk


class Toolbar(ttk.Frame):
    """Application toolbar with buttons and separators."""

    def __init__(self, parent, **kwargs):
        """Create Toolbar.

        Args:
            parent: Parent widget
        """
        super().__init__(parent, **kwargs)
        self._buttons = {}

    def add_button(self, name, text, command, tooltip=""):
        """Add a button to the toolbar.

        Args:
            name: Button identifier
            text: Button label
            command: Click handler
            tooltip: Tooltip text

        Returns:
            ttk.Button: Created button
        """
        btn = ttk.Button(self, text=text, command=command)
        btn.pack(side="left", padx=2, pady=2)
        self._buttons[name] = btn

        if tooltip:
            self._add_tooltip(btn, tooltip)

        return btn

    def add_separator(self):
        """Add a vertical separator to the toolbar."""
        sep = ttk.Separator(self, orient="vertical")
        sep.pack(side="left", fill="y", padx=6, pady=3)

    def enable_button(self, name):
        """Enable a button by name."""
        if name in self._buttons:
            self._buttons[name].config(state="normal")

    def disable_button(self, name):
        """Disable a button by name."""
        if name in self._buttons:
            self._buttons[name].config(state="disabled")

    def _add_tooltip(self, widget, text):
        """Add tooltip to a widget.

        Shows tooltip on mouse hover with a slight delay.

        Args:
            widget: Target widget
            text: Tooltip text
        """
        tooltip = None

        def show(event):
            nonlocal tooltip
            x = widget.winfo_rootx() + 20
            y = widget.winfo_rooty() + widget.winfo_height() + 5
            tooltip = tk.Toplevel(widget)
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{x}+{y}")
            label = tk.Label(
                tooltip, text=text, bg="#334155", fg="#e2e8f0",
                padx=8, pady=4, font=("Segoe UI", 9)
            )
            label.pack()

        def hide(event):
            nonlocal tooltip
            if tooltip:
                tooltip.destroy()
                tooltip = None

        widget.bind("<Enter>", show)
        widget.bind("<Leave>", hide)
