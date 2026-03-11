"""
Image Converter Pro — Watermark engine module.
Text watermark with font fallback and shadow.
"""

from PIL import Image, ImageDraw, ImageFont


class WatermarkEngine:
    """Text watermark engine with font fallback and opacity control."""

    # Font fallback list (cross-platform)
    FONT_FALLBACKS = [
        "arial.ttf", "Arial.ttf",
        "DejaVuSans.ttf", "FreeSans.ttf",
        "Helvetica.ttf",
    ]

    @staticmethod
    def _get_font(size=24):
        """Get best available font with fallback.

        Args:
            size: Font size in pixels

        Returns:
            ImageFont: Loaded font
        """
        for font_name in WatermarkEngine.FONT_FALLBACKS:
            try:
                return ImageFont.truetype(font_name, size)
            except (OSError, IOError):
                continue
        return ImageFont.load_default()

    @staticmethod
    def _calculate_position(img_size, text_size, position):
        """Calculate watermark position coordinates.

        Args:
            img_size: (width, height) of the image
            text_size: (width, height) of the text
            position: Position string ("top-left", "center", etc.)

        Returns:
            tuple: (x, y) coordinates
        """
        img_w, img_h = img_size
        txt_w, txt_h = text_size
        margin = 20

        positions = {
            "top-left": (margin, margin),
            "top-right": (img_w - txt_w - margin, margin),
            "bottom-left": (margin, img_h - txt_h - margin),
            "bottom-right": (img_w - txt_w - margin, img_h - txt_h - margin),
            "center": ((img_w - txt_w) // 2, (img_h - txt_h) // 2),
        }

        return positions.get(position, positions["bottom-right"])

    def add_text_watermark(self, img, text, position="bottom-right",
                            opacity=0.5, font_size=24):
        """Add text watermark to image.

        Features:
            - Font fallback (cross-platform)
            - Text shadow for readability
            - Opacity control via alpha compositing

        Args:
            img: PIL Image
            text: Watermark text
            position: Position ("top-left", "top-right", "bottom-left",
                       "bottom-right", "center")
            opacity: Text opacity (0.0-1.0)
            font_size: Font size in pixels

        Returns:
            PIL Image: Image with watermark
        """
        if not text:
            return img

        # Convert to RGBA for transparency support
        base = img.convert("RGBA")
        watermark_layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(watermark_layer)

        font = self._get_font(font_size)

        # Calculate text size
        bbox = draw.textbbox((0, 0), text, font=font)
        text_size = (bbox[2] - bbox[0], bbox[3] - bbox[1])

        # Calculate position
        x, y = self._calculate_position(base.size, text_size, position)

        # Draw shadow (offset by 2px)
        shadow_alpha = int(128 * opacity)
        draw.text((x + 2, y + 2), text, fill=(0, 0, 0, shadow_alpha), font=font)

        # Draw main text
        text_alpha = int(255 * opacity)
        draw.text((x, y), text, fill=(255, 255, 255, text_alpha), font=font)

        # Composite
        result = Image.alpha_composite(base, watermark_layer)

        # Convert back to original mode
        if img.mode == "RGB":
            return result.convert("RGB")
        return result
