"""
Test — PresetManager klassi.
"""

import pytest
import os
import sys
import tempfile
import shutil

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from core.preset_manager import PresetManager


@pytest.fixture
def preset_dir():
    """Vaqtinchalik preset papka yaratish."""
    tmpdir = tempfile.mkdtemp()
    yield tmpdir
    shutil.rmtree(tmpdir)


@pytest.fixture
def manager(preset_dir):
    return PresetManager(presets_dir=preset_dir)


class TestSave:
    def test_save_preset(self, manager):
        settings = {"format": "PNG", "width": 1024, "height": 768}
        path = manager.save("test_preset", settings)
        assert os.path.exists(path)

    def test_save_empty_name(self, manager):
        with pytest.raises(ValueError):
            manager.save("", {})

    def test_save_whitespace_name(self, manager):
        with pytest.raises(ValueError):
            manager.save("   ", {})


class TestLoad:
    def test_load_preset(self, manager):
        manager.save("test", {"format": "PNG", "width": 1024})
        loaded = manager.load("test")
        assert loaded["format"] == "PNG"
        assert loaded["width"] == 1024

    def test_load_nonexistent(self, manager):
        with pytest.raises(FileNotFoundError):
            manager.load("nonexistent")

    def test_load_with_defaults(self, manager):
        manager.save("minimal", {"format": "BMP"})
        loaded = manager.load("minimal")
        # Default qiymatlar bilan to'ldirilishi kerak
        assert "quality" in loaded
        assert "brightness" in loaded


class TestList:
    def test_empty_list(self, manager):
        assert manager.list_presets() == []

    def test_list_presets(self, manager):
        manager.save("alpha", {})
        manager.save("beta", {})
        presets = manager.list_presets()
        assert len(presets) == 2
        assert "alpha" in presets
        assert "beta" in presets


class TestDelete:
    def test_delete_existing(self, manager):
        manager.save("to_delete", {})
        assert manager.delete("to_delete") is True
        assert "to_delete" not in manager.list_presets()

    def test_delete_nonexistent(self, manager):
        assert manager.delete("nonexistent") is False


class TestDefault:
    def test_get_default(self, manager):
        default = manager.get_default()
        assert default["format"] == "JPEG"
        assert default["quality"] == 85
        assert default["brightness"] == 1.0
