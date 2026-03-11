"""
Image Converter Pro — Effects Tab.
Advanced filters, adjustments, and watermark configuration.
"""

import tkinter as tk
from tkinter import ttk

from config.constants import FILTER_NAMES, WATERMARK_POSITIONS
from ui.widgets.labeled_scale import LabeledScale


class EffectsTab(ttk.Frame):
    """Effects tab — filters, adjustments, and watermark settings."""

    def __init__(self, parent, app, **kwargs):
        super().__init__(parent, **kwargs)
        self.app = app

        self._create_filters_section()
        self._create_adjustments_section()
        self._create_watermark_section()

    def _create_filters_section(self):
        """Filters section with checkboxes."""
        filter_frame = ttk.LabelFrame(self, text="🎭 Filters")
        filter_frame.pack(fill="x", pady=4, padx=5)

        self.filter_vars = {}
        cols = ttk.Frame(filter_frame)
        cols.pack(fill="x", padx=5, pady=3)

        for i, name in enumerate(FILTER_NAMES):
            var = tk.BooleanVar(value=False)
            self.filter_vars[name] = var
            cb = ttk.Checkbutton(cols, text=name, variable=var)
            cb.grid(row=i // 3, column=i % 3, sticky="w", padx=5, pady=2)

    def _create_adjustments_section(self):
        """Additional adjustments section."""
        adj_frame = ttk.LabelFrame(self, text="🔧 Adjustments")
        adj_frame.pack(fill="x", pady=4, padx=5)

        self.saturation_scale = LabeledScale(adj_frame, "Saturation:", 0, 2, 1.0)
        self.saturation_scale.pack(fill="x", padx=5, pady=3)

        self.sharpness_scale = LabeledScale(adj_frame, "Sharpness:", 0, 2, 1.0)
        self.sharpness_scale.pack(fill="x", padx=5, pady=3)

    def _create_watermark_section(self):
        """Watermark configuration section."""
        wm_frame = ttk.LabelFrame(self, text="💧 Watermark")
        wm_frame.pack(fill="x", pady=4, padx=5)

        # Enable/disable
        self.watermark_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            wm_frame, text="Enable watermark",
            variable=self.watermark_var
        ).pack(anchor="w", padx=5, pady=3)

        # Text
        text_frame = ttk.Frame(wm_frame)
        text_frame.pack(fill="x", padx=5, pady=3)
        ttk.Label(text_frame, text="Text:").pack(side="left")
        self.watermark_text = ttk.Entry(text_frame, width=25)
        self.watermark_text.insert(0, "© Copyright")
        self.watermark_text.pack(side="right", fill="x", expand=True, padx=5)

        # Position
        pos_frame = ttk.Frame(wm_frame)
        pos_frame.pack(fill="x", padx=5, pady=3)
        ttk.Label(pos_frame, text="Position:").pack(side="left")
        self.watermark_position = tk.StringVar(value="bottom-right")
        ttk.OptionMenu(pos_frame, self.watermark_position,
                       "bottom-right", *WATERMARK_POSITIONS).pack(side="right")

        # Opacity
        self.watermark_opacity = LabeledScale(
            wm_frame, "Opacity:", 0, 1, 0.5, "{:.2f}"
        )
        self.watermark_opacity.pack(fill="x", padx=5, pady=3)

    def get_settings(self):
        """Get all effects settings as a dictionary."""
        settings = {
            "saturation": self.saturation_scale.get(),
            "sharpness": self.sharpness_scale.get(),
            "watermark": self.watermark_var.get(),
            "watermark_text": self.watermark_text.get(),
            "watermark_position": self.watermark_position.get(),
            "watermark_opacity": self.watermark_opacity.get(),
        }

        # Filter flags
        filter_map = {
            "Blur": "blur", "Sharpen": "sharpen",
            "Edge Enhance": "edge_enhance", "Emboss": "emboss",
            "Contour": "contour", "Grayscale": "grayscale",
            "Sepia": "sepia", "Vignette": "vignette",
            "Auto Enhance": "auto_enhance",
        }

        for display_name, key in filter_map.items():
            if display_name in self.filter_vars:
                settings[key] = self.filter_vars[display_name].get()

        return settings

    def set_settings(self, settings):
        """Set settings from a dictionary (for preset loading)."""
        self.saturation_scale.set(settings.get("saturation", 1.0))
        self.sharpness_scale.set(settings.get("sharpness", 1.0))

        self.watermark_var.set(settings.get("watermark", False))
        self.watermark_text.delete(0, tk.END)
        self.watermark_text.insert(0, settings.get("watermark_text", "© Copyright"))
        self.watermark_position.set(settings.get("watermark_position", "bottom-right"))
        self.watermark_opacity.set(settings.get("watermark_opacity", 0.5))

        filter_map = {
            "Blur": "blur", "Sharpen": "sharpen",
            "Edge Enhance": "edge_enhance", "Emboss": "emboss",
            "Contour": "contour", "Grayscale": "grayscale",
            "Sepia": "sepia", "Vignette": "vignette",
            "Auto Enhance": "auto_enhance",
        }
        for display_name, key in filter_map.items():
            if display_name in self.filter_vars:
                self.filter_vars[display_name].set(settings.get(key, False))
