"""
Image Converter Pro — Image cropping module.
Free-form, center, and ratio-based cropping.
"""

from PIL import Image


class ImageCropper:
    """Image cropping with multiple modes.

    Supports free-form, center, and aspect ratio cropping.
    """

    @staticmethod
    def crop(img, x1, y1, x2, y2):
        """Crop image to specified coordinates.

        Automatically normalizes reversed coordinates.

        Args:
            img: PIL Image
            x1, y1: Top-left corner
            x2, y2: Bottom-right corner

        Returns:
            PIL Image: Cropped image

        Raises:
            ValueError: If crop region is invalid
        """
        # Normalize coordinates
        left = min(x1, x2)
        top = min(y1, y2)
        right = max(x1, x2)
        bottom = max(y1, y2)

        # Clamp to image bounds
        left = max(0, left)
        top = max(0, top)
        right = min(img.width, right)
        bottom = min(img.height, bottom)

        # Validate
        if right - left <= 0 or bottom - top <= 0:
            raise ValueError(f"Invalid crop region: ({left},{top}) to ({right},{bottom})")

        return img.crop((left, top, right, bottom))

    @staticmethod
    def crop_center(img, crop_width, crop_height):
        """Crop image from center.

        Args:
            img: PIL Image
            crop_width: Crop width
            crop_height: Crop height

        Returns:
            PIL Image: Center-cropped image
        """
        # Limit to image dimensions
        crop_width = min(crop_width, img.width)
        crop_height = min(crop_height, img.height)

        left = (img.width - crop_width) // 2
        top = (img.height - crop_height) // 2
        right = left + crop_width
        bottom = top + crop_height

        return img.crop((left, top, right, bottom))

    @staticmethod
    def crop_ratio(img, ratio_w, ratio_h):
        """Crop image to specified aspect ratio.

        Crops from center, keeping the maximum possible area.

        Args:
            img: PIL Image
            ratio_w: Width ratio (e.g., 16)
            ratio_h: Height ratio (e.g., 9)

        Returns:
            PIL Image: Ratio-cropped image
        """
        target_ratio = ratio_w / ratio_h
        current_ratio = img.width / img.height

        if current_ratio > target_ratio:
            # Image is wider, crop width
            new_width = int(img.height * target_ratio)
            new_height = img.height
        else:
            # Image is taller, crop height
            new_width = img.width
            new_height = int(img.width / target_ratio)

        return ImageCropper.crop_center(img, new_width, new_height)

    @staticmethod
    def calculate_canvas_coords(img_size, canvas_size, crop_coords):
        """Convert crop coordinates from canvas to original image coordinates.

        Args:
            img_size: (width, height) of original image
            canvas_size: (width, height) of canvas
            crop_coords: (x1, y1, x2, y2) on canvas

        Returns:
            tuple: (x1, y1, x2, y2) in original image coordinates
        """
        img_w, img_h = img_size
        canvas_w, canvas_h = canvas_size
        cx1, cy1, cx2, cy2 = crop_coords

        scale_x = img_w / canvas_w
        scale_y = img_h / canvas_h

        return (
            int(cx1 * scale_x),
            int(cy1 * scale_y),
            int(cx2 * scale_x),
            int(cy2 * scale_y)
        )
