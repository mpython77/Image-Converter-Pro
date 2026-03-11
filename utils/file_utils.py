"""
Image Converter Pro — File utility functions.
Filename generation, folder operations, file info.
"""

import os
import platform
import subprocess
from datetime import datetime


def generate_output_filename(input_path, num, save_dir, fmt,
                              rename=False, pattern=""):
    """Generate output filename with optional renaming patterns.

    Supports placeholders:
        {num}  -> sequential number (001, 002, ...)
        {orig} -> original filename (without extension)
        {date} -> current date (2024-01-15)
        {time} -> current time (14-30-00)

    Args:
        input_path: Original file path
        num: Sequential number
        save_dir: Output directory
        fmt: Output format (JPEG, PNG, etc.)
        rename: Whether to use rename pattern
        pattern: Rename pattern string

    Returns:
        str: Full output file path
    """
    from config.constants import FORMAT_EXTENSIONS

    ext = FORMAT_EXTENSIONS.get(fmt, ".jpg")
    original_name = os.path.splitext(os.path.basename(input_path))[0]

    if rename and pattern:
        now = datetime.now()
        name = pattern.replace("{num}", f"{num:03d}")
        name = name.replace("{orig}", original_name)
        name = name.replace("{date}", now.strftime("%Y-%m-%d"))
        name = name.replace("{time}", now.strftime("%H-%M-%S"))
    else:
        name = original_name

    filename = f"{name}{ext}"
    output_path = os.path.join(save_dir, filename)

    # Prevent overwriting existing files
    counter = 1
    base_name = name
    while os.path.exists(output_path):
        name = f"{base_name}_{counter}"
        output_path = os.path.join(save_dir, f"{name}{ext}")
        counter += 1

    return output_path


def open_folder(folder_path):
    """Open a folder in the system's default file explorer.

    Args:
        folder_path: Path to the folder

    Returns:
        bool: True if successful
    """
    try:
        system = platform.system()
        if system == "Windows":
            os.startfile(folder_path)
        elif system == "Darwin":
            subprocess.Popen(["open", folder_path])
        else:
            subprocess.Popen(["xdg-open", folder_path])
        return True
    except Exception:
        return False


def format_file_size(size_bytes):
    """Format file size in human-readable form.

    Args:
        size_bytes: File size in bytes

    Returns:
        str: Formatted size string (e.g., '2.5 MB')
    """
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.2f} MB"


def get_image_info(filepath):
    """Get basic image file information.

    Args:
        filepath: Image file path

    Returns:
        dict: Image information (name, size, format, dimensions)
    """
    from PIL import Image

    info = {
        "name": os.path.basename(filepath),
        "size": format_file_size(os.path.getsize(filepath)),
        "path": filepath,
    }

    try:
        with Image.open(filepath) as img:
            info["width"] = img.width
            info["height"] = img.height
            info["format"] = img.format
            info["mode"] = img.mode
    except Exception:
        info["width"] = 0
        info["height"] = 0

    return info


def ensure_directory(directory):
    """Ensure a directory exists, creating it if necessary.

    Args:
        directory: Directory path
    """
    os.makedirs(directory, exist_ok=True)


def has_valid_extension(filepath):
    """Check if a file has a valid image extension.

    Args:
        filepath: File path to check

    Returns:
        bool: True if extension is valid
    """
    from config.constants import DND_EXTENSIONS
    ext = os.path.splitext(filepath)[1].lower()
    return ext in DND_EXTENSIONS
