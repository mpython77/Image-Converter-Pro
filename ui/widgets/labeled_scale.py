"""
Image Converter Pro — Reusable labeled scale widget.
Combines a label, a scale slider, and a value display.
"""

import tkinter as tk
from tkinter import ttk


class LabeledScale(ttk.Frame):
    """Scale widget with label and real-time value display.

    Features:
        - Custom label text
        - Configurable range (from_, to)
        - Default value
        - Value format string
        - Optional change callback
    """

    def __init__(self, parent, label_text="", from_=0, to=100,
                 default=50, format_str="{:.1f}", command=None, **kwargs):
        """Create LabeledScale.

        Args:
            parent: Parent widget
            label_text: Label text
            from_: Minimum value
            to: Maximum value
            default: Default value
            format_str: Format string for value display
            command: Optional callback on value change
        """
        super().__init__(parent, **kwargs)

        self._format_str = format_str
        self._command = command

        # Label
        self._label = ttk.Label(self, text=label_text, width=12, anchor="w")
        self._label.pack(side="left", padx=(0, 5))

        # Scale (slider)
        self._var = tk.DoubleVar(value=default)
        self._scale = ttk.Scale(
            self, from_=from_, to=to,
            variable=self._var, orient="horizontal",
            command=self._on_change
        )
        self._scale.pack(side="left", fill="x", expand=True)

        # Value display
        self._value_label = ttk.Label(
            self, text=format_str.format(default), width=6, anchor="e"
        )
        self._value_label.pack(side="right", padx=(5, 0))

    def _on_change(self, value):
        """Internal handler for value changes."""
        val = float(value)
        self._value_label.config(text=self._format_str.format(val))
        if self._command:
            self._command(val)

    def get(self):
        """Get current value.

        Returns:
            float: Current value
        """
        return self._var.get()

    def set(self, value):
        """Set the value.

        Args:
            value: New value
        """
        self._var.set(value)
        self._value_label.config(text=self._format_str.format(float(value)))
