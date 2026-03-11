"""
Image Converter Pro — Main application window.
Orchestrates all components: menu, toolbar, tabs, status bar.
"""

import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import queue
import time
from PIL import Image, ImageTk

from config.constants import (
    APP_NAME, APP_VERSION, WINDOW_WIDTH, WINDOW_HEIGHT,
    WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT, SHORTCUTS, MAX_WORKERS,
    FONT_FAMILY, FONT_SIZE_NORMAL, FONT_SIZE_TITLE
)
from config.themes import ThemeManager

from core.converter import ImageConverter
from core.effects import EffectsEngine
from core.watermark import WatermarkEngine
from core.batch_processor import BatchProcessor
from core.preset_manager import PresetManager
from core.history import HistoryManager
from core.metadata import MetadataReader

from ui.tabs.main_tab import MainTab
from ui.tabs.effects_tab import EffectsTab
from ui.tabs.crop_tab import CropTab
from ui.tabs.batch_tab import BatchTab
from ui.tabs.log_tab import LogTab
from ui.widgets.toolbar import Toolbar
from ui.widgets.status_bar import StatusBar
from ui.dialogs.about_dialog import AboutDialog
from ui.dialogs.comparison_dialog import ComparisonDialog

from utils.logger import AppLogger
from utils.file_utils import open_folder
from utils.validators import ValidationError


class ImageConverterApp:
    """Main application window.

    Integrates all UI components and manages business logic.
    """

    def __init__(self, root):
        self.root = root
        self.root.title(f"{APP_NAME} v{APP_VERSION}")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.minsize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)

        # ========== Core components ==========
        self.image_paths = []
        self.output_dir = None
        self.processing = False
        self._queue = queue.Queue()

        # Managers
        self.log = AppLogger()
        self.theme_manager = ThemeManager()
        self.preset_manager = PresetManager()
        self.history = HistoryManager()
        self.converter = ImageConverter()
        self.effects_engine = EffectsEngine()
        self.watermark_engine = WatermarkEngine()
        self.batch_processor = BatchProcessor(max_workers=MAX_WORKERS)
        self.metadata_reader = MetadataReader()

        # ========== Theme setup ==========
        self._apply_theme(self.theme_manager.current)

        # ========== Menu bar ==========
        self._create_menu_bar()

        # ========== Toolbar ==========
        self.toolbar = Toolbar(root)
        self.toolbar.pack(fill="x", padx=10, pady=(5, 0))
        self._setup_toolbar()

        # ========== Main container ==========
        main_frame = ttk.Frame(root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Notebook (tabs)
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill="both", expand=True)

        # Tabs
        self.main_tab = MainTab(self.notebook, self)
        self.notebook.add(self.main_tab, text="  📋 Main  ")

        self.effects_tab = EffectsTab(self.notebook, self)
        self.notebook.add(self.effects_tab, text="  🎨 Effects  ")

        self.crop_tab = CropTab(self.notebook, self)
        self.notebook.add(self.crop_tab, text="  ✂️ Crop  ")

        self.batch_tab = BatchTab(self.notebook, self)
        self.notebook.add(self.batch_tab, text="  ⚡ Batch  ")

        self.log_tab = LogTab(self.notebook, self)
        self.notebook.add(self.log_tab, text="  📜 Log  ")

        # ========== Status bar ==========
        self.status_bar = StatusBar(root)
        self.status_bar.pack(fill="x", side="bottom", padx=10, pady=(0, 5))

        # ========== Logger UI callback ==========
        self.log.set_ui_callback(self.log_tab.add_entry)

        # ========== Keyboard shortcuts ==========
        self._setup_shortcuts()

        # ========== Start log ==========
        self.log.info(f"{APP_NAME} v{APP_VERSION} started.")
        self.status_bar.set_status("Ready", "success")

    # ========== Theme ==========

    def _apply_theme(self, theme):
        """Apply theme to all widgets."""
        style = ttk.Style()
        style.theme_use("clam")

        # Button
        style.configure(
            "TButton",
            background=theme["primary"],
            foreground=theme["button_fg"],
            font=(FONT_FAMILY, FONT_SIZE_NORMAL, "bold"),
            padding=6, relief="flat"
        )
        style.map("TButton", background=[
            ("active", theme["primary_hover"]),
            ("disabled", theme["border"])
        ])

        # Label
        style.configure(
            "TLabel",
            font=(FONT_FAMILY, FONT_SIZE_NORMAL),
            foreground=theme["fg"],
            background=theme["bg"],
            padding=2
        )

        # Frame
        style.configure("TFrame", background=theme["bg"])

        # LabelFrame
        style.configure(
            "TLabelframe", background=theme["bg"],
            padding=8, font=(FONT_FAMILY, FONT_SIZE_NORMAL, "bold")
        )
        style.configure(
            "TLabelframe.Label",
            foreground=theme["primary"],
            background=theme["bg"],
            font=(FONT_FAMILY, FONT_SIZE_TITLE, "bold")
        )

        # Notebook
        style.configure("TNotebook", background=theme["bg"])
        style.configure(
            "TNotebook.Tab",
            font=(FONT_FAMILY, FONT_SIZE_NORMAL, "bold"),
            padding=[12, 5],
            background=theme["tab_bg"],
            foreground=theme["tab_fg"]
        )
        style.map("TNotebook.Tab", background=[
            ("selected", theme["tab_selected_bg"])
        ], foreground=[
            ("selected", theme["tab_selected_fg"])
        ])

        # Checkbutton
        style.configure(
            "TCheckbutton",
            background=theme["bg"],
            foreground=theme["fg"],
            font=(FONT_FAMILY, FONT_SIZE_NORMAL)
        )

        # Entry
        style.configure(
            "TEntry",
            fieldbackground=theme["input_bg"],
            foreground=theme["input_fg"]
        )

        # Progressbar
        style.configure(
            "Horizontal.TProgressbar",
            troughcolor=theme["progress_bg"],
            background=theme["progress_fg"]
        )

        # OptionMenu (Menubutton)
        style.configure(
            "TMenubutton",
            background=theme["surface"],
            foreground=theme["fg"],
            padding=4, relief="flat"
        )

        # Scale
        style.configure(
            "Horizontal.TScale",
            background=theme["bg"],
            troughcolor=theme["border"]
        )

        # Separator
        style.configure("TSeparator", background=theme["border"])

        # Scrollbar
        style.configure(
            "Vertical.TScrollbar",
            background=theme["scrollbar"],
            troughcolor=theme["bg"]
        )

        # Root window
        self.root.configure(background=theme["bg"])

    def toggle_theme(self):
        """Toggle between Dark and Light theme."""
        theme = self.theme_manager.toggle()
        self._apply_theme(theme)
        self.log.info(f"Theme switched to: {theme['name']}")

    # ========== Menu bar ==========

    def _create_menu_bar(self):
        """Create the menu bar."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="📂 File", menu=file_menu)
        file_menu.add_command(label="Open Images  (Ctrl+O)", command=self._menu_open)
        file_menu.add_command(label="Process  (Ctrl+Enter)", command=self.start_processing)
        file_menu.add_separator()
        file_menu.add_command(label="Exit  (Ctrl+Q)", command=self.root.quit)

        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="✏️ Edit", menu=edit_menu)
        edit_menu.add_command(label="Undo  (Ctrl+Z)", command=self._undo)
        edit_menu.add_command(label="Redo  (Ctrl+Y)", command=self._redo)
        edit_menu.add_separator()
        edit_menu.add_command(label="Clear Selection  (Ctrl+Del)", command=self._clear_all)

        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="👁️ View", menu=view_menu)
        view_menu.add_command(label="Toggle Theme  (Ctrl+T)", command=self.toggle_theme)

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="❓ Help", menu=help_menu)
        help_menu.add_command(label="About", command=lambda: AboutDialog.show(self.root))

    # ========== Toolbar ==========

    def _setup_toolbar(self):
        """Set up toolbar buttons."""
        self.toolbar.add_button("open", "📂 Open", self._menu_open, "Open images (Ctrl+O)")
        self.toolbar.add_button("process", "🚀 Process", self.start_processing, "Process images (Ctrl+Enter)")
        self.toolbar.add_separator()
        self.toolbar.add_button("undo", "↩️ Undo", self._undo, "Undo (Ctrl+Z)")
        self.toolbar.add_button("redo", "↪️ Redo", self._redo, "Redo (Ctrl+Y)")
        self.toolbar.add_separator()
        self.toolbar.add_button("theme", "🎨 Theme", self.toggle_theme, "Toggle theme (Ctrl+T)")

    # ========== Shortcuts ==========

    def _setup_shortcuts(self):
        """Set up keyboard shortcuts."""
        self.root.bind(SHORTCUTS["open"], lambda e: self._menu_open())
        self.root.bind(SHORTCUTS["save"], lambda e: self.start_processing())
        self.root.bind(SHORTCUTS["undo"], lambda e: self._undo())
        self.root.bind(SHORTCUTS["redo"], lambda e: self._redo())
        self.root.bind(SHORTCUTS["quit"], lambda e: self.root.quit())
        self.root.bind(SHORTCUTS["process"], lambda e: self.start_processing())
        self.root.bind(SHORTCUTS["theme_toggle"], lambda e: self.toggle_theme())

    # ========== Menu actions ==========

    def _menu_open(self):
        """Open file selection dialog."""
        self.notebook.select(self.main_tab)
        self.main_tab._select_images()

    def _clear_all(self):
        """Clear all selections."""
        self.main_tab._clear_selection()

    def _undo(self):
        """Undo last action."""
        state = self.history.undo()
        if state:
            self.log.info(f"Undone. (Steps: {self.history.undo_count})")
        else:
            self.log.warning("Nothing to undo.")

    def _redo(self):
        """Redo last undone action."""
        state = self.history.redo()
        if state:
            self.log.info(f"Redone. (Steps: {self.history.redo_count})")
        else:
            self.log.warning("Nothing to redo.")

    # ========== Settings ==========

    def get_all_settings(self):
        """Collect all settings from all tabs."""
        settings = {}
        settings.update(self.main_tab.get_settings())
        settings.update(self.effects_tab.get_settings())
        settings.update(self.batch_tab.get_rename_settings())
        return settings

    def apply_settings(self, settings):
        """Apply preset settings to all tabs."""
        self.main_tab.set_settings(settings)
        self.effects_tab.set_settings(settings)

    # ========== Processing ==========

    def start_processing(self):
        """Start batch image processing."""
        if not self.image_paths:
            messagebox.showerror("Error", "Please select at least one image!")
            return

        if self.processing:
            messagebox.showwarning("Warning", "Processing is already in progress.")
            return

        save_dir = filedialog.askdirectory(title="Select output folder")
        if not save_dir:
            return

        self.output_dir = save_dir
        self.processing = True
        self._start_time = time.time()

        # Lock UI
        self.main_tab.process_btn.config(state="disabled")
        self.main_tab.cancel_btn.config(state="normal")
        self.main_tab.progress["maximum"] = len(self.image_paths)
        self.main_tab.progress["value"] = 0
        self.main_tab.status_label.config(text="Status: Processing...")
        self.status_bar.set_status("Processing...", "info")

        # Read settings in main thread (thread-safe!)
        settings = self.get_all_settings()

        self.log.info(f"Processing started. {len(self.image_paths)} image(s).")

        # Worker thread
        thread = threading.Thread(
            target=self._process_worker,
            args=(settings, save_dir),
            daemon=True
        )
        thread.start()

        # Queue monitoring
        self.root.after(100, self._check_queue)

    def _process_worker(self, settings, save_dir):
        """Worker thread — process images in background."""
        try:
            def progress_callback(idx, total, filename, status):
                self._queue.put(("progress", (idx, total, filename, status)))

            results = self.batch_processor.process_batch(
                self.image_paths, settings, save_dir,
                progress_callback=progress_callback
            )

            self._queue.put(("complete", results))

        except Exception as e:
            self._queue.put(("error", str(e)))

    def _check_queue(self):
        """Read messages from the processing queue."""
        try:
            while True:
                msg_type, data = self._queue.get_nowait()

                if msg_type == "progress":
                    idx, total, filename, status = data
                    self.main_tab.progress["value"] = idx + 1
                    self.main_tab.status_label.config(text=f"Status: {filename}")
                    self.status_bar.set_status(f"Processing {idx+1}/{total}...")
                    self.log.info(status)

                    # Time calculation
                    elapsed = time.time() - self._start_time
                    if idx + 1 > 0:
                        remaining = (elapsed / (idx + 1)) * (total - idx - 1)
                        self.main_tab.time_label.config(
                            text=f"⏱️ Elapsed: {int(elapsed)}s | Remaining: {int(remaining)}s"
                        )

                elif msg_type == "complete":
                    self._process_complete(data)

                elif msg_type == "error":
                    messagebox.showerror("Error", f"Processing error: {data}")
                    self.cancel_processing()

                self._queue.task_done()

        except queue.Empty:
            if self.processing:
                self.root.after(100, self._check_queue)

    def _process_complete(self, results):
        """Handle processing completion."""
        elapsed = time.time() - self._start_time

        success = results["success"]
        failed = results["failed"]

        self.log.success(
            f"Done! {success} successful, {failed} failed. "
            f"Time: {elapsed:.1f}s"
        )

        if results["errors"]:
            for err in results["errors"]:
                self.log.error(err)

        # Update UI
        self.main_tab.status_label.config(
            text=f"Status: Complete ✅ ({success}/{success + failed})"
        )
        self.main_tab.time_label.config(text=f"⏱️ Total: {int(elapsed)}s")
        self.main_tab.process_btn.config(state="normal")
        self.main_tab.cancel_btn.config(state="disabled")
        self.main_tab.open_folder_btn.config(state="normal")
        self.status_bar.set_status(f"{success} image(s) saved ({elapsed:.1f}s)", "success")

        self.processing = False

        if success > 0:
            messagebox.showinfo(
                "Success",
                f"✅ {success} image(s) processed successfully.\n"
                f"{'❌ ' + str(failed) + ' error(s).' if failed else ''}\n"
                f"⏱️ Time: {elapsed:.1f} seconds"
            )

    def cancel_processing(self):
        """Cancel processing."""
        self.processing = False
        self.batch_processor.cancel()
        self.log.warning("Processing cancelled.")
        self.main_tab.status_label.config(text="Status: Cancelled ⏹️")
        self.main_tab.process_btn.config(state="normal")
        self.main_tab.cancel_btn.config(state="disabled")
        self.status_bar.set_status("Cancelled", "warning")

    def open_output_folder(self):
        """Open the output folder in file explorer."""
        if self.output_dir:
            if not open_folder(self.output_dir):
                messagebox.showerror("Error", "Could not open folder.")
        else:
            messagebox.showwarning("Warning", "No output folder available.")

    # ========== Preview & Metadata ==========

    def show_preview(self, img, title="Preview"):
        """Show image preview window."""
        preview_win = tk.Toplevel(self.root)
        preview_win.title(f"👁️ {title}")
        preview_win.geometry("600x550")
        preview_win.transient(self.root)

        frame = ttk.Frame(preview_win, padding=10)
        frame.pack(fill="both", expand=True)

        # Fit image
        display_img = img.copy()
        display_img.thumbnail((550, 420), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(display_img)

        img_label = ttk.Label(frame, image=photo)
        img_label.image = photo
        img_label.pack(pady=10)

        # Info
        info_text = (
            f"Size: {img.width}×{img.height} px\n"
            f"Format: {img.format or 'N/A'}\n"
            f"Mode: {img.mode}"
        )
        ttk.Label(frame, text=info_text, justify="center").pack(pady=5)

        ttk.Button(frame, text="Close", command=preview_win.destroy).pack(pady=5)

    def show_metadata(self, image_path):
        """Show EXIF metadata window."""
        meta_win = tk.Toplevel(self.root)
        meta_win.title(f"ℹ️ Metadata: {os.path.basename(image_path)}")
        meta_win.geometry("500x450")
        meta_win.transient(self.root)

        frame = ttk.Frame(meta_win, padding=10)
        frame.pack(fill="both", expand=True)

        # Basic info
        basic_info = self.metadata_reader.get_basic_info(image_path)
        ttk.Label(frame, text="📸 Image Information", font=(FONT_FAMILY, 12, "bold")).pack(anchor="w", pady=(0, 5))

        for key, value in basic_info.items():
            ttk.Label(frame, text=f"  {key}: {value}").pack(anchor="w")

        ttk.Separator(frame, orient="horizontal").pack(fill="x", pady=10)

        # EXIF
        ttk.Label(frame, text="📋 EXIF Data", font=(FONT_FAMILY, 12, "bold")).pack(anchor="w", pady=(0, 5))

        exif_data = self.metadata_reader.read_exif(image_path)
        if exif_data:
            camera_info = self.metadata_reader.get_camera_info(exif_data)
            if camera_info:
                for key, value in camera_info.items():
                    ttk.Label(frame, text=f"  {key}: {value}").pack(anchor="w")
            else:
                ttk.Label(frame, text="  No camera information found.").pack(anchor="w")
        else:
            ttk.Label(frame, text="  No EXIF data found.").pack(anchor="w")

        ttk.Button(frame, text="Close", command=meta_win.destroy).pack(pady=10)
