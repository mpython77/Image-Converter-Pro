"""
Image Converter Pro — Undo/Redo history module.
"""

from PIL import Image
from config.constants import MAX_HISTORY_STEPS


class HistoryManager:
    """Undo/Redo system using image state stacks."""

    def __init__(self, max_steps=None):
        """Create HistoryManager.

        Args:
            max_steps: Maximum number of history steps to keep
        """
        self.max_steps = max_steps or MAX_HISTORY_STEPS
        self._undo_stack = []
        self._redo_stack = []

    def push(self, img):
        """Push a new state onto the history.

        Args:
            img: PIL Image representing the current state
        """
        self._undo_stack.append(img.copy())
        self._redo_stack.clear()

        while len(self._undo_stack) > self.max_steps:
            self._undo_stack.pop(0)

    def undo(self):
        """Undo the last action.

        Returns:
            PIL Image or None: Previous state
        """
        if not self.can_undo:
            return None

        current = self._undo_stack.pop()
        self._redo_stack.append(current)

        if self._undo_stack:
            return self._undo_stack[-1].copy()
        return None

    def redo(self):
        """Redo the last undone action.

        Returns:
            PIL Image or None: Restored state
        """
        if not self.can_redo:
            return None

        state = self._redo_stack.pop()
        self._undo_stack.append(state)
        return state.copy()

    @property
    def can_undo(self):
        """Check if undo is possible."""
        return len(self._undo_stack) > 1

    @property
    def can_redo(self):
        """Check if redo is possible."""
        return len(self._redo_stack) > 0

    @property
    def undo_count(self):
        """Number of available undo steps."""
        return max(0, len(self._undo_stack) - 1)

    @property
    def redo_count(self):
        """Number of available redo steps."""
        return len(self._redo_stack)

    def clear(self):
        """Clear all history."""
        self._undo_stack.clear()
        self._redo_stack.clear()

    def get_current(self):
        """Get the current state.

        Returns:
            PIL Image or None
        """
        if self._undo_stack:
            return self._undo_stack[-1].copy()
        return None
