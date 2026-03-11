"""
Image Converter Pro — Image canvas widget.
Displays images with auto-fit, zoom, and crop selection.
"""

import tkinter as tk
from PIL import Image, ImageTk


class ImageCanvas(tk.Canvas):
    """Canvas for displaying images with crop selection support.

    Features:
        - Auto-fit image to canvas size
        - Mouse-based crop area selection
        - Coordinate mapping (canvas -> original image)
    """

    def __init__(self, parent, width=500, height=400, **kwargs):
        """Create ImageCanvas.

        Args:
            parent: Parent widget
            width: Canvas width
            height: Canvas height
        """
        super().__init__(parent, width=width, height=height,
                        bg="#1e293b", highlightthickness=0, **kwargs)

        self._image = None
        self._photo = None
        self._original_size = None

        # Crop selection
        self._crop_rect = None
        self._crop_start = None
        self._crop_coords = None
        self._on_crop_callback = None

        # Mouse events for crop
        self.bind("<ButtonPress-1>", self._on_mouse_down)
        self.bind("<B1-Motion>", self._on_mouse_drag)
        self.bind("<ButtonRelease-1>", self._on_mouse_up)

    def show_image(self, img):
        """Display image on canvas with auto-fit.

        Args:
            img: PIL Image to display
        """
        self._image = img.copy()
        self._original_size = img.size

        # Scale to fit canvas
        canvas_w = self.winfo_width() or 500
        canvas_h = self.winfo_height() or 400

        img_copy = img.copy()
        img_copy.thumbnail((canvas_w, canvas_h), Image.Resampling.LANCZOS)

        self._photo = ImageTk.PhotoImage(img_copy)
        self.delete("all")

        # Center on canvas
        x = (canvas_w - img_copy.width) // 2
        y = (canvas_h - img_copy.height) // 2

        self.create_image(x, y, image=self._photo, anchor="nw", tags="image")
        self._display_offset = (x, y)
        self._display_size = (img_copy.width, img_copy.height)

    def clear(self):
        """Clear canvas."""
        self.delete("all")
        self._image = None
        self._photo = None
        self._crop_coords = None

    def set_crop_callback(self, callback):
        """Set callback for crop selection.

        Args:
            callback: Function(x1, y1, x2, y2) in original image coordinates
        """
        self._on_crop_callback = callback

    def get_crop_coords(self):
        """Get crop coordinates in original image space.

        Returns:
            tuple: (x1, y1, x2, y2) or None
        """
        return self._crop_coords

    # ========== Mouse events ==========

    def _on_mouse_down(self, event):
        """Start crop selection."""
        if not self._image:
            return
        self._crop_start = (event.x, event.y)
        if self._crop_rect:
            self.delete(self._crop_rect)

    def _on_mouse_drag(self, event):
        """Update crop selection rectangle."""
        if not self._crop_start or not self._image:
            return

        if self._crop_rect:
            self.delete(self._crop_rect)

        x1, y1 = self._crop_start
        self._crop_rect = self.create_rectangle(
            x1, y1, event.x, event.y,
            outline="#3b82f6", width=2, dash=(5, 3)
        )

    def _on_mouse_up(self, event):
        """Finish crop selection and calculate coordinates."""
        if not self._crop_start or not self._image:
            return

        x1, y1 = self._crop_start
        x2, y2 = event.x, event.y

        # Convert to original image coordinates
        if hasattr(self, "_display_offset") and hasattr(self, "_display_size"):
            ox, oy = self._display_offset
            dw, dh = self._display_size
            ow, oh = self._original_size

            # Scale factors
            sx = ow / dw if dw > 0 else 1
            sy = oh / dh if dh > 0 else 1

            # Convert
            img_x1 = int((min(x1, x2) - ox) * sx)
            img_y1 = int((min(y1, y2) - oy) * sy)
            img_x2 = int((max(x1, x2) - ox) * sx)
            img_y2 = int((max(y1, y2) - oy) * sy)

            # Clamp to image bounds
            img_x1 = max(0, img_x1)
            img_y1 = max(0, img_y1)
            img_x2 = min(ow, img_x2)
            img_y2 = min(oh, img_y2)

            self._crop_coords = (img_x1, img_y1, img_x2, img_y2)

            if self._on_crop_callback:
                self._on_crop_callback(img_x1, img_y1, img_x2, img_y2)

        self._crop_start = None
