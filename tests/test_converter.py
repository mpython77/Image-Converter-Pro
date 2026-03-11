"""
Test — ImageConverter klassi.
"""

import pytest
import os
import tempfile
from PIL import Image

# Loyiha root ni path ga qo'shish
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from core.converter import ImageConverter
from utils.validators import ValidationError


@pytest.fixture
def converter():
    return ImageConverter()


@pytest.fixture
def sample_image():
    """Test rasm yaratish (RGB, 200x150)."""
    return Image.new("RGB", (200, 150), color=(100, 150, 200))


@pytest.fixture
def rgba_image():
    """RGBA test rasm yaratish."""
    return Image.new("RGBA", (200, 150), color=(100, 150, 200, 128))


class TestResize:
    def test_resize_no_ratio(self, sample_image):
        result = ImageConverter.resize(sample_image, 100, 80, maintain_ratio=False)
        assert result.size == (100, 80)

    def test_resize_with_ratio(self, sample_image):
        result = ImageConverter.resize(sample_image, 100, 100, maintain_ratio=True)
        assert result.width <= 100
        assert result.height <= 100

    def test_resize_invalid_dimensions(self, sample_image):
        with pytest.raises(ValidationError):
            ImageConverter.resize(sample_image, "abc", 100)

    def test_resize_negative_dimensions(self, sample_image):
        with pytest.raises(ValidationError):
            ImageConverter.resize(sample_image, -100, 100)

    def test_resize_preserves_mode(self, sample_image):
        result = ImageConverter.resize(sample_image, 100, 100)
        assert result.mode == "RGB"


class TestRotate:
    def test_rotate_90(self, sample_image):
        result = ImageConverter.rotate(sample_image, 90)
        assert result.width == 150  # Width va height almashadi
        assert result.height == 200

    def test_rotate_180(self, sample_image):
        result = ImageConverter.rotate(sample_image, 180)
        assert result.width == 200
        assert result.height == 150

    def test_rotate_zero(self, sample_image):
        result = ImageConverter.rotate(sample_image, 0)
        assert result.size == sample_image.size

    def test_rotate_invalid(self, sample_image):
        with pytest.raises(ValidationError):
            ImageConverter.rotate(sample_image, "abc")


class TestConvertFormat:
    def test_rgba_to_jpeg(self, rgba_image):
        result = ImageConverter.convert_format(rgba_image, "JPEG")
        assert result.mode == "RGB"

    def test_rgb_stays_rgb(self, sample_image):
        result = ImageConverter.convert_format(sample_image, "JPEG")
        assert result.mode == "RGB"

    def test_invalid_format(self, sample_image):
        with pytest.raises(ValidationError):
            ImageConverter.convert_format(sample_image, "INVALID")


class TestSave:
    def test_save_jpeg(self, sample_image):
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as f:
            path = f.name

        try:
            ImageConverter.save(sample_image, path, "JPEG", quality=85)
            assert os.path.exists(path)
            assert os.path.getsize(path) > 0
        finally:
            os.unlink(path)

    def test_save_png(self, sample_image):
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            path = f.name

        try:
            ImageConverter.save(sample_image, path, "PNG")
            assert os.path.exists(path)
        finally:
            os.unlink(path)

    def test_save_invalid_quality(self, sample_image):
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as f:
            path = f.name

        try:
            with pytest.raises(ValidationError):
                ImageConverter.save(sample_image, path, "JPEG", quality=150)
        finally:
            os.unlink(path)


class TestLoad:
    def test_load_image(self, sample_image):
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            path = f.name
            sample_image.save(path)

        try:
            loaded = ImageConverter.load(path)
            assert loaded.size == (200, 150)
        finally:
            os.unlink(path)


class TestProcess:
    def test_full_process(self, converter, sample_image):
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            path = f.name
            sample_image.save(path)

        try:
            settings = {
                "width": 100,
                "height": 100,
                "maintain_ratio": True,
                "angle": 0,
                "format": "JPEG"
            }
            result = converter.process(path, settings)
            assert result.width <= 100
            assert result.height <= 100
        finally:
            os.unlink(path)
