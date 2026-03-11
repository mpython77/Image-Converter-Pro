"""
Image Converter Pro — Processing statistics.
Tracks batch results: timing, file sizes, compression ratio.
"""

import os
import time
from dataclasses import dataclass, field
from typing import List


@dataclass
class ProcessingStats:
    """Tracks and reports batch processing statistics.

    Attributes:
        total: Total number of images
        success: Successfully processed count
        failed: Failed count
        start_time: Start timestamp
        end_time: End timestamp
        total_input_size: Total input file size (bytes)
        total_output_size: Total output file size (bytes)
        errors: Error messages list
    """
    total: int = 0
    success: int = 0
    failed: int = 0
    start_time: float = 0
    end_time: float = 0
    total_input_size: int = 0
    total_output_size: int = 0
    errors: List[str] = field(default_factory=list)

    def start(self, total):
        """Start tracking statistics."""
        self.total = total
        self.start_time = time.time()
        self.success = 0
        self.failed = 0
        self.errors = []
        self.total_input_size = 0
        self.total_output_size = 0

    def finish(self):
        """Finish tracking."""
        self.end_time = time.time()

    @property
    def elapsed(self):
        """Elapsed time in seconds."""
        end = self.end_time if self.end_time else time.time()
        return end - self.start_time

    @property
    def avg_time(self):
        """Average time per image."""
        processed = self.success + self.failed
        if processed == 0:
            return 0
        return self.elapsed / processed

    @property
    def speed(self):
        """Processing speed (images/second)."""
        if self.elapsed == 0:
            return 0
        return (self.success + self.failed) / self.elapsed

    @property
    def compression_ratio(self):
        """Compression ratio as percentage."""
        if self.total_input_size == 0:
            return 0
        return (1 - self.total_output_size / self.total_input_size) * 100

    def add_input_size(self, path):
        """Add input file size to total."""
        try:
            self.total_input_size += os.path.getsize(path)
        except OSError:
            pass

    def add_output_size(self, path):
        """Add output file size to total."""
        try:
            self.total_output_size += os.path.getsize(path)
        except OSError:
            pass

    def summary(self):
        """Generate detailed results summary.

        Returns:
            dict: Detailed report
        """
        return {
            "total": self.total,
            "success": self.success,
            "failed": self.failed,
            "elapsed": f"{self.elapsed:.1f}s",
            "avg_time": f"{self.avg_time:.2f}s",
            "speed": f"{self.speed:.1f} img/s",
            "input_size": self._format_size(self.total_input_size),
            "output_size": self._format_size(self.total_output_size),
            "compression": f"{self.compression_ratio:.1f}%",
            "errors": self.errors,
        }

    def summary_text(self):
        """Generate human-readable summary text."""
        s = self.summary()
        lines = [
            f"📊 Results: {s['success']}/{s['total']} successful",
            f"⏱️ Time: {s['elapsed']} (avg: {s['avg_time']}/image)",
            f"⚡ Speed: {s['speed']}",
            f"💾 Input: {s['input_size']} → Output: {s['output_size']}",
            f"📉 Compression: {s['compression']}",
        ]
        if self.failed:
            lines.append(f"❌ Errors: {self.failed}")
        return "\n".join(lines)

    @staticmethod
    def _format_size(size_bytes):
        """Format file size in human-readable form."""
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        else:
            return f"{size_bytes / (1024 * 1024):.2f} MB"
