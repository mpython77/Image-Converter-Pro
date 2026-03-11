"""
Image Converter Pro — Preset manager module.
Save, load, list, and delete processing presets.
"""

import os
import json


class PresetManager:
    """Handles processing presets as JSON files.

    Features:
        - Save/Load/Delete presets
        - Default preset with sensible values
        - Auto-creation of presets directory
    """

    # Default preset values
    DEFAULTS = {
        "format": "JPEG",
        "width": 800,
        "height": 600,
        "maintain_ratio": True,
        "angle": 0,
        "quality": 85,
        "brightness": 1.0,
        "contrast": 1.0,
        "saturation": 1.0,
        "sharpness": 1.0,
        "blur": False, "sharpen": False, "edge_enhance": False,
        "emboss": False, "contour": False, "grayscale": False,
        "sepia": False, "vignette": False, "auto_enhance": False,
        "watermark": False,
        "watermark_text": "© Copyright",
        "watermark_position": "bottom-right",
        "watermark_opacity": 0.5,
        "rename": False,
        "rename_pattern": "image_{num}",
    }

    def __init__(self, presets_dir=None):
        """Create PresetManager.

        Args:
            presets_dir: Directory for preset files (default: ./presets)
        """
        self.presets_dir = presets_dir or os.path.join(os.getcwd(), "presets")
        os.makedirs(self.presets_dir, exist_ok=True)

    def save(self, name, settings):
        """Save a preset.

        Args:
            name: Preset name
            settings: Settings dictionary

        Returns:
            str: Saved file path

        Raises:
            ValueError: If name is empty
        """
        if not name or not name.strip():
            raise ValueError("Preset name cannot be empty.")

        # Merge with defaults
        full_settings = self.DEFAULTS.copy()
        full_settings.update(settings)

        filepath = os.path.join(self.presets_dir, f"{name.strip()}.json")
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(full_settings, f, indent=2, ensure_ascii=False)

        return filepath

    def load(self, name):
        """Load a preset.

        Args:
            name: Preset name

        Returns:
            dict: Loaded settings

        Raises:
            FileNotFoundError: If preset does not exist
        """
        filepath = os.path.join(self.presets_dir, f"{name}.json")
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Preset not found: {name}")

        with open(filepath, "r", encoding="utf-8") as f:
            settings = json.load(f)

        # Fill in missing defaults
        full_settings = self.DEFAULTS.copy()
        full_settings.update(settings)
        return full_settings

    def list_presets(self):
        """List all available presets.

        Returns:
            list: Preset names (without .json extension)
        """
        if not os.path.exists(self.presets_dir):
            return []

        presets = []
        for filename in sorted(os.listdir(self.presets_dir)):
            if filename.endswith(".json"):
                presets.append(filename[:-5])  # Remove .json
        return presets

    def delete(self, name):
        """Delete a preset.

        Args:
            name: Preset name

        Returns:
            bool: True if deleted successfully
        """
        filepath = os.path.join(self.presets_dir, f"{name}.json")
        if os.path.exists(filepath):
            os.remove(filepath)
            return True
        return False

    def get_default(self):
        """Get default preset settings.

        Returns:
            dict: Default settings
        """
        return self.DEFAULTS.copy()
