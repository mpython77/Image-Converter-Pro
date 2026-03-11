"""
Test — ImageCropper klassi.
"""

import pytest
import os
import sys
from PIL import Image

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from core.cropper import ImageCropper


@pytest.fixture
def cropper():
    return ImageCropper()


@pytest.fixture
def sample_image():
    return Image.new("RGB", (400, 300), color=(100, 150, 200))


class TestCrop:
    def test_basic_crop(self):
        img = Image.new("RGB", (400, 300))
        result = ImageCropper.crop(img, 50, 50, 200, 200)
        assert result.size == (150, 150)

    def test_crop_reversed_coords(self):
        img = Image.new("RGB", (400, 300))
        result = ImageCropper.crop(img, 200, 200, 50, 50)
        assert result.size == (150, 150)

    def test_crop_full_image(self):
        img = Image.new("RGB", (400, 300))
        result = ImageCropper.crop(img, 0, 0, 400, 300)
        assert result.size == (400, 300)

    def test_crop_invalid_region(self):
        img = Image.new("RGB", (400, 300))
        with pytest.raises(ValueError):
            ImageCropper.crop(img, 100, 100, 100, 100)

    def test_crop_out_of_bounds(self):
        img = Image.new("RGB", (400, 300))
        result = ImageCropper.crop(img, 350, 250, 500, 400)
        assert result.width <= 400
        assert result.height <= 300


class TestCropCenter:
    def test_center_crop(self):
        img = Image.new("RGB", (400, 300))
        result = ImageCropper.crop_center(img, 200, 200)
        assert result.size == (200, 200)

    def test_center_crop_too_large(self):
        img = Image.new("RGB", (400, 300))
        result = ImageCropper.crop_center(img, 500, 500)
        assert result.width <= 400
        assert result.height <= 300


class TestCropRatio:
    def test_16_9_from_square(self):
        img = Image.new("RGB", (400, 400))
        result = ImageCropper.crop_ratio(img, 16, 9)
        ratio = result.width / result.height
        assert abs(ratio - 16/9) < 0.01

    def test_1_1(self):
        img = Image.new("RGB", (400, 300))
        result = ImageCropper.crop_ratio(img, 1, 1)
        assert result.width == result.height

    def test_4_3(self):
        img = Image.new("RGB", (400, 300))
        result = ImageCropper.crop_ratio(img, 4, 3)
        ratio = result.width / result.height
        assert abs(ratio - 4/3) < 0.01
