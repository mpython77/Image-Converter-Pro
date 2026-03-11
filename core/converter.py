"""
Image Converter Pro — Core image conversion module.
Format conversion, resize, and rotate operations.
"""

from PIL import Image
from utils.validators import validate_dimensions, validate_angle, validate_quality, validate_format


class ImageConverter:
    """Image conversion and transformation class.

    Thread-safe: all parameters are passed as arguments,
    no Tkinter variables are used directly.
    """

    @staticmethod
    def resize(img, width, height, maintain_ratio=True):
        """Resize an image.

        Args:
            img: PIL Image
            width: New width
            height: New height
            maintain_ratio: Whether to maintain aspect ratio

        Returns:
            PIL Image: Resized image
        """
        w, h = validate_dimensions(width, height)

        if maintain_ratio:
            img_copy = img.copy()
            img_copy.thumbnail((w, h), Image.Resampling.LANCZOS)
            return img_copy
        else:
            return img.resize((w, h), Image.Resampling.LANCZOS)

    @staticmethod
    def rotate(img, angle):
        """Rotate an image.

        Args:
            img: PIL Image
            angle: Rotation angle in degrees

        Returns:
            PIL Image: Rotated image
        """
        a = validate_angle(angle)
        if a == 0:
            return img
        return img.rotate(a, expand=True, resample=Image.Resampling.BICUBIC)

    @staticmethod
    def convert_format(img, target_format):
        """Prepare image for format conversion.

        Handles mode conversions (RGBA->RGB, P->RGB, etc.)

        Args:
            img: PIL Image
            target_format: Target format ("JPEG", "PNG", etc.)

        Returns:
            PIL Image: Image ready for saving in target format
        """
        fmt = validate_format(target_format)

        # RGBA -> RGB (for JPEG/WEBP/BMP)
        if fmt in ("JPEG", "WEBP", "BMP") and img.mode == "RGBA":
            background = Image.new("RGB", img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[3])
            return background

        # P mode -> RGB (for JPEG)
        if fmt == "JPEG" and img.mode == "P":
            return img.convert("RGB")

        # Other modes -> RGB (for JPEG)
        if fmt == "JPEG" and img.mode not in ("RGB", "L"):
            return img.convert("RGB")

        return img

    @staticmethod
    def save(img, output_path, fmt, quality=85):
        """Save image to file.

        Args:
            img: PIL Image
            output_path: Output file path
            fmt: Format ("JPEG", "PNG", etc.)
            quality: Quality (1-100, JPEG/WEBP only)

        Returns:
            str: Saved file path
        """
        fmt = validate_format(fmt)
        quality = validate_quality(quality)

        save_options = {}

        if fmt in ("JPEG", "WEBP"):
            save_options["quality"] = quality

        if fmt == "JPEG":
            save_options["optimize"] = True

        if fmt == "PNG":
            save_options["optimize"] = True

        img.save(output_path, format=fmt, **save_options)
        return output_path

    @staticmethod
    def load(image_path):
        """Load image from file.

        Args:
            image_path: File path

        Returns:
            PIL Image: Loaded image

        Raises:
            IOError: If file cannot be opened
        """
        img = Image.open(image_path)
        img.load()  # Force full loading (not lazy)
        return img

    def process(self, image_path, settings):
        """Process image with given settings.

        Args:
            image_path: Input file path
            settings: Settings dictionary:
                - width (int): Width
                - height (int): Height
                - maintain_ratio (bool): Maintain aspect ratio
                - angle (float): Rotation angle
                - format (str): Output format

        Returns:
            PIL Image: Processed image
        """
        img = self.load(image_path)

        # Resize
        width = settings.get("width")
        height = settings.get("height")
        if width and height:
            maintain = settings.get("maintain_ratio", True)
            img = self.resize(img, width, height, maintain)

        # Rotate
        angle = settings.get("angle", 0)
        if angle and float(angle) != 0:
            img = self.rotate(img, angle)

        # Format conversion prep
        fmt = settings.get("format", "JPEG")
        img = self.convert_format(img, fmt)

        return img
