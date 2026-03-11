"""conftest.py — Shared pytest configuration and fixtures."""

import sys
import os
import pytest
from PIL import Image

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


@pytest.fixture
def sample_rgb():
    """200x150 RGB test image."""
    return Image.new("RGB", (200, 150), color=(100, 150, 200))


@pytest.fixture
def sample_rgba():
    """200x150 RGBA test image."""
    return Image.new("RGBA", (200, 150), color=(100, 150, 200, 128))


@pytest.fixture
def sample_large():
    """1920x1080 RGB test image (large)."""
    return Image.new("RGB", (1920, 1080), color=(50, 100, 150))


@pytest.fixture
def sample_square():
    """400x400 RGB square image."""
    return Image.new("RGB", (400, 400), color=(200, 200, 200))


@pytest.fixture
def tmp_image_path(sample_rgb, tmp_path):
    """Temporary PNG file path."""
    path = str(tmp_path / "test.png")
    sample_rgb.save(path)
    return path


@pytest.fixture
def tmp_dir(tmp_path):
    """Temporary directory."""
    return str(tmp_path)
