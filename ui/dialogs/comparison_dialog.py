"""
Image Converter Pro — Comparison dialog.
Side-by-side before/after image comparison.
"""

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


class ComparisonDialog:
    """Side-by-side image comparison dialog."""

    @staticmethod
    def show(parent, original, processed, title="Comparison"):
        """Show comparison dialog.

        Args:
            parent: Parent window
            original: Original PIL Image
            processed: Processed PIL Image
            title: Dialog title
        """
        dialog = tk.Toplevel(parent)
        dialog.title(title)
        dialog.geometry("800x450")
        dialog.transient(parent)

        # Title
        ttk.Label(dialog, text="Before / After Comparison",
                 font=("Segoe UI", 12, "bold")).pack(pady=5)

        # Image frames
        frames = ttk.Frame(dialog)
        frames.pack(fill="both", expand=True, padx=10, pady=5)

        # Original
        left = ttk.LabelFrame(frames, text="📷 Original")
        left.pack(side="left", fill="both", expand=True, padx=5)

        orig_copy = original.copy()
        orig_copy.thumbnail((380, 350), Image.Resampling.LANCZOS)
        orig_photo = ImageTk.PhotoImage(orig_copy)
        orig_label = ttk.Label(left, image=orig_photo)
        orig_label.image = orig_photo
        orig_label.pack(padx=5, pady=5)

        # Processed
        right = ttk.LabelFrame(frames, text="✨ Processed")
        right.pack(side="right", fill="both", expand=True, padx=5)

        proc_copy = processed.copy()
        proc_copy.thumbnail((380, 350), Image.Resampling.LANCZOS)
        proc_photo = ImageTk.PhotoImage(proc_copy)
        proc_label = ttk.Label(right, image=proc_photo)
        proc_label.image = proc_photo
        proc_label.pack(padx=5, pady=5)

        # Close button
        ttk.Button(dialog, text="Close", command=dialog.destroy).pack(pady=10)
