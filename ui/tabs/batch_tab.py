"""
Image Converter Pro — Batch Tab.
Preset management, rename patterns, and operations preview.
"""

import tkinter as tk
from tkinter import ttk, messagebox

from config.constants import RENAME_PLACEHOLDERS


class BatchTab(ttk.Frame):
    """Batch tab — presets, renaming, and operations preview."""

    def __init__(self, parent, app, **kwargs):
        super().__init__(parent, **kwargs)
        self.app = app

        self._create_preset_section()
        self._create_rename_section()
        self._create_operations_section()

    def _create_preset_section(self):
        """Preset management section."""
        preset_frame = ttk.LabelFrame(self, text="💾 Presets")
        preset_frame.pack(fill="x", pady=4, padx=5)

        # Preset name
        name_frame = ttk.Frame(preset_frame)
        name_frame.pack(fill="x", padx=5, pady=3)
        ttk.Label(name_frame, text="Name:").pack(side="left")
        self.preset_name_entry = ttk.Entry(name_frame, width=20)
        self.preset_name_entry.pack(side="left", padx=5, fill="x", expand=True)

        # Buttons
        btn_frame = ttk.Frame(preset_frame)
        btn_frame.pack(fill="x", padx=5, pady=3)

        ttk.Button(btn_frame, text="💾 Save", command=self._save_preset).pack(side="left", padx=3)
        ttk.Button(btn_frame, text="📂 Load", command=self._load_preset).pack(side="left", padx=3)
        ttk.Button(btn_frame, text="🗑️ Delete", command=self._delete_preset).pack(side="left", padx=3)

        # Preset list
        self.preset_listbox = tk.Listbox(preset_frame, height=4)
        self.preset_listbox.pack(fill="x", padx=5, pady=3)
        self._refresh_presets()

    def _create_rename_section(self):
        """File renaming section."""
        rename_frame = ttk.LabelFrame(self, text="📝 File Renaming")
        rename_frame.pack(fill="x", pady=4, padx=5)

        # Enable/disable
        self.rename_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            rename_frame, text="Enable renaming",
            variable=self.rename_var
        ).pack(anchor="w", padx=5, pady=3)

        # Pattern
        pattern_frame = ttk.Frame(rename_frame)
        pattern_frame.pack(fill="x", padx=5, pady=3)
        ttk.Label(pattern_frame, text="Pattern:").pack(side="left")
        self.pattern_entry = ttk.Entry(pattern_frame, width=25)
        self.pattern_entry.insert(0, "image_{num}")
        self.pattern_entry.pack(side="left", padx=5, fill="x", expand=True)

        # Help text
        help_text = "Available placeholders:\n"
        for key, desc in RENAME_PLACEHOLDERS.items():
            help_text += f"  {key} → {desc}\n"
        ttk.Label(rename_frame, text=help_text, justify="left",
                 font=("Segoe UI", 8)).pack(anchor="w", padx=5, pady=3)

    def _create_operations_section(self):
        """Operations preview section."""
        ops_frame = ttk.LabelFrame(self, text="📋 Active Operations")
        ops_frame.pack(fill="both", expand=True, pady=4, padx=5)

        self.operations_text = tk.Text(
            ops_frame, height=8, wrap="word", state="disabled",
            bg="#1e293b", fg="#e2e8f0", font=("Consolas", 9),
            bd=0, highlightthickness=0
        )
        self.operations_text.pack(fill="both", expand=True, padx=3, pady=3)

    # ========== Functions ==========

    def _save_preset(self):
        """Save current settings as a preset."""
        name = self.preset_name_entry.get().strip()
        if not name:
            messagebox.showwarning("Warning", "Please enter a preset name.")
            return

        try:
            settings = self.app.get_all_settings()
            self.app.preset_manager.save(name, settings)
            self._refresh_presets()
            self.app.log.success(f"Preset saved: {name}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save preset: {str(e)}")

    def _load_preset(self):
        """Load selected preset."""
        selection = self.preset_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a preset to load.")
            return

        name = self.preset_listbox.get(selection[0])
        try:
            settings = self.app.preset_manager.load(name)
            self.app.apply_settings(settings)
            self.app.log.info(f"Preset loaded: {name}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not load preset: {str(e)}")

    def _delete_preset(self):
        """Delete selected preset."""
        selection = self.preset_listbox.curselection()
        if not selection:
            return

        name = self.preset_listbox.get(selection[0])
        if self.app.preset_manager.delete(name):
            self._refresh_presets()
            self.app.log.info(f"Preset deleted: {name}")

    def _refresh_presets(self):
        """Refresh preset list."""
        self.preset_listbox.delete(0, tk.END)
        for name in self.app.preset_manager.list_presets():
            self.preset_listbox.insert(tk.END, name)

    def update_operations(self, settings):
        """Update operations preview from settings.

        Args:
            settings: Current settings dictionary
        """
        self.operations_text.config(state="normal")
        self.operations_text.delete("1.0", tk.END)

        lines = ["Active Operations:", "=" * 40 + "\n"]

        lines.append(f"📦 Output Format: {settings.get('format', 'JPEG')}")
        lines.append(f"📐 Size: {settings.get('width', '800')} × {settings.get('height', '600')}")
        lines.append(f"📏 Maintain Ratio: {'Yes' if settings.get('maintain_ratio', True) else 'No'}")
        lines.append(f"🔄 Rotation: {settings.get('angle', '0')}°")
        lines.append(f"⭐ Quality: {settings.get('quality', 85)}")

        b = settings.get("brightness", 1.0)
        c = settings.get("contrast", 1.0)
        if b != 1.0:
            lines.append(f"☀️ Brightness: {b:.1f}")
        if c != 1.0:
            lines.append(f"🔲 Contrast: {c:.1f}")

        # Active filters
        filters = []
        filter_keys = ["blur", "sharpen", "edge_enhance", "emboss",
                       "contour", "grayscale", "sepia", "vignette", "auto_enhance"]
        for key in filter_keys:
            if settings.get(key, False):
                filters.append(key.replace("_", " ").title())
        if filters:
            lines.append(f"🎭 Filters: {', '.join(filters)}")

        if settings.get("watermark", False):
            lines.append(f"💧 Watermark: \"{settings.get('watermark_text', '')}\"")

        self.operations_text.insert("1.0", "\n".join(lines))
        self.operations_text.config(state="disabled")

    def get_rename_settings(self):
        """Get rename settings."""
        return {
            "rename": self.rename_var.get(),
            "rename_pattern": self.pattern_entry.get(),
        }
