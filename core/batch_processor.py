"""
Image Converter Pro — Parallel batch processing module.
Fast batch processing with ThreadPoolExecutor.
"""

import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from PIL import Image

from core.converter import ImageConverter
from core.effects import EffectsEngine
from core.watermark import WatermarkEngine
from utils.file_utils import generate_output_filename


class BatchProcessor:
    """Parallel batch image processing.

    Uses ThreadPoolExecutor to process multiple images simultaneously.
    Error-tolerant: continues processing if a single image fails.
    """

    def __init__(self, max_workers=4):
        """Create BatchProcessor.

        Args:
            max_workers: Number of parallel workers
        """
        self.max_workers = max_workers
        self.converter = ImageConverter()
        self.effects = EffectsEngine()
        self.watermark = WatermarkEngine()
        self._cancelled = False

    def cancel(self):
        """Cancel batch processing."""
        self._cancelled = True

    def reset(self):
        """Reset cancellation state."""
        self._cancelled = False

    def process_batch(self, image_paths, settings, save_dir, progress_callback=None):
        """Process multiple images in batch.

        Args:
            image_paths: List of image file paths
            settings: Processing settings (dict)
            save_dir: Output directory
            progress_callback: Progress function (index, total, filename, status)

        Returns:
            dict: {"success": int, "failed": int, "errors": list}
        """
        self.reset()
        total = len(image_paths)
        results = {"success": 0, "failed": 0, "errors": []}

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {}

            for i, path in enumerate(image_paths):
                if self._cancelled:
                    break

                future = executor.submit(
                    self._process_single,
                    path, settings, save_dir, i + 1
                )
                futures[future] = (i, path)

            for future in as_completed(futures):
                if self._cancelled:
                    break

                idx, path = futures[future]
                filename = os.path.basename(path)

                try:
                    output_path = future.result()
                    results["success"] += 1

                    if progress_callback:
                        progress_callback(
                            idx, total, filename,
                            f"✅ Saved: {os.path.basename(output_path)}"
                        )

                except Exception as e:
                    results["failed"] += 1
                    error_msg = f"{filename}: {str(e)}"
                    results["errors"].append(error_msg)

                    if progress_callback:
                        progress_callback(
                            idx, total, filename,
                            f"❌ Error: {filename} - {str(e)}"
                        )

        return results

    def _process_single(self, image_path, settings, save_dir, num):
        """Process a single image (runs inside worker thread).

        Args:
            image_path: Input file path
            settings: Settings dictionary
            save_dir: Output directory
            num: Sequential number

        Returns:
            str: Output file path

        Raises:
            Exception: If processing fails
        """
        if self._cancelled:
            raise Exception("Cancelled")

        # 1. Load image ONLY ONCE
        img = ImageConverter.load(image_path)

        # 2. Resize
        width = settings.get("width")
        height = settings.get("height")
        if width and height:
            try:
                img = ImageConverter.resize(
                    img, width, height,
                    maintain_ratio=settings.get("maintain_ratio", True)
                )
            except Exception:
                pass  # Invalid dimensions — skip resize

        # 3. Rotate
        angle = settings.get("angle", 0)
        try:
            if angle and float(angle) != 0:
                img = ImageConverter.rotate(img, angle)
        except (ValueError, TypeError):
            pass  # Invalid angle — skip rotate

        # 4. Effects (brightness, contrast, filters)
        img = self.effects.apply_all(img, settings)

        # 5. Watermark
        if settings.get("watermark", False) and settings.get("watermark_text"):
            img = self.watermark.add_text_watermark(
                img,
                text=settings["watermark_text"],
                position=settings.get("watermark_position", "bottom-right"),
                opacity=settings.get("watermark_opacity", 0.5),
            )

        # 6. Format conversion (RGBA -> RGB etc.)
        fmt = settings.get("format", "JPEG")
        img = ImageConverter.convert_format(img, fmt)

        # 7. Generate output filename
        output_path = generate_output_filename(
            image_path, num, save_dir, fmt,
            rename=settings.get("rename", False),
            pattern=settings.get("rename_pattern", ""),
        )

        # 8. Save
        quality = settings.get("quality", 85)
        ImageConverter.save(img, output_path, fmt, quality)

        return output_path
