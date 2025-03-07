import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from PIL import Image, ImageEnhance, ImageFilter, ImageOps, ImageDraw, ImageFont
import os
import threading
import queue
import time
from datetime import datetime
import json
import subprocess
import sys

class ImageConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Converter Pro")
        self.root.geometry("800x900")

        # Define colors and styles
        self.primary_color = "#3498db"  # Blue
        self.secondary_color = "#2ecc71"  # Green
        self.bg_color = "#f5f5f5"  # Light gray
        self.text_color = "#2c3e50"  # Dark gray

        self.setup_theme()

        # Initialize variables
        self.image_paths = []
        self.processed_count = 0
        self.queue = queue.Queue()
        self.processing = False

        # Main container
        main_frame = ttk.Frame(root)
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)

        # Create notebook (tabs)
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill="both", expand=True, padx=5, pady=5)

        # Define tabs
        self.main_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.main_tab, text="Main")

        self.effects_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.effects_tab, text="Advanced Effects")

        self.batch_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.batch_tab, text="Batch Processing")

        self.log_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.log_tab, text="Log")

        # Create UI sections
        self.create_file_section(self.main_tab)
        self.create_conversion_section(self.main_tab)
        self.create_basic_effects_section(self.main_tab)
        self.create_advanced_effects_section(self.effects_tab)
        self.create_batch_section(self.batch_tab)
        self.create_log_section(self.log_tab)
        self.create_process_section(self.main_tab)

    # Theme Configuration
    def setup_theme(self):
        style = ttk.Style()
        style.theme_use("clam")

        # Button style
        style.configure(
            "TButton",
            background=self.primary_color,
            foreground="white",
            font=("Helvetica", 10, "bold"),
            padding=8,
            relief="flat"
        )
        style.map(
            "TButton",
            background=[("active", self.secondary_color), ("disabled", "#cccccc")]
        )

        # Label style
        style.configure(
            "TLabel",
            font=("Helvetica", 10),
            foreground=self.text_color,
            background=self.bg_color,
            padding=3
        )

        # Frame style
        style.configure(
            "TFrame",
            background=self.bg_color,
            padding=5
        )

        # LabelFrame style
        style.configure(
            "TLabelframe",
            background=self.bg_color,
            padding=10,
            font=("Helvetica", 10, "bold")
        )
        style.configure(
            "TLabelframe.Label",
            foreground=self.primary_color,
            background=self.bg_color,
            font=("Helvetica", 11, "bold")
        )

        # Notebook style
        style.configure(
            "TNotebook",
            background=self.bg_color,
            tabposition="n"
        )
        style.configure(
            "TNotebook.Tab",
            font=("Helvetica", 10, "bold"),
            padding=[12, 4],
            background=self.bg_color,
            foreground=self.text_color
        )
        style.map(
            "TNotebook.Tab",
            background=[("selected", self.primary_color)],
            foreground=[("selected", "white")]
        )

        # OptionMenu style
        style.configure(
            "TMenubutton",
            background="white",
            padding=5,
            relief="flat"
        )

        # Progressbar style
        style.configure(
            "Horizontal.TProgressbar",
            troughcolor="#e0e0e0",
            background=self.secondary_color
        )

        # Set window background
        self.root.configure(background=self.bg_color)

    # File Selection Section
    def create_file_section(self, parent):
        file_frame = ttk.LabelFrame(parent, text="File Selection")
        file_frame.pack(fill="x", pady=10)

        button_frame = ttk.Frame(file_frame)
        button_frame.pack(fill="x", pady=5)

        self.select_button = ttk.Button(button_frame, text="Select Image(s)", command=self.select_images)
        self.select_button.pack(side="left", padx=5)

        self.clear_button = ttk.Button(button_frame, text="Clear", command=self.clear_selection)
        self.clear_button.pack(side="left", padx=5)

        self.preview_button = ttk.Button(button_frame, text="Preview", command=self.preview_image, state="disabled")
        self.preview_button.pack(side="right", padx=5)

        # File listbox
        list_frame = ttk.Frame(file_frame)
        list_frame.pack(fill="both", expand=True, pady=5)

        self.file_listbox = tk.Listbox(list_frame, height=4, selectmode=tk.SINGLE, bg="white", bd=1,
                                      highlightthickness=1, highlightbackground="#cccccc")
        self.file_listbox.pack(side="left", fill="both", expand=True)
        self.file_listbox.bind("<<ListboxSelect>>", self.on_file_select)

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.file_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.file_listbox.config(yscrollcommand=scrollbar.set)

        self.file_label = ttk.Label(file_frame, text="Selected files: 0")
        self.file_label.pack(pady=5, anchor="w")

    # Conversion Settings Section
    def create_conversion_section(self, parent):
        conv_frame = ttk.LabelFrame(parent, text="Conversion Settings")
        conv_frame.pack(fill="x", pady=10)

        # Two-column layout
        left_frame = ttk.Frame(conv_frame)
        left_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        right_frame = ttk.Frame(conv_frame)
        right_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)

        # Left column elements
        # Format
        format_frame = ttk.Frame(left_frame)
        format_frame.pack(fill="x", pady=3)
        ttk.Label(format_frame, text="Output Format:").pack(side="left")
        self.formats = ["JPEG", "PNG", "BMP", "GIF", "TIFF", "WEBP"]
        self.format_var = tk.StringVar(value="JPEG")
        ttk.OptionMenu(format_frame, self.format_var, *self.formats).pack(side="right")

        # Resize
        resize_frame = ttk.Frame(left_frame)
        resize_frame.pack(fill="x", pady=3)
        ttk.Label(resize_frame, text="Size (Width x Height):").pack(side="left")

        size_frame = ttk.Frame(resize_frame)
        size_frame.pack(side="right")

        self.width_entry = ttk.Entry(size_frame, width=6)
        self.width_entry.insert(0, "800")
        self.width_entry.pack(side="left", padx=2)

        ttk.Label(size_frame, text="x").pack(side="left", padx=2)

        self.height_entry = ttk.Entry(size_frame, width=6)
        self.height_entry.insert(0, "600")
        self.height_entry.pack(side="left", padx=2)

        self.maintain_ratio_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(left_frame, text="Maintain Aspect Ratio", variable=self.maintain_ratio_var).pack(anchor="w", pady=3)

        # Right column elements
        # Rotate
        rotate_frame = ttk.Frame(right_frame)
        rotate_frame.pack(fill="x", pady=3)
        ttk.Label(rotate_frame, text="Rotate:").pack(side="left")
        self.rotate_var = tk.StringVar(value="0")
        rotate_options = ["0", "90", "180", "270", "Custom"]
        ttk.OptionMenu(rotate_frame, self.rotate_var, *rotate_options, command=self.toggle_rotate_entry).pack(side="right")

        custom_rotate_frame = ttk.Frame(right_frame)
        custom_rotate_frame.pack(fill="x", pady=3)
        ttk.Label(custom_rotate_frame, text="Angle (degrees):").pack(side="left")
        self.rotate_entry = ttk.Entry(custom_rotate_frame, width=6, state="disabled")
        self.rotate_entry.insert(0, "0")
        self.rotate_entry.pack(side="right")

        # Quality
        quality_frame = ttk.Frame(right_frame)
        quality_frame.pack(fill="x", pady=3)
        ttk.Label(quality_frame, text="Quality (1-100):").pack(side="left")

        self.quality_var = tk.IntVar(value=85)
        quality_scale = ttk.Scale(quality_frame, from_=1, to=100, variable=self.quality_var,
                                  orient="horizontal", command=self.update_quality_label)
        quality_scale.pack(side="left", fill="x", expand=True, padx=5)

        self.quality_label = ttk.Label(quality_frame, text="85")
        self.quality_label.pack(side="right", padx=5)

    # Basic Effects Section
    def create_basic_effects_section(self, parent):
        effect_frame = ttk.LabelFrame(parent, text="Basic Effects")
        effect_frame.pack(fill="x", pady=10)

        # Two-column layout
        left_frame = ttk.Frame(effect_frame)
        left_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        right_frame = ttk.Frame(effect_frame)
        right_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)

        # Brightness
        brightness_frame = ttk.Frame(left_frame)
        brightness_frame.pack(fill="x", pady=5)
        ttk.Label(brightness_frame, text="Brightness:").pack(side="left")
        self.brightness_var = tk.DoubleVar(value=1.0)
        brightness_scale = ttk.Scale(brightness_frame, from_=0, to=2, variable=self.brightness_var,
                                     orient="horizontal", command=self.update_brightness_label)
        brightness_scale.pack(side="left", fill="x", expand=True, padx=5)
        self.brightness_label = ttk.Label(brightness_frame, text="1.0")
        self.brightness_label.pack(side="right", padx=5)

        # Contrast
        contrast_frame = ttk.Frame(right_frame)
        contrast_frame.pack(fill="x", pady=5)
        ttk.Label(contrast_frame, text="Contrast:").pack(side="left")
        self.contrast_var = tk.DoubleVar(value=1.0)
        contrast_scale = ttk.Scale(contrast_frame, from_=0, to=2, variable=self.contrast_var,
                                   orient="horizontal", command=self.update_contrast_label)
        contrast_scale.pack(side="left", fill="x", expand=True, padx=5)
        self.contrast_label = ttk.Label(contrast_frame, text="1.0")
        self.contrast_label.pack(side="right", padx=5)

    # Advanced Effects Section
    def create_advanced_effects_section(self, parent):
        adv_effect_frame = ttk.LabelFrame(parent, text="Advanced Effects")
        adv_effect_frame.pack(fill="x", pady=10)

        # Filter options
        filter_frame = ttk.Frame(adv_effect_frame)
        filter_frame.pack(fill="x", pady=5)

        ttk.Label(filter_frame, text="Filters:").grid(row=0, column=0, sticky="w", pady=5)

        self.blur_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(filter_frame, text="Blur", variable=self.blur_var).grid(row=0, column=1, padx=10)

        self.sharpen_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(filter_frame, text="Sharpen", variable=self.sharpen_var).grid(row=0, column=2, padx=10)

        self.edge_enhance_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(filter_frame, text="Edge Enhance", variable=self.edge_enhance_var).grid(row=0, column=3, padx=10)

        self.emboss_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(filter_frame, text="Emboss", variable=self.emboss_var).grid(row=1, column=1, padx=10)

        self.contour_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(filter_frame, text="Contour", variable=self.contour_var).grid(row=1, column=2, padx=10)

        self.grayscale_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(filter_frame, text="Grayscale", variable=self.grayscale_var).grid(row=1, column=3, padx=10)

        # Saturation
        saturation_frame = ttk.Frame(adv_effect_frame)
        saturation_frame.pack(fill="x", pady=5)

        ttk.Label(saturation_frame, text="Saturation:").pack(side="left")
        self.saturation_var = tk.DoubleVar(value=1.0)
        saturation_scale = ttk.Scale(saturation_frame, from_=0, to=2, variable=self.saturation_var,
                                     orient="horizontal", command=self.update_saturation_label)
        saturation_scale.pack(side="left", fill="x", expand=True, padx=5)
        self.saturation_label = ttk.Label(saturation_frame, text="1.0")
        self.saturation_label.pack(side="right", padx=5)

        # Sharpness
        sharpness_frame = ttk.Frame(adv_effect_frame)
        sharpness_frame.pack(fill="x", pady=5)

        ttk.Label(sharpness_frame, text="Sharpness:").pack(side="left")
        self.sharpness_var = tk.DoubleVar(value=1.0)
        sharpness_scale = ttk.Scale(sharpness_frame, from_=0, to=2, variable=self.sharpness_var,
                                    orient="horizontal", command=self.update_sharpness_label)
        sharpness_scale.pack(side="left", fill="x", expand=True, padx=5)
        self.sharpness_label = ttk.Label(sharpness_frame, text="1.0")
        self.sharpness_label.pack(side="right", padx=5)

        # Watermark
        watermark_frame = ttk.LabelFrame(parent, text="Watermark")
        watermark_frame.pack(fill="x", pady=10)

        self.watermark_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(watermark_frame, text="Add Watermark", variable=self.watermark_var).pack(anchor="w", pady=5)

        text_frame = ttk.Frame(watermark_frame)
        text_frame.pack(fill="x", pady=5)

        ttk.Label(text_frame, text="Text:").pack(side="left")
        self.watermark_text = ttk.Entry(text_frame, width=30)
        self.watermark_text.insert(0, "© Copyright")
        self.watermark_text.pack(side="left", padx=5, fill="x", expand=True)

        position_frame = ttk.Frame(watermark_frame)
        position_frame.pack(fill="x", pady=5)

        ttk.Label(position_frame, text="Position:").pack(side="left")
        self.watermark_position = tk.StringVar(value="bottom-right")
        positions = ["top-left", "top-right", "bottom-left", "bottom-right", "center"]
        ttk.OptionMenu(position_frame, self.watermark_position, *positions).pack(side="left", padx=5)

        ttk.Label(position_frame, text="Opacity:").pack(side="left", padx=10)
        self.watermark_opacity = tk.DoubleVar(value=0.5)
        opacity_scale = ttk.Scale(position_frame, from_=0.1, to=1.0, variable=self.watermark_opacity,
                                  orient="horizontal", command=self.update_opacity_label)
        opacity_scale.pack(side="left", fill="x", expand=True, padx=5)
        self.opacity_label = ttk.Label(position_frame, text="0.5")
        self.opacity_label.pack(side="right", padx=5)

    # Batch Processing Section
    def create_batch_section(self, parent):
        batch_frame = ttk.LabelFrame(parent, text="Batch Processing")
        batch_frame.pack(fill="both", expand=True, pady=10)

        # Preset management
        preset_frame = ttk.Frame(batch_frame)
        preset_frame.pack(fill="x", pady=10)

        ttk.Label(preset_frame, text="Presets:").pack(side="left", padx=5)
        self.preset_name = ttk.Entry(preset_frame, width=20)
        self.preset_name.pack(side="left", padx=5)

        self.save_preset_button = ttk.Button(preset_frame, text="Save", command=self.save_preset)
        self.save_preset_button.pack(side="left", padx=5)

        self.load_preset_button = ttk.Button(preset_frame, text="Load", command=self.load_preset)
        self.load_preset_button.pack(side="left", padx=5)

        # Batch operations
        operations_frame = ttk.LabelFrame(batch_frame, text="Operations")
        operations_frame.pack(fill="both", expand=True, pady=10)

        self.rename_var = tk.BooleanVar(value=False)
        rename_frame = ttk.Frame(operations_frame)
        rename_frame.pack(fill="x", pady=5)

        ttk.Checkbutton(rename_frame, text="Rename:", variable=self.rename_var).pack(side="left")

        self.rename_pattern = ttk.Entry(rename_frame, width=20)
        self.rename_pattern.insert(0, "image_{num}")
        self.rename_pattern.pack(side="left", padx=5, fill="x", expand=True)

        ttk.Label(rename_frame, text="{num} - number, {orig} - original name").pack(side="right", padx=5)

        # Operations listbox
        operations_list_frame = ttk.Frame(operations_frame)
        operations_list_frame.pack(fill="both", expand=True, pady=5)

        self.operations_listbox = tk.Listbox(operations_list_frame, height=5, bg="white", bd=1,
                                             highlightthickness=1, highlightbackground="#cccccc")
        self.operations_listbox.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(operations_list_frame, orient="vertical", command=self.operations_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.operations_listbox.config(yscrollcommand=scrollbar.set)

        # Update operations list
        self.update_operations_list()

    # Log Section
    def create_log_section(self, parent):
        log_frame = ttk.LabelFrame(parent, text="Processing Log")
        log_frame.pack(fill="both", expand=True, pady=10)

        self.log_text = scrolledtext.ScrolledText(log_frame, height=20, width=70, wrap=tk.WORD)
        self.log_text.pack(fill="both", expand=True, pady=5)
        self.log_text.config(state="disabled")

        button_frame = ttk.Frame(log_frame)
        button_frame.pack(fill="x", pady=5)

        self.clear_log_button = ttk.Button(button_frame, text="Clear Log", command=self.clear_log)
        self.clear_log_button.pack(side="left", padx=5)

        self.save_log_button = ttk.Button(button_frame, text="Save Log", command=self.save_log)
        self.save_log_button.pack(side="left", padx=5)

    # Process Section
    def create_process_section(self, parent):
        process_frame = ttk.Frame(parent)
        process_frame.pack(fill="x", pady=10)

        # Button row
        button_frame = ttk.Frame(process_frame)
        button_frame.pack(fill="x", pady=5)

        self.process_button = ttk.Button(button_frame, text="Process and Save", command=self.start_processing)
        self.process_button.pack(side="left", padx=5)

        self.cancel_button = ttk.Button(button_frame, text="Cancel", command=self.cancel_processing, state="disabled")
        self.cancel_button.pack(side="left", padx=5)

        self.open_folder_button = ttk.Button(button_frame, text="Open Folder", command=self.open_output_folder, state="disabled")
        self.open_folder_button.pack(side="right", padx=5)

        # Progress bar
        self.progress = ttk.Progressbar(process_frame, mode="determinate")
        self.progress.pack(fill="x", pady=5)

        # Status frame
        status_frame = ttk.Frame(process_frame)
        status_frame.pack(fill="x", pady=5)

        self.status_label = ttk.Label(status_frame, text="Status: Ready")
        self.status_label.pack(side="left")

        self.time_label = ttk.Label(status_frame, text="")
        self.time_label.pack(side="right")

    # Update Label Functions
    def update_quality_label(self, event=None):
        self.quality_label.config(text=str(self.quality_var.get()))

    def update_brightness_label(self, event=None):
        self.brightness_label.config(text=f"{self.brightness_var.get():.1f}")

    def update_contrast_label(self, event=None):
        self.contrast_label.config(text=f"{self.contrast_var.get():.1f}")

    def update_saturation_label(self, event=None):
        self.saturation_label.config(text=f"{self.saturation_var.get():.1f}")

    def update_sharpness_label(self, event=None):
        self.sharpness_label.config(text=f"{self.sharpness_var.get():.1f}")

    def update_opacity_label(self, event=None):
        self.opacity_label.config(text=f"{self.watermark_opacity.get():.1f}")

    # Utility Functions
    def toggle_rotate_entry(self, value):
        if value == "Custom":
            self.rotate_entry.config(state="normal")
        else:
            self.rotate_entry.config(state="disabled")
            self.rotate_entry.delete(0, tk.END)
            self.rotate_entry.insert(0, value)

    def select_images(self):
        new_paths = filedialog.askopenfilenames(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif *.tiff *.webp")]
        )
        if new_paths:
            self.image_paths.extend(new_paths)
            self.update_file_list()
            self.log(f"{len(new_paths)} image(s) selected.")

    def update_file_list(self):
        self.file_listbox.delete(0, tk.END)
        for path in self.image_paths:
            filename = os.path.basename(path)
            self.file_listbox.insert(tk.END, filename)

        self.file_label.config(text=f"Selected files: {len(self.image_paths)}")

        if len(self.image_paths) > 0:
            self.preview_button.config(state="normal")
        else:
            self.preview_button.config(state="disabled")

    def on_file_select(self, event=None):
        if self.file_listbox.curselection():
            self.preview_button.config(state="normal")
        else:
            self.preview_button.config(state="disabled")

    def clear_selection(self):
        self.image_paths = []
        self.update_file_list()
        self.log("Selected files cleared.")

    def preview_image(self):
        try:
            if not self.file_listbox.curselection():
                messagebox.showwarning("Warning", "Please select an image to preview.")
                return

            selected_index = self.file_listbox.curselection()[0]
            selected_path = self.image_paths[selected_index]

            # Create preview window
            preview_window = tk.Toplevel(self.root)
            preview_window.title(f"Preview: {os.path.basename(selected_path)}")
            preview_window.geometry("600x500")

            # Main container
            frame = ttk.Frame(preview_window, padding=10)
            frame.pack(fill="both", expand=True)

            # Load and resize image
            img = Image.open(selected_path)
            img.thumbnail((500, 400))

            # Convert to PhotoImage
            from PIL import ImageTk
            photo = ImageTk.PhotoImage(img)

            # Display image
            img_label = ttk.Label(frame, image=photo)
            img_label.image = photo  # Keep reference
            img_label.pack(pady=10)

            # Image info
            info_text = (
                f"File name: {os.path.basename(selected_path)}\n"
                f"Size: {img.width}x{img.height} pixels\n"
                f"Format: {img.format}\n"
                f"Mode: {img.mode}"
            )

            info_label = ttk.Label(frame, text=info_text, justify="left")
            info_label.pack(pady=10)

            ttk.Button(frame, text="Close", command=preview_window.destroy).pack(pady=10)

        except Exception as e:
            messagebox.showerror("Error", f"Error previewing image: {str(e)}")

    # Processing Functions
    def start_processing(self):
        if not self.image_paths:
            messagebox.showerror("Error", "Please select at least one image!")
            return

        save_dir = filedialog.askdirectory(title="Select Save Folder")
        if not save_dir:
            return

        self.output_dir = save_dir
        self.processing = True
        self.processed_count = 0
        self.start_time = time.time()

        # Update UI elements
        self.process_button.config(state="disabled")
        self.cancel_button.config(state="normal")
        self.status_label.config(text="Status: Processing...")
        self.progress["maximum"] = len(self.image_paths)
        self.progress["value"] = 0

        # Log start of processing
        self.log(f"Processing started. {len(self.image_paths)} image(s).")

        # Start processing in a separate thread
        threading.Thread(target=self.process_images, args=(save_dir,), daemon=True).start()

        # Schedule queue check
        self.root.after(100, self.check_queue)

    def process_images(self, save_dir):
        try:
            for i, image_path in enumerate(self.image_paths):
                if not self.processing:  # Check for cancellation
                    break

                # Send status update to queue
                self.queue.put(("status", f"Processing: {os.path.basename(image_path)}"))
                self.queue.put(("progress", i))

                # Process the image
                self.process_single_image(image_path, save_dir, i + 1)

                self.processed_count += 1

            # Signal completion
            self.queue.put(("complete", None))

        except Exception as e:
            self.queue.put(("error", str(e)))

    def process_single_image(self, image_path, save_dir, num):
        try:
            # Load image
            img = Image.open(image_path)
            original_format = img.format

            # Resize
            if self.width_entry.get() and self.height_entry.get():
                try:
                    width = int(self.width_entry.get())
                    height = int(self.height_entry.get())

                    if self.maintain_ratio_var.get():
                        img.thumbnail((width, height), Image.Resampling.LANCZOS)
                    else:
                        img = img.resize((width, height), Image.Resampling.LANCZOS)
                except ValueError:
                    self.log(f"Error: Size must be valid numbers: {image_path}")

            # Rotate
            if self.rotate_var.get() != "0":
                if self.rotate_var.get() == "Custom":
                    try:
                        angle = float(self.rotate_entry.get())
                        img = img.rotate(angle, expand=True)
                    except ValueError:
                        self.log(f"Error: Rotation angle must be a valid number: {image_path}")
                else:
                    angle = int(self.rotate_var.get())
                    img = img.rotate(angle, expand=True)

            # Basic effects
            if self.brightness_var.get() != 1.0:
                enhancer = ImageEnhance.Brightness(img)
                img = enhancer.enhance(self.brightness_var.get())

            if self.contrast_var.get() != 1.0:
                enhancer = ImageEnhance.Contrast(img)
                img = enhancer.enhance(self.contrast_var.get())

            # Advanced effects
            if self.saturation_var.get() != 1.0:
                enhancer = ImageEnhance.Color(img)
                img = enhancer.enhance(self.saturation_var.get())

            if self.sharpness_var.get() != 1.0:
                enhancer = ImageEnhance.Sharpness(img)
                img = enhancer.enhance(self.sharpness_var.get())

            # Filters
            if self.blur_var.get():
                img = img.filter(ImageFilter.BLUR)

            if self.sharpen_var.get():
                img = img.filter(ImageFilter.SHARPEN)

            if self.edge_enhance_var.get():
                img = img.filter(ImageFilter.EDGE_ENHANCE)

            if self.emboss_var.get():
                img = img.filter(ImageFilter.EMBOSS)

            if self.contour_var.get():
                img = img.filter(ImageFilter.CONTOUR)

            if self.grayscale_var.get():
                img = ImageOps.grayscale(img)

            # Watermark
            if self.watermark_var.get() and self.watermark_text.get():
                img = self.add_watermark(img)

            # Convert to RGB if saving as JPEG or WEBP to avoid RGBA issue
            if self.format_var.get() in ["JPEG", "WEBP"] and img.mode == "RGBA":
                img = img.convert("RGB")

            # Save file
            output_filename = self.get_output_filename(image_path, num, save_dir)

            save_options = {}
            if self.format_var.get() in ["JPEG", "WEBP"]:
                save_options["quality"] = self.quality_var.get()

            img.save(output_filename, format=self.format_var.get(), **save_options)

            self.log(f"Saved: {os.path.basename(output_filename)}")

        except Exception as e:
            self.log(f"Error: {os.path.basename(image_path)} - {str(e)}")
            raise
    def add_watermark(self, img):
        # Create a copy for watermarking
        watermark_img = img.copy().convert("RGBA")

        # Transparent overlay
        overlay = Image.new('RGBA', watermark_img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        # Select font
        try:
            font_size = min(watermark_img.width, watermark_img.height) // 20
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()

        # Text dimensions
        text = self.watermark_text.get()
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        # Position watermark
        position = self.watermark_position.get()
        padding = 10

        if position == "top-left":
            pos = (padding, padding)
        elif position == "top-right":
            pos = (watermark_img.width - text_width - padding, padding)
        elif position == "bottom-left":
            pos = (padding, watermark_img.height - text_height - padding)
        elif position == "bottom-right":
            pos = (watermark_img.width - text_width - padding, watermark_img.height - text_height - padding)
        else:  # center
            pos = ((watermark_img.width - text_width) // 2, (watermark_img.height - text_height) // 2)

        # Draw watermark
        opacity = int(self.watermark_opacity.get() * 255)
        draw.text(pos, text, fill=(255, 255, 255, opacity), font=font)

        # Combine watermark with image
        result = Image.alpha_composite(watermark_img, overlay)

        # Convert back to original mode if needed
        if img.mode != 'RGBA':
            result = result.convert(img.mode)

        return result

    def get_output_filename(self, input_path, num, save_dir):
        original_filename = os.path.splitext(os.path.basename(input_path))[0]

        if self.rename_var.get() and self.rename_pattern.get():
            pattern = self.rename_pattern.get()
            filename = pattern.replace("{num}", f"{num:03d}").replace("{orig}", original_filename)
        else:
            filename = f"{original_filename}"

        extension = self.format_var.get().lower()
        if extension == "jpeg":
            extension = "jpg"

        return os.path.join(save_dir, f"{filename}.{extension}")

    def check_queue(self):
        try:
            while True:
                message_type, message = self.queue.get_nowait()

                if message_type == "status":
                    self.status_label.config(text=f"Status: {message}")

                elif message_type == "progress":
                    self.progress["value"] = message + 1
                    elapsed_time = time.time() - self.start_time
                    remaining = (elapsed_time / (message + 1)) * (len(self.image_paths) - message - 1)
                    self.time_label.config(text=f"Elapsed time: {int(elapsed_time)}s | Remaining: {int(remaining)}s")

                elif message_type == "complete":
                    self.process_complete()

                elif message_type == "error":
                    messagebox.showerror("Error", f"Processing error: {message}")
                    self.cancel_processing()

                self.queue.task_done()

        except queue.Empty:
            if self.processing:
                self.root.after(100, self.check_queue)

    def process_complete(self):
        elapsed_time = time.time() - self.start_time
        self.log(f"Processing completed. {self.processed_count} image(s). Time: {elapsed_time:.1f} seconds.")

        self.status_label.config(text=f"Status: Completed ({self.processed_count}/{len(self.image_paths)})")
        self.time_label.config(text=f"Total time: {int(elapsed_time)}s")

        self.process_button.config(state="normal")
        self.cancel_button.config(state="disabled")
        self.open_folder_button.config(state="normal")

        self.processing = False

        if self.processed_count > 0:
            messagebox.showinfo("Info", f"Processing completed. {self.processed_count} image(s) saved.")

    def cancel_processing(self):
        self.processing = False
        self.log("Processing canceled.")
        self.status_label.config(text="Status: Canceled")
        self.process_button.config(state="normal")
        self.cancel_button.config(state="disabled")

    def open_output_folder(self):
        if hasattr(self, 'output_dir'):
            try:
                if sys.platform == 'win32':
                    os.startfile(self.output_dir)
                elif sys.platform == 'darwin':  # macOS
                    subprocess.Popen(['open', self.output_dir])
                else:  # Linux
                    subprocess.Popen(['xdg-open', self.output_dir])
            except Exception as e:
                messagebox.showerror("Error", f"Error opening folder: {str(e)}")
        else:
            messagebox.showwarning("Warning", "Save folder not available.")

    # Log Functions
    def log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"

        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        self.log_text.config(state="disabled")

    def clear_log(self):
        self.log_text.config(state="normal")
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state="disabled")
        self.log("Log cleared.")

    def save_log(self):
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            if filename:
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(self.log_text.get(1.0, tk.END))
                self.log(f"Log saved: {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Error saving log: {str(e)}")

    # Batch Operations
    def update_operations_list(self):
        self.operations_listbox.delete(0, tk.END)

        if self.width_entry.get() and self.height_entry.get():
            size_text = f"Resize: {self.width_entry.get()}x{self.height_entry.get()}"
            if self.maintain_ratio_var.get():
                size_text += " (proportional)"
            self.operations_listbox.insert(tk.END, size_text)

        self.operations_listbox.insert(tk.END, f"Format: {self.format_var.get()}")

        if self.rotate_var.get() != "0":
            rotate_angle = self.rotate_entry.get() if self.rotate_var.get() == "Custom" else self.rotate_var.get()
            self.operations_listbox.insert(tk.END, f"Rotate: {rotate_angle}°")

        if self.brightness_var.get() != 1.0:
            self.operations_listbox.insert(tk.END, f"Brightness: {self.brightness_var.get():.1f}")

        if self.contrast_var.get() != 1.0:
            self.operations_listbox.insert(tk.END, f"Contrast: {self.contrast_var.get():.1f}")

        active_filters = []
        if self.blur_var.get(): active_filters.append("Blur")
        if self.sharpen_var.get(): active_filters.append("Sharpen")
        if self.edge_enhance_var.get(): active_filters.append("Edge Enhance")
        if self.emboss_var.get(): active_filters.append("Emboss")
        if self.contour_var.get(): active_filters.append("Contour")
        if self.grayscale_var.get(): active_filters.append("Grayscale")

        if active_filters:
            self.operations_listbox.insert(tk.END, f"Filters: {', '.join(active_filters)}")

        if self.watermark_var.get():
            self.operations_listbox.insert(tk.END, f"Watermark: '{self.watermark_text.get()}'")

        if self.rename_var.get():
            self.operations_listbox.insert(tk.END, f"Rename: {self.rename_pattern.get()}")

    def save_preset(self):
        preset_name = self.preset_name.get()
        if not preset_name:
            messagebox.showwarning("Warning", "Please enter a preset name.")
            return

        preset = {
            "format": self.format_var.get(),
            "width": self.width_entry.get(),
            "height": self.height_entry.get(),
            "maintain_ratio": self.maintain_ratio_var.get(),
            "rotate": self.rotate_var.get(),
            "rotate_custom": self.rotate_entry.get(),
            "quality": self.quality_var.get(),
            "brightness": self.brightness_var.get(),
            "contrast": self.contrast_var.get(),
            "saturation": self.saturation_var.get(),
            "sharpness": self.sharpness_var.get(),
            "blur": self.blur_var.get(),
            "sharpen": self.sharpen_var.get(),
            "edge_enhance": self.edge_enhance_var.get(),
            "emboss": self.emboss_var.get(),
            "contour": self.contour_var.get(),
            "grayscale": self.grayscale_var.get(),
            "watermark": self.watermark_var.get(),
            "watermark_text": self.watermark_text.get(),
            "watermark_position": self.watermark_position.get(),
            "watermark_opacity": self.watermark_opacity.get(),
            "rename": self.rename_var.get(),
            "rename_pattern": self.rename_pattern.get()
        }

        try:
            presets_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "presets")
            os.makedirs(presets_dir, exist_ok=True)

            preset_path = os.path.join(presets_dir, f"{preset_name}.json")
            with open(preset_path, "w", encoding="utf-8") as f:
                json.dump(preset, f, indent=4)

            self.log(f"Preset saved: {preset_name}")
            messagebox.showinfo("Info", f"Preset saved: {preset_name}")

        except Exception as e:
            messagebox.showerror("Error", f"Error saving preset: {str(e)}")

    def load_preset(self):
        try:
            presets_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "presets")
            if not os.path.exists(presets_dir):
                messagebox.showinfo("Info", "No presets found.")
                return

            preset_file = filedialog.askopenfilename(
                initialdir=presets_dir,
                title="Select Preset",
                filetypes=[("JSON files", "*.json")]
            )

            if not preset_file:
                return

            with open(preset_file, "r", encoding="utf-8") as f:
                preset = json.load(f)

            self.format_var.set(preset.get("format", "JPEG"))
            self.width_entry.delete(0, tk.END)
            self.width_entry.insert(0, preset.get("width", "800"))
            self.height_entry.delete(0, tk.END)
            self.height_entry.insert(0, preset.get("height", "600"))
            self.maintain_ratio_var.set(preset.get("maintain_ratio", True))
            self.rotate_var.set(preset.get("rotate", "0"))
            self.rotate_entry.delete(0, tk.END)
            self.rotate_entry.insert(0, preset.get("rotate_custom", "0"))
            self.quality_var.set(preset.get("quality", 85))
            self.brightness_var.set(preset.get("brightness", 1.0))
            self.contrast_var.set(preset.get("contrast", 1.0))
            self.saturation_var.set(preset.get("saturation", 1.0))
            self.sharpness_var.set(preset.get("sharpness", 1.0))
            self.blur_var.set(preset.get("blur", False))
            self.sharpen_var.set(preset.get("sharpen", False))
            self.edge_enhance_var.set(preset.get("edge_enhance", False))
            self.emboss_var.set(preset.get("emboss", False))
            self.contour_var.set(preset.get("contour", False))
            self.grayscale_var.set(preset.get("grayscale", False))
            self.watermark_var.set(preset.get("watermark", False))
            self.watermark_text.delete(0, tk.END)
            self.watermark_text.insert(0, preset.get("watermark_text", "© Copyright"))
            self.watermark_position.set(preset.get("watermark_position", "bottom-right"))
            self.watermark_opacity.set(preset.get("watermark_opacity", 0.5))
            self.rename_var.set(preset.get("rename", False))
            self.rename_pattern.delete(0, tk.END)
            self.rename_pattern.insert(0, preset.get("rename_pattern", "image_{num}"))

            self.toggle_rotate_entry(preset.get("rotate", "0"))

            self.update_quality_label()
            self.update_brightness_label()
            self.update_contrast_label()
            self.update_saturation_label()
            self.update_sharpness_label()
            self.update_opacity_label()

            self.update_operations_list()

            preset_name = os.path.splitext(os.path.basename(preset_file))[0]
            self.preset_name.delete(0, tk.END)
            self.preset_name.insert(0, preset_name)

            self.log(f"Preset loaded: {preset_name}")

        except Exception as e:
            messagebox.showerror("Error", f"Error loading preset: {str(e)}")

def main():
    root = tk.Tk()
    app = ImageConverterApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
