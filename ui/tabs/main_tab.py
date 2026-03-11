"""
Image Converter Pro — Main Tab.
File selection, conversion settings, preview.
"""

import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk

from config.constants import (
    SUPPORTED_FORMATS, ROTATION_ANGLES, DEFAULT_WIDTH,
    DEFAULT_HEIGHT, DEFAULT_QUALITY, FILE_FILTER, FONT_FAMILY
)
from ui.widgets.labeled_scale import LabeledScale


class MainTab(ttk.Frame):
    """Main tab — file selection, conversion settings, and basic effects."""

    def __init__(self, parent, app, **kwargs):
        super().__init__(parent, **kwargs)
        self.app = app

        self._create_file_section()
        self._create_conversion_section()
        self._create_basic_effects_section()
        self._create_process_section()

    # ========== File Selection ==========

    def _create_file_section(self):
        """File selection section."""
        file_frame = ttk.LabelFrame(self, text="📁 File Selection")
        file_frame.pack(fill="x", pady=(0, 8), padx=5)

        # Buttons
        btn_frame = ttk.Frame(file_frame)
        btn_frame.pack(fill="x", pady=5)

        self.select_btn = ttk.Button(btn_frame, text="📂 Select Images", command=self._select_images)
        self.select_btn.pack(side="left", padx=3)

        self.clear_btn = ttk.Button(btn_frame, text="🗑️ Clear", command=self._clear_selection)
        self.clear_btn.pack(side="left", padx=3)

        self.preview_btn = ttk.Button(btn_frame, text="👁️ Preview", command=self._preview_image, state="disabled")
        self.preview_btn.pack(side="right", padx=3)

        self.metadata_btn = ttk.Button(btn_frame, text="ℹ️ Metadata", command=self._show_metadata, state="disabled")
        self.metadata_btn.pack(side="right", padx=3)

        # File list
        list_frame = ttk.Frame(file_frame)
        list_frame.pack(fill="both", expand=True, pady=3)

        self.file_listbox = tk.Listbox(
            list_frame, height=4, selectmode=tk.EXTENDED,
            bg="white", bd=1, highlightthickness=1,
            highlightbackground="#e2e8f0", font=(FONT_FAMILY, 9),
            selectbackground="#3b82f6", selectforeground="white"
        )
        self.file_listbox.pack(side="left", fill="both", expand=True)
        self.file_listbox.bind("<<ListboxSelect>>", self._on_file_select)

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.file_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.file_listbox.config(yscrollcommand=scrollbar.set)

        self.file_label = ttk.Label(file_frame, text="Selected files: 0")
        self.file_label.pack(pady=3, anchor="w")

    # ========== Conversion Settings ==========

    def _create_conversion_section(self):
        """Conversion settings section."""
        conv_frame = ttk.LabelFrame(self, text="⚙️ Conversion Settings")
        conv_frame.pack(fill="x", pady=4, padx=5)

        # Two columns
        columns = ttk.Frame(conv_frame)
        columns.pack(fill="x", pady=3)

        left = ttk.Frame(columns)
        left.pack(side="left", fill="both", expand=True, padx=3)

        right = ttk.Frame(columns)
        right.pack(side="right", fill="both", expand=True, padx=3)

        # Format
        fmt_frame = ttk.Frame(left)
        fmt_frame.pack(fill="x", pady=3)
        ttk.Label(fmt_frame, text="Output format:").pack(side="left")
        self.format_var = tk.StringVar(value="JPEG")
        fmt_menu = ttk.OptionMenu(fmt_frame, self.format_var, "JPEG", *SUPPORTED_FORMATS)
        fmt_menu.pack(side="right")

        # Size
        size_frame = ttk.Frame(left)
        size_frame.pack(fill="x", pady=3)
        ttk.Label(size_frame, text="Size (W × H):").pack(side="left")

        size_inputs = ttk.Frame(size_frame)
        size_inputs.pack(side="right")

        self.width_entry = ttk.Entry(size_inputs, width=6)
        self.width_entry.insert(0, str(DEFAULT_WIDTH))
        self.width_entry.pack(side="left", padx=2)

        ttk.Label(size_inputs, text="×").pack(side="left", padx=2)

        self.height_entry = ttk.Entry(size_inputs, width=6)
        self.height_entry.insert(0, str(DEFAULT_HEIGHT))
        self.height_entry.pack(side="left", padx=2)

        # Aspect ratio
        self.maintain_ratio_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(left, text="📐 Maintain aspect ratio", variable=self.maintain_ratio_var).pack(anchor="w", pady=2)

        # Rotate
        rot_frame = ttk.Frame(right)
        rot_frame.pack(fill="x", pady=3)
        ttk.Label(rot_frame, text="Rotation:").pack(side="left")
        self.rotate_var = tk.StringVar(value="0")
        ttk.OptionMenu(rot_frame, self.rotate_var, "0", *ROTATION_ANGLES,
                        command=self._toggle_rotate_entry).pack(side="right")

        # Custom angle
        custom_frame = ttk.Frame(right)
        custom_frame.pack(fill="x", pady=3)
        ttk.Label(custom_frame, text="Angle (°):").pack(side="left")
        self.rotate_entry = ttk.Entry(custom_frame, width=6, state="disabled")
        self.rotate_entry.insert(0, "0")
        self.rotate_entry.pack(side="right")

        # Quality
        self.quality_scale = LabeledScale(
            right, label_text="Quality:", from_=1, to=100,
            default=DEFAULT_QUALITY, format_str="{:.0f}"
        )
        self.quality_scale.pack(fill="x", pady=3)

    # ========== Basic Effects ==========

    def _create_basic_effects_section(self):
        """Basic effects section."""
        effect_frame = ttk.LabelFrame(self, text="🎨 Basic Effects")
        effect_frame.pack(fill="x", pady=4, padx=5)

        cols = ttk.Frame(effect_frame)
        cols.pack(fill="x")

        left = ttk.Frame(cols)
        left.pack(side="left", fill="both", expand=True, padx=3)

        right = ttk.Frame(cols)
        right.pack(side="right", fill="both", expand=True, padx=3)

        self.brightness_scale = LabeledScale(left, "Brightness:", 0, 2, 1.0)
        self.brightness_scale.pack(fill="x", pady=3)

        self.contrast_scale = LabeledScale(right, "Contrast:", 0, 2, 1.0)
        self.contrast_scale.pack(fill="x", pady=3)

    # ========== Process Section ==========

    def _create_process_section(self):
        """Process control section."""
        process_frame = ttk.Frame(self)
        process_frame.pack(fill="x", pady=4, padx=5)

        # Buttons
        btn_frame = ttk.Frame(process_frame)
        btn_frame.pack(fill="x", pady=3)

        self.process_btn = ttk.Button(
            btn_frame, text="🚀 Process & Save",
            command=self.app.start_processing
        )
        self.process_btn.pack(side="left", padx=3)

        self.cancel_btn = ttk.Button(
            btn_frame, text="⏹️ Cancel",
            command=self.app.cancel_processing, state="disabled"
        )
        self.cancel_btn.pack(side="left", padx=3)

        self.open_folder_btn = ttk.Button(
            btn_frame, text="📂 Open Folder",
            command=self.app.open_output_folder, state="disabled"
        )
        self.open_folder_btn.pack(side="right", padx=3)

        # Progress
        self.progress = ttk.Progressbar(process_frame, mode="determinate")
        self.progress.pack(fill="x", pady=3)

        # Status
        status_frame = ttk.Frame(process_frame)
        status_frame.pack(fill="x", pady=3)

        self.status_label = ttk.Label(status_frame, text="Status: Ready")
        self.status_label.pack(side="left")

        self.time_label = ttk.Label(status_frame, text="")
        self.time_label.pack(side="right")

    # ========== Functions ==========

    def _select_images(self):
        """Open file selection dialog."""
        new_paths = filedialog.askopenfilenames(filetypes=FILE_FILTER)
        if new_paths:
            self.app.image_paths.extend(new_paths)
            self._update_file_list()
            self.app.log.info(f"{len(new_paths)} image(s) selected.")

    def _clear_selection(self):
        """Clear file selection."""
        self.app.image_paths.clear()
        self._update_file_list()
        self.app.log.info("Selection cleared.")

    def _update_file_list(self):
        """Update file listbox."""
        self.file_listbox.delete(0, tk.END)
        for path in self.app.image_paths:
            self.file_listbox.insert(tk.END, os.path.basename(path))

        count = len(self.app.image_paths)
        self.file_label.config(text=f"Selected files: {count}")
        self.app.status_bar.set_file_count(count)

        state = "normal" if count > 0 else "disabled"
        self.preview_btn.config(state=state)
        self.metadata_btn.config(state=state)

    def _on_file_select(self, event=None):
        """Handle file list selection."""
        state = "normal" if self.file_listbox.curselection() else "disabled"
        self.preview_btn.config(state=state)
        self.metadata_btn.config(state=state)

    def _toggle_rotate_entry(self, value):
        """Toggle custom rotation entry."""
        if value == "Custom":
            self.rotate_entry.config(state="normal")
        else:
            self.rotate_entry.config(state="disabled")
            self.rotate_entry.delete(0, tk.END)
            self.rotate_entry.insert(0, value)

    def _preview_image(self):
        """Preview selected image."""
        selection = self.file_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an image to preview.")
            return

        path = self.app.image_paths[selection[0]]
        try:
            img = Image.open(path)
            self.app.show_preview(img, os.path.basename(path))
        except Exception as e:
            messagebox.showerror("Error", f"Could not open image: {str(e)}")

    def _show_metadata(self):
        """Show EXIF metadata for selected image."""
        selection = self.file_listbox.curselection()
        if not selection:
            return

        path = self.app.image_paths[selection[0]]
        self.app.show_metadata(path)

    def get_settings(self):
        """Get all settings as a dictionary."""
        rotate_angle = self.rotate_entry.get() if self.rotate_var.get() == "Custom" else self.rotate_var.get()

        return {
            "format": self.format_var.get(),
            "width": self.width_entry.get(),
            "height": self.height_entry.get(),
            "maintain_ratio": self.maintain_ratio_var.get(),
            "angle": rotate_angle,
            "quality": int(self.quality_scale.get()),
            "brightness": self.brightness_scale.get(),
            "contrast": self.contrast_scale.get(),
        }

    def set_settings(self, settings):
        """Set settings from a dictionary (for preset loading)."""
        self.format_var.set(settings.get("format", "JPEG"))

        self.width_entry.delete(0, tk.END)
        self.width_entry.insert(0, str(settings.get("width", DEFAULT_WIDTH)))

        self.height_entry.delete(0, tk.END)
        self.height_entry.insert(0, str(settings.get("height", DEFAULT_HEIGHT)))

        self.maintain_ratio_var.set(settings.get("maintain_ratio", True))

        angle = settings.get("angle", 0)
        if str(angle) in ["0", "90", "180", "270"]:
            self.rotate_var.set(str(angle))
            self._toggle_rotate_entry(str(angle))
        else:
            self.rotate_var.set("Custom")
            self._toggle_rotate_entry("Custom")
            self.rotate_entry.delete(0, tk.END)
            self.rotate_entry.insert(0, str(angle))

        self.quality_scale.set(settings.get("quality", DEFAULT_QUALITY))
        self.brightness_scale.set(settings.get("brightness", 1.0))
        self.contrast_scale.set(settings.get("contrast", 1.0))
