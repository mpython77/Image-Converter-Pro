"""
Image Converter Pro — Log Tab.
Log viewer with color-coded entries, save, and copy functionality.
"""

import tkinter as tk
from tkinter import ttk, filedialog


class LogTab(ttk.Frame):
    """Log tab — terminal-style log viewer."""

    def __init__(self, parent, app, **kwargs):
        super().__init__(parent, **kwargs)
        self.app = app

        self._create_controls()
        self._create_log_view()

    def _create_controls(self):
        """Create control buttons."""
        ctrl_frame = ttk.Frame(self)
        ctrl_frame.pack(fill="x", padx=5, pady=5)

        ttk.Button(ctrl_frame, text="🗑️ Clear", command=self._clear_log).pack(side="left", padx=3)
        ttk.Button(ctrl_frame, text="💾 Save Log", command=self._save_log).pack(side="left", padx=3)
        ttk.Button(ctrl_frame, text="📋 Copy", command=self._copy_log).pack(side="left", padx=3)

    def _create_log_view(self):
        """Create log text area."""
        log_frame = ttk.LabelFrame(self, text="📋 Activity Log")
        log_frame.pack(fill="both", expand=True, padx=5, pady=5)

        self.log_text = tk.Text(
            log_frame, wrap="word", state="disabled",
            bg="#0f172a", fg="#e2e8f0", font=("Consolas", 9),
            bd=0, highlightthickness=0, insertbackground="#e2e8f0"
        )
        self.log_text.pack(side="left", fill="both", expand=True, padx=3, pady=3)

        scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.log_text.config(yscrollcommand=scrollbar.set)

        # Color tags
        self.log_text.tag_configure("INFO", foreground="#60a5fa")
        self.log_text.tag_configure("SUCCESS", foreground="#34d399")
        self.log_text.tag_configure("WARNING", foreground="#fbbf24")
        self.log_text.tag_configure("ERROR", foreground="#f87171")

    def add_entry(self, entry):
        """Add a log entry with color coding.

        Args:
            entry: Log entry string
        """
        self.log_text.config(state="normal")

        # Determine tag
        tag = "INFO"
        if "[SUCCESS]" in entry:
            tag = "SUCCESS"
        elif "[WARNING]" in entry:
            tag = "WARNING"
        elif "[ERROR]" in entry:
            tag = "ERROR"

        self.log_text.insert("end", entry + "\n", tag)
        self.log_text.see("end")
        self.log_text.config(state="disabled")

    def _clear_log(self):
        """Clear log view."""
        self.log_text.config(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.config(state="disabled")
        self.app.log.clear()

    def _save_log(self):
        """Save log to file."""
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if path:
            try:
                self.app.log.save_to_file(path)
            except Exception as e:
                pass

    def _copy_log(self):
        """Copy log to clipboard."""
        self.clipboard_clear()
        self.clipboard_append(self.app.log.get_text())
