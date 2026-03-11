"""
Image Converter Pro — Effects engine module.
Brightness, contrast, filters, and artistic effects.
"""

import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
from utils.validators import validate_effect_value


class EffectsEngine:
    """Image effects and filters engine.

    Provides static methods for adjustments and filters.
    Thread-safe: all methods accept parameters as arguments.
    """

    # ========== Adjustments ==========

    @staticmethod
    def adjust_brightness(img, factor):
        """Adjust image brightness.

        Args:
            img: PIL Image
            factor: Brightness factor (0=black, 1=original, 2=bright)

        Returns:
            PIL Image: Adjusted image
        """
        factor = validate_effect_value(factor, "Brightness")
        if factor == 1.0:
            return img
        return ImageEnhance.Brightness(img).enhance(factor)

    @staticmethod
    def adjust_contrast(img, factor):
        """Adjust image contrast.

        Args:
            img: PIL Image
            factor: Contrast factor (0=gray, 1=original, 2=high)

        Returns:
            PIL Image: Adjusted image
        """
        factor = validate_effect_value(factor, "Contrast")
        if factor == 1.0:
            return img
        return ImageEnhance.Contrast(img).enhance(factor)

    @staticmethod
    def adjust_saturation(img, factor):
        """Adjust image color saturation.

        Args:
            img: PIL Image
            factor: Saturation factor (0=grayscale, 1=original, 2=vivid)

        Returns:
            PIL Image: Adjusted image
        """
        factor = validate_effect_value(factor, "Saturation")
        if factor == 1.0:
            return img
        return ImageEnhance.Color(img).enhance(factor)

    @staticmethod
    def adjust_sharpness(img, factor):
        """Adjust image sharpness.

        Args:
            img: PIL Image
            factor: Sharpness factor (0=blurred, 1=original, 2=sharp)

        Returns:
            PIL Image: Adjusted image
        """
        factor = validate_effect_value(factor, "Sharpness")
        if factor == 1.0:
            return img
        return ImageEnhance.Sharpness(img).enhance(factor)

    # ========== Filters ==========

    @staticmethod
    def apply_blur(img):
        """Apply Gaussian blur filter."""
        return img.filter(ImageFilter.GaussianBlur(radius=2))

    @staticmethod
    def apply_sharpen(img):
        """Apply sharpen filter."""
        return img.filter(ImageFilter.SHARPEN)

    @staticmethod
    def apply_edge_enhance(img):
        """Apply edge enhancement filter."""
        return img.filter(ImageFilter.EDGE_ENHANCE_MORE)

    @staticmethod
    def apply_emboss(img):
        """Apply emboss filter."""
        return img.filter(ImageFilter.EMBOSS)

    @staticmethod
    def apply_contour(img):
        """Apply contour detection filter."""
        return img.filter(ImageFilter.CONTOUR)

    @staticmethod
    def apply_grayscale(img):
        """Convert image to grayscale."""
        return img.convert("L")

    @staticmethod
    def apply_sepia(img):
        """Apply sepia tone effect.

        Converts image to warm brownish tones.
        Preserves alpha channel if present.
        """
        has_alpha = img.mode == "RGBA"
        alpha = None

        if has_alpha:
            alpha = img.split()[3]
            img = img.convert("RGB")

        img_array = np.array(img, dtype=np.float64)

        # Sepia transformation matrix
        sepia_matrix = np.array([
            [0.393, 0.769, 0.189],
            [0.349, 0.686, 0.168],
            [0.272, 0.534, 0.131]
        ])

        sepia_array = img_array @ sepia_matrix.T
        sepia_array = np.clip(sepia_array, 0, 255).astype(np.uint8)

        result = Image.fromarray(sepia_array, "RGB")

        if has_alpha and alpha:
            result.putalpha(alpha)

        return result

    @staticmethod
    def apply_vignette(img, strength=0.5):
        """Apply vignette effect (darker edges).

        Args:
            img: PIL Image
            strength: Vignette intensity (0.0-1.0)
        """
        width, height = img.size
        img_array = np.array(img, dtype=np.float64)

        # Create vignette mask
        x = np.linspace(-1, 1, width)
        y = np.linspace(-1, 1, height)
        X, Y = np.meshgrid(x, y)
        dist = np.sqrt(X**2 + Y**2)

        vignette = 1 - (dist * strength)
        vignette = np.clip(vignette, 0, 1)

        # Apply to each channel
        if len(img_array.shape) == 3:
            for c in range(min(3, img_array.shape[2])):
                img_array[:, :, c] *= vignette
        else:
            img_array *= vignette

        result_array = np.clip(img_array, 0, 255).astype(np.uint8)
        return Image.fromarray(result_array, img.mode)

    @staticmethod
    def auto_enhance(img):
        """Automatically enhance image (brightness + contrast + sharpness).

        Applies moderate improvements across all parameters.
        """
        img = ImageEnhance.Brightness(img).enhance(1.1)
        img = ImageEnhance.Contrast(img).enhance(1.15)
        img = ImageEnhance.Sharpness(img).enhance(1.2)
        img = ImageEnhance.Color(img).enhance(1.1)
        return img

    # ========== Batch apply ==========

    def apply_all(self, img, settings):
        """Apply all specified effects to an image.

        Args:
            img: PIL Image
            settings: Settings dictionary with effect parameters

        Returns:
            PIL Image: Image with all effects applied
        """
        # Adjustments
        brightness = settings.get("brightness", 1.0)
        if brightness != 1.0:
            img = self.adjust_brightness(img, brightness)

        contrast = settings.get("contrast", 1.0)
        if contrast != 1.0:
            img = self.adjust_contrast(img, contrast)

        saturation = settings.get("saturation", 1.0)
        if saturation != 1.0:
            img = self.adjust_saturation(img, saturation)

        sharpness = settings.get("sharpness", 1.0)
        if sharpness != 1.0:
            img = self.adjust_sharpness(img, sharpness)

        # Filters
        if settings.get("blur", False):
            img = self.apply_blur(img)
        if settings.get("sharpen", False):
            img = self.apply_sharpen(img)
        if settings.get("edge_enhance", False):
            img = self.apply_edge_enhance(img)
        if settings.get("emboss", False):
            img = self.apply_emboss(img)
        if settings.get("contour", False):
            img = self.apply_contour(img)
        if settings.get("grayscale", False):
            img = self.apply_grayscale(img)
        if settings.get("sepia", False):
            img = self.apply_sepia(img)
        if settings.get("vignette", False):
            img = self.apply_vignette(img)
        if settings.get("auto_enhance", False):
            img = self.auto_enhance(img)

        return img
