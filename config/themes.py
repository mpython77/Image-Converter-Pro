"""
Image Converter Pro — Theme management system.
Dark and Light themes with dynamic switching.
"""


# Light theme
LIGHT_THEME = {
    "name": "Light",
    "bg": "#f8fafc",
    "fg": "#1e293b",
    "surface": "#ffffff",
    "primary": "#3b82f6",
    "primary_hover": "#2563eb",
    "secondary": "#64748b",
    "border": "#e2e8f0",
    "success": "#22c55e",
    "warning": "#f59e0b",
    "error": "#ef4444",
    "button_fg": "#ffffff",
    "input_bg": "#ffffff",
    "input_fg": "#1e293b",
    "tab_bg": "#e2e8f0",
    "tab_fg": "#475569",
    "tab_selected_bg": "#3b82f6",
    "tab_selected_fg": "#ffffff",
    "progress_bg": "#e2e8f0",
    "progress_fg": "#3b82f6",
    "scrollbar": "#cbd5e1",
}

# Dark theme
DARK_THEME = {
    "name": "Dark",
    "bg": "#0f172a",
    "fg": "#e2e8f0",
    "surface": "#1e293b",
    "primary": "#3b82f6",
    "primary_hover": "#60a5fa",
    "secondary": "#94a3b8",
    "border": "#334155",
    "success": "#34d399",
    "warning": "#fbbf24",
    "error": "#f87171",
    "button_fg": "#ffffff",
    "input_bg": "#1e293b",
    "input_fg": "#e2e8f0",
    "tab_bg": "#1e293b",
    "tab_fg": "#94a3b8",
    "tab_selected_bg": "#3b82f6",
    "tab_selected_fg": "#ffffff",
    "progress_bg": "#334155",
    "progress_fg": "#3b82f6",
    "scrollbar": "#475569",
}


class ThemeManager:
    """Manages application themes with dynamic switching.

    Attributes:
        current: Currently active theme dictionary
        _listeners: Callback functions notified on theme change
    """

    def __init__(self, default="dark"):
        """Initialize ThemeManager.

        Args:
            default: Default theme name ('dark' or 'light')
        """
        self.current = DARK_THEME if default == "dark" else LIGHT_THEME
        self._listeners = []

    def toggle(self):
        """Toggle between dark and light themes.

        Returns:
            dict: The newly activated theme
        """
        if self.current["name"] == "Dark":
            self.current = LIGHT_THEME
        else:
            self.current = DARK_THEME

        self._notify_listeners()
        return self.current

    def set_theme(self, name):
        """Set a specific theme by name.

        Args:
            name: Theme name ('dark' or 'light')
        """
        if name.lower() == "dark":
            self.current = DARK_THEME
        else:
            self.current = LIGHT_THEME
        self._notify_listeners()

    def add_listener(self, callback):
        """Register a callback for theme changes.

        Args:
            callback: Function to call when theme changes (receives theme dict)
        """
        self._listeners.append(callback)

    def _notify_listeners(self):
        """Notify all registered listeners of a theme change."""
        for listener in self._listeners:
            try:
                listener(self.current)
            except Exception:
                pass

    @property
    def is_dark(self):
        """Check if current theme is dark."""
        return self.current["name"] == "Dark"
