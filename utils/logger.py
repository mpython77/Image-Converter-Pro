"""
Image Converter Pro — Logging system.
Dual output: UI callback and Python logging.
"""

import logging
from datetime import datetime


class AppLogger:
    """Application logger with dual output (UI + file/console).

    Attributes:
        _entries: List of log entries
        _ui_callback: Callback for writing to UI
    """

    def __init__(self):
        self._entries = []
        self._ui_callback = None
        self._setup_file_logger()

    def _setup_file_logger(self):
        """Set up Python's logging module."""
        self._logger = logging.getLogger("ImageConverterPro")
        self._logger.setLevel(logging.DEBUG)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        formatter = logging.Formatter(
            "[%(asctime)s] %(levelname)s: %(message)s",
            datefmt="%H:%M:%S"
        )
        console_handler.setFormatter(formatter)

        if not self._logger.handlers:
            self._logger.addHandler(console_handler)

    def set_ui_callback(self, callback):
        """Set callback for writing log entries to the UI.

        Args:
            callback: Function that accepts a log string (str -> None)
        """
        self._ui_callback = callback

    def info(self, message):
        """Log an info-level message."""
        self._log("INFO", message)

    def warning(self, message):
        """Log a warning-level message."""
        self._log("WARNING", message)

    def error(self, message):
        """Log an error-level message."""
        self._log("ERROR", message)

    def success(self, message):
        """Log a success-level message."""
        self._log("SUCCESS", message)

    def debug(self, message):
        """Log a debug-level message."""
        self._logger.debug(message)

    def _log(self, level, message):
        """Internal log writing function."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        entry = f"[{timestamp}] [{level}] {message}"
        self._entries.append(entry)

        # Python logger
        if level == "ERROR":
            self._logger.error(message)
        elif level == "WARNING":
            self._logger.warning(message)
        else:
            self._logger.info(message)

        # UI callback
        if self._ui_callback:
            try:
                self._ui_callback(entry)
            except Exception:
                pass

    def get_all_entries(self):
        """Return all log entries.

        Returns:
            list: Copy of log entries
        """
        return self._entries.copy()

    def get_text(self):
        """Return all log entries as a single string.

        Returns:
            str: All logs joined by newlines
        """
        return "\n".join(self._entries)

    def clear(self):
        """Clear all log entries."""
        self._entries.clear()

    def save_to_file(self, filepath):
        """Save logs to a text file.

        Args:
            filepath: Output file path

        Raises:
            IOError: If writing fails
        """
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(self.get_text())
        self.info(f"Log saved to: {filepath}")
