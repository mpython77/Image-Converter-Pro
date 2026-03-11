"""
Test — History (Undo/Redo) klassi.
"""

import pytest
import os
import sys
from PIL import Image

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from core.history import HistoryManager


@pytest.fixture
def history():
    return HistoryManager(max_steps=5)


@pytest.fixture
def images():
    """3 ta turli rasm yaratish."""
    return [
        Image.new("RGB", (100, 100), color=(255, 0, 0)),
        Image.new("RGB", (100, 100), color=(0, 255, 0)),
        Image.new("RGB", (100, 100), color=(0, 0, 255)),
    ]


class TestUndo:
    def test_undo_empty(self, history):
        result = history.undo()
        assert result is None

    def test_undo_single(self, history, images):
        history.push(images[0])
        history.push(images[1])
        result = history.undo()
        assert result is not None

    def test_undo_multiple(self, history, images):
        for img in images:
            history.push(img)
        history.undo()
        result = history.undo()
        assert result is not None


class TestRedo:
    def test_redo_empty(self, history):
        result = history.redo()
        assert result is None

    def test_redo_after_undo(self, history, images):
        history.push(images[0])
        history.push(images[1])
        history.undo()
        result = history.redo()
        assert result is not None

    def test_redo_cleared_on_push(self, history, images):
        history.push(images[0])
        history.push(images[1])
        history.undo()
        history.push(images[2])  # Bu redo stackni tozalashi kerak
        result = history.redo()
        assert result is None


class TestMaxSteps:
    def test_max_steps(self):
        history = HistoryManager(max_steps=3)
        for i in range(10):
            history.push(Image.new("RGB", (10, 10), color=(i, i, i)))
        assert history.undo_count <= 3


class TestClear:
    def test_clear(self, history, images):
        for img in images:
            history.push(img)
        history.clear()
        assert history.undo_count == 0
        assert history.redo_count == 0


class TestCounts:
    def test_undo_count(self, history, images):
        assert history.undo_count == 0
        history.push(images[0])  # boshlang'ich holat
        assert history.undo_count == 0  # birinchi push = base state
        history.push(images[1])  # birinchi o'zgarish
        assert history.undo_count == 1  # endi 1 ta undo mumkin

    def test_redo_count(self, history, images):
        history.push(images[0])
        history.push(images[1])
        assert history.redo_count == 0
        history.undo()
        assert history.redo_count == 1
