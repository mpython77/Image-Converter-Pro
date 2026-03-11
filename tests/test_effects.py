"""
Test — EffectsEngine klassi.
"""

import pytest
import os
import sys
from PIL import Image

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from core.effects import EffectsEngine
from utils.validators import ValidationError


@pytest.fixture
def engine():
    return EffectsEngine()


@pytest.fixture
def sample_image():
    return Image.new("RGB", (100, 100), color=(128, 128, 128))


@pytest.fixture
def rgba_image():
    return Image.new("RGBA", (100, 100), color=(128, 128, 128, 255))


class TestBrightness:
    def test_default_no_change(self, sample_image):
        result = EffectsEngine.adjust_brightness(sample_image, 1.0)
        assert result.size == sample_image.size

    def test_brighter(self, sample_image):
        result = EffectsEngine.adjust_brightness(sample_image, 1.5)
        assert result is not None

    def test_darker(self, sample_image):
        result = EffectsEngine.adjust_brightness(sample_image, 0.5)
        assert result is not None

    def test_invalid_value(self, sample_image):
        with pytest.raises(ValidationError):
            EffectsEngine.adjust_brightness(sample_image, "abc")


class TestContrast:
    def test_default_no_change(self, sample_image):
        result = EffectsEngine.adjust_contrast(sample_image, 1.0)
        assert result.size == sample_image.size

    def test_high_contrast(self, sample_image):
        result = EffectsEngine.adjust_contrast(sample_image, 2.0)
        assert result is not None


class TestFilters:
    def test_blur(self, sample_image):
        result = EffectsEngine.apply_blur(sample_image)
        assert result.size == sample_image.size

    def test_sharpen(self, sample_image):
        result = EffectsEngine.apply_sharpen(sample_image)
        assert result is not None

    def test_edge_enhance(self, sample_image):
        result = EffectsEngine.apply_edge_enhance(sample_image)
        assert result is not None

    def test_emboss(self, sample_image):
        result = EffectsEngine.apply_emboss(sample_image)
        assert result is not None

    def test_contour(self, sample_image):
        result = EffectsEngine.apply_contour(sample_image)
        assert result is not None

    def test_grayscale(self, sample_image):
        result = EffectsEngine.apply_grayscale(sample_image)
        assert result.mode == "L"

    def test_sepia(self, sample_image):
        result = EffectsEngine.apply_sepia(sample_image)
        assert result.mode == "RGB"

    def test_sepia_rgba(self, rgba_image):
        result = EffectsEngine.apply_sepia(rgba_image)
        assert result.mode == "RGBA"

    def test_auto_enhance(self, sample_image):
        result = EffectsEngine.auto_enhance(sample_image)
        assert result is not None


class TestApplyAll:
    def test_apply_multiple(self, engine, sample_image):
        settings = {
            "brightness": 1.2,
            "contrast": 1.1,
            "blur": True,
            "sepia": False,
        }
        result = engine.apply_all(sample_image, settings)
        assert result.size == sample_image.size

    def test_apply_no_effects(self, engine, sample_image):
        settings = {}
        result = engine.apply_all(sample_image, settings)
        assert result.size == sample_image.size
