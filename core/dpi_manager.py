"""
Image Converter Pro — DPI Manager module.
DPI setting, conversion, and print size calculation.
"""

from PIL import Image
from config.constants import DEFAULT_DPI, PRINT_DPI


class DPIManager:
    """DPI (Dots Per Inch) management class."""

    @staticmethod
    def get_dpi(img):
        """Get image DPI value.

        Args:
            img: PIL Image

        Returns:
            tuple: (x_dpi, y_dpi)
        """
        dpi = img.info.get("dpi", (DEFAULT_DPI, DEFAULT_DPI))
        if isinstance(dpi, (int, float)):
            return (int(dpi), int(dpi))
        return (int(dpi[0]), int(dpi[1]))

    @staticmethod
    def set_dpi(img, dpi_x, dpi_y=None):
        """Set image DPI.

        Args:
            img: PIL Image
            dpi_x: Horizontal DPI
            dpi_y: Vertical DPI (defaults to dpi_x if None)

        Returns:
            PIL Image: Image with updated DPI
        """
        if dpi_y is None:
            dpi_y = dpi_x

        img_copy = img.copy()
        img_copy.info["dpi"] = (int(dpi_x), int(dpi_y))
        return img_copy

    @staticmethod
    def convert_to_print(img):
        """Convert image to print quality (300 DPI).

        Args:
            img: PIL Image

        Returns:
            PIL Image: Image with 300 DPI
        """
        return DPIManager.set_dpi(img, PRINT_DPI)

    @staticmethod
    def convert_to_web(img):
        """Convert image to web quality (72 DPI).

        Args:
            img: PIL Image

        Returns:
            PIL Image: Image with 72 DPI
        """
        return DPIManager.set_dpi(img, DEFAULT_DPI)

    @staticmethod
    def calculate_print_size_cm(img):
        """Calculate printable size in centimeters.

        Args:
            img: PIL Image

        Returns:
            tuple: (width_cm, height_cm)
        """
        dpi = DPIManager.get_dpi(img)
        width_inches = img.width / dpi[0]
        height_inches = img.height / dpi[1]
        return (round(width_inches * 2.54, 1), round(height_inches * 2.54, 1))
