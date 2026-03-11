"""
Test — WatermarkEngine klassi.
"""

import pytest
import os
import sys
from PIL import Image

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from core.watermark import WatermarkEngine


@pytest.fixture
def engine():
    return WatermarkEngine()


@pytest.fixture
def sample_image():
    return Image.new("RGB", (400, 300), color=(255, 255, 255))


@pytest.fixture
def rgba_image():
    return Image.new("RGBA", (400, 300), color=(255, 255, 255, 255))


class TestWatermark:
    def test_add_watermark_bottom_right(self, engine, sample_image):
        result = engine.add_text_watermark(sample_image, "Test", position="bottom-right")
        assert result.size == sample_image.size
        assert result.mode == "RGB"

    def test_add_watermark_center(self, engine, sample_image):
        result = engine.add_text_watermark(sample_image, "Center", position="center")
        assert result is not None

    def test_add_watermark_all_positions(self, engine, sample_image):
        positions = ["top-left", "top-right", "bottom-left", "bottom-right", "center"]
        for pos in positions:
            result = engine.add_text_watermark(sample_image, "Test", position=pos)
            assert result is not None, f"Failed for position: {pos}"

    def test_rgba_watermark(self, engine, rgba_image):
        result = engine.add_text_watermark(rgba_image, "RGBA Test")
        assert result.mode == "RGBA"

    def test_empty_text(self, engine, sample_image):
        result = engine.add_text_watermark(sample_image, "")
        assert result.size == sample_image.size

    def test_opacity(self, engine, sample_image):
        result = engine.add_text_watermark(sample_image, "Test", opacity=0.3)
        assert result is not None

    def test_full_opacity(self, engine, sample_image):
        result = engine.add_text_watermark(sample_image, "Test", opacity=1.0)
        assert result is not None
