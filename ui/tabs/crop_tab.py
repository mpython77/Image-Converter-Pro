"""
Image Converter Pro — Crop Tab.
Interactive image cropping with ratio presets.
"""

import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image

from ui.widgets.image_canvas import ImageCanvas
from core.cropper import ImageCropper


class CropTab(ttk.Frame):
    """Crop tab — interactive image cropping."""

    def __init__(self, parent, app, **kwargs):
        super().__init__(parent, **kwargs)
        self.app = app
        self._current_image = None
        self._cropped_image = None

        self._create_controls()
        self._create_canvas()

    def _create_controls(self):
        """Create crop control section."""
        ctrl_frame = ttk.Frame(self)
        ctrl_frame.pack(fill="x", padx=5, pady=5)

        # Load button
        ttk.Button(ctrl_frame, text="📂 Load Image", command=self._load_image).pack(side="left", padx=3)

        # Ratio presets
        ttk.Label(ctrl_frame, text="Ratio:").pack(side="left", padx=(15, 3))
        self.ratio_var = tk.StringVar(value="Free")
        ratios = ["Free", "1:1", "4:3", "16:9", "3:2", "9:16"]
        ttk.OptionMenu(ctrl_frame, self.ratio_var, "Free", *ratios,
                       command=self._apply_ratio).pack(side="left", padx=3)

        # Action buttons
        ttk.Button(ctrl_frame, text="✂️ Apply Crop", command=self._apply_crop).pack(side="left", padx=3)
        ttk.Button(ctrl_frame, text="🔄 Reset", command=self._reset).pack(side="left", padx=3)
        ttk.Button(ctrl_frame, text="💾 Save", command=self._save_cropped).pack(side="right", padx=3)

        # Coordinates display
        self.coord_label = ttk.Label(ctrl_frame, text="Crop: Not selected")
        self.coord_label.pack(side="right", padx=10)

    def _create_canvas(self):
        """Create image canvas."""
        canvas_frame = ttk.LabelFrame(self, text="✂️ Crop Area")
        canvas_frame.pack(fill="both", expand=True, padx=5, pady=5)

        self.canvas = ImageCanvas(canvas_frame, width=500, height=350)
        self.canvas.pack(fill="both", expand=True, padx=3, pady=3)
        self.canvas.set_crop_callback(self._on_crop_select)

    def _load_image(self):
        """Load image for cropping."""
        path = filedialog.askopenfilename(
            filetypes=[("Images", "*.png *.jpg *.jpeg *.bmp *.tiff *.webp")]
        )
        if path:
            try:
                self._current_image = Image.open(path)
                self._current_image.load()
                self.canvas.show_image(self._current_image)
                self.app.log.info(f"Image loaded for cropping: {os.path.basename(path)}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not load image: {str(e)}")

    def _on_crop_select(self, x1, y1, x2, y2):
        """Handle crop selection."""
        self.coord_label.config(text=f"Crop: ({x1},{y1}) → ({x2},{y2})")

    def _apply_ratio(self, ratio_str):
        """Apply ratio-based crop."""
        if not self._current_image or ratio_str == "Free":
            return

        try:
            w, h = map(int, ratio_str.split(":"))
            self._cropped_image = ImageCropper.crop_ratio(self._current_image, w, h)
            self.canvas.show_image(self._cropped_image)
            self.app.log.success(f"Applied {ratio_str} ratio crop.")
        except Exception as e:
            messagebox.showerror("Error", f"Could not apply ratio: {str(e)}")

    def _apply_crop(self):
        """Apply free-form crop from canvas selection."""
        if not self._current_image:
            messagebox.showwarning("Warning", "Please load an image first.")
            return

        coords = self.canvas.get_crop_coords()
        if not coords:
            messagebox.showwarning("Warning", "Please select a crop area on the canvas.")
            return

        try:
            x1, y1, x2, y2 = coords
            self._cropped_image = ImageCropper.crop(self._current_image, x1, y1, x2, y2)
            self.canvas.show_image(self._cropped_image)
            self.app.log.success(f"Crop applied: {self._cropped_image.size[0]}×{self._cropped_image.size[1]} px")
        except Exception as e:
            messagebox.showerror("Error", f"Crop failed: {str(e)}")

    def _reset(self):
        """Reset to original image."""
        if self._current_image:
            self._cropped_image = None
            self.canvas.show_image(self._current_image)
            self.coord_label.config(text="Crop: Not selected")
            self.app.log.info("Crop reset to original.")

    def _save_cropped(self):
        """Save cropped image."""
        img = self._cropped_image or self._current_image
        if not img:
            messagebox.showwarning("Warning", "No image to save.")
            return

        path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"), ("All files", "*.*")]
        )
        if path:
            try:
                img.save(path)
                self.app.log.success(f"Cropped image saved: {os.path.basename(path)}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save: {str(e)}")
