"""
Test — DPIManager va ProcessingStats.
"""

import pytest
import os
import sys
from PIL import Image

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from core.dpi_manager import DPIManager
from core.stats import ProcessingStats


class TestDPIManager:
    def test_get_dpi_default(self):
        img = Image.new("RGB", (100, 100))
        dpi = DPIManager.get_dpi(img)
        assert isinstance(dpi, tuple)
        assert len(dpi) == 2

    def test_set_dpi(self):
        img = Image.new("RGB", (100, 100))
        result = DPIManager.set_dpi(img, 300)
        assert result.info["dpi"] == (300, 300)

    def test_set_dpi_asymmetric(self):
        img = Image.new("RGB", (100, 100))
        result = DPIManager.set_dpi(img, 300, 150)
        assert result.info["dpi"] == (300, 150)

    def test_convert_to_print(self):
        img = Image.new("RGB", (100, 100))
        result = DPIManager.convert_to_print(img)
        assert result.info["dpi"] == (300, 300)

    def test_convert_to_web(self):
        img = Image.new("RGB", (100, 100))
        result = DPIManager.convert_to_web(img)
        assert result.info["dpi"] == (72, 72)

    def test_calculate_print_size(self):
        img = Image.new("RGB", (300, 300))
        img.info["dpi"] = (300, 300)
        w_cm, h_cm = DPIManager.calculate_print_size_cm(img)
        assert abs(w_cm - 2.5) < 0.1  # 300px / 300dpi = 1 inch = 2.54cm
        assert abs(h_cm - 2.5) < 0.1

    def test_doesnt_modify_original(self):
        img = Image.new("RGB", (100, 100))
        result = DPIManager.set_dpi(img, 300)
        assert result is not img


class TestProcessingStats:
    def test_start(self):
        stats = ProcessingStats()
        stats.start(10)
        assert stats.total == 10
        assert stats.success == 0
        assert stats.failed == 0

    def test_elapsed(self):
        stats = ProcessingStats()
        stats.start(5)
        import time
        time.sleep(0.1)
        assert stats.elapsed > 0

    def test_avg_time(self):
        stats = ProcessingStats()
        stats.start(2)
        stats.success = 2
        stats.finish()
        assert stats.avg_time >= 0

    def test_speed(self):
        stats = ProcessingStats()
        stats.start(10)
        import time
        time.sleep(0.05)
        stats.success = 10
        stats.finish()
        assert stats.speed > 0

    def test_compression_ratio(self):
        stats = ProcessingStats()
        stats.total_input_size = 1000
        stats.total_output_size = 500
        assert abs(stats.compression_ratio - 50.0) < 0.1

    def test_compression_ratio_zero_input(self):
        stats = ProcessingStats()
        assert stats.compression_ratio == 0

    def test_summary(self):
        stats = ProcessingStats()
        stats.start(5)
        stats.success = 4
        stats.failed = 1
        stats.finish()
        s = stats.summary()
        assert s["total"] == 5
        assert s["success"] == 4
        assert s["failed"] == 1

    def test_summary_text(self):
        stats = ProcessingStats()
        stats.start(3)
        stats.success = 3
        stats.finish()
        text = stats.summary_text()
        assert "3/3" in text
        assert "⏱️" in text

    def test_format_size(self):
        assert "B" in ProcessingStats._format_size(500)
        assert "KB" in ProcessingStats._format_size(2048)
        assert "MB" in ProcessingStats._format_size(2 * 1024 * 1024)
