"""
Image Converter Pro — EXIF metadata reader module.
Extracts EXIF data, camera info, and basic image details.
"""

import os
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS


class MetadataReader:
    """Reads EXIF metadata and basic image information."""

    @staticmethod
    def read_exif(image_path):
        """Read EXIF data from an image file.

        Args:
            image_path: Image file path

        Returns:
            dict: EXIF data with human-readable tag names, or empty dict
        """
        try:
            img = Image.open(image_path)
            exif_data = img._getexif()
            if not exif_data:
                return {}

            result = {}
            for tag_id, value in exif_data.items():
                tag_name = TAGS.get(tag_id, tag_id)
                if isinstance(value, bytes):
                    try:
                        value = value.decode("utf-8", errors="ignore")
                    except Exception:
                        value = str(value)
                result[tag_name] = value

            return result

        except Exception:
            return {}

    @staticmethod
    def get_camera_info(exif_data):
        """Extract camera information from EXIF data.

        Args:
            exif_data: EXIF data dictionary

        Returns:
            dict: Camera information (make, model, exposure, ISO, etc.)
        """
        camera_tags = {
            "Make": "Camera Make",
            "Model": "Camera Model",
            "ExposureTime": "Exposure Time",
            "FNumber": "Aperture (f-stop)",
            "ISOSpeedRatings": "ISO Speed",
            "FocalLength": "Focal Length",
            "DateTimeOriginal": "Date Taken",
            "Flash": "Flash",
            "WhiteBalance": "White Balance",
            "LensModel": "Lens Model",
            "Software": "Software",
        }

        info = {}
        for exif_key, display_name in camera_tags.items():
            if exif_key in exif_data:
                value = exif_data[exif_key]
                if isinstance(value, tuple) and len(value) == 2:
                    value = f"{value[0]}/{value[1]}"
                info[display_name] = str(value)

        return info

    @staticmethod
    def get_gps_info(exif_data):
        """Extract GPS information from EXIF data.

        Args:
            exif_data: EXIF data dictionary

        Returns:
            dict: GPS information or empty dict
        """
        gps_data = exif_data.get("GPSInfo", {})
        if not gps_data:
            return {}

        gps_info = {}
        for tag_id, value in gps_data.items():
            tag_name = GPSTAGS.get(tag_id, tag_id)
            gps_info[tag_name] = value

        return gps_info

    @staticmethod
    def get_basic_info(image_path):
        """Get basic image information (non-EXIF).

        Args:
            image_path: Image file path

        Returns:
            dict: Basic image info (dimensions, format, size, DPI)
        """
        info = {}
        try:
            file_size = os.path.getsize(image_path)

            if file_size < 1024:
                size_str = f"{file_size} B"
            elif file_size < 1024 * 1024:
                size_str = f"{file_size / 1024:.1f} KB"
            else:
                size_str = f"{file_size / (1024 * 1024):.2f} MB"

            info["File Name"] = os.path.basename(image_path)
            info["File Size"] = size_str

            with Image.open(image_path) as img:
                info["Dimensions"] = f"{img.width} × {img.height} px"
                info["Format"] = img.format or "Unknown"
                info["Color Mode"] = img.mode
                megapixels = (img.width * img.height) / 1_000_000
                info["Megapixels"] = f"{megapixels:.1f} MP"

                dpi = img.info.get("dpi")
                if dpi:
                    info["DPI"] = f"{int(dpi[0])} × {int(dpi[1])}"

        except Exception:
            info["Error"] = "Could not read image information"

        return info

    def format_metadata(self, image_path):
        """Get formatted metadata text for display.

        Args:
            image_path: Image file path

        Returns:
            str: Formatted metadata text
        """
        lines = []

        # Basic info
        basic = self.get_basic_info(image_path)
        lines.append("=== Image Information ===")
        for key, value in basic.items():
            lines.append(f"  {key}: {value}")

        # EXIF
        exif = self.read_exif(image_path)
        if exif:
            camera = self.get_camera_info(exif)
            if camera:
                lines.append("\n=== Camera Information ===")
                for key, value in camera.items():
                    lines.append(f"  {key}: {value}")

            gps = self.get_gps_info(exif)
            if gps:
                lines.append("\n=== GPS Information ===")
                for key, value in gps.items():
                    lines.append(f"  {key}: {value}")

        return "\n".join(lines)
