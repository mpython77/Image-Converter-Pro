"""
Image Converter Pro — Input validation module.
Comprehensive validation for dimensions, angles, quality, paths, formats.
"""

import os


class ValidationError(Exception):
    """Custom validation error with descriptive messages."""
    pass


def validate_dimensions(width, height, max_dim=20000):
    """Validate image dimensions.

    Args:
        width: Image width (int or str)
        height: Image height (int or str)
        max_dim: Maximum allowed dimension

    Returns:
        tuple: (width, height) as integers

    Raises:
        ValidationError: If dimensions are invalid
    """
    try:
        w = int(width)
        h = int(height)
    except (ValueError, TypeError):
        raise ValidationError(f"Invalid dimensions: {width}x{height}. Must be integers.")

    if w <= 0 or h <= 0:
        raise ValidationError(f"Dimensions must be positive: {w}x{h}")

    if w > max_dim or h > max_dim:
        raise ValidationError(f"Dimensions too large: {w}x{h}. Max: {max_dim}")

    return w, h


def validate_angle(angle):
    """Validate rotation angle.

    Args:
        angle: Rotation angle (int, float, or str)

    Returns:
        float: Validated angle

    Raises:
        ValidationError: If angle is invalid
    """
    try:
        a = float(angle)
    except (ValueError, TypeError):
        raise ValidationError(f"Invalid angle: {angle}. Must be a number.")

    if a < -360 or a > 360:
        raise ValidationError(f"Angle out of range: {a}. Must be -360 to 360.")

    return a


def validate_quality(quality):
    """Validate image quality.

    Args:
        quality: Quality value (1-100)

    Returns:
        int: Validated quality

    Raises:
        ValidationError: If quality is invalid
    """
    try:
        q = int(quality)
    except (ValueError, TypeError):
        raise ValidationError(f"Invalid quality: {quality}. Must be an integer.")

    if q < 1 or q > 100:
        raise ValidationError(f"Quality out of range: {q}. Must be 1-100.")

    return q


def validate_image_path(path):
    """Validate image file path.

    Args:
        path: File path to validate

    Returns:
        str: Validated path

    Raises:
        ValidationError: If path is invalid
    """
    if not path or not path.strip():
        raise ValidationError("Image path cannot be empty.")

    if not os.path.exists(path):
        raise ValidationError(f"File not found: {path}")

    valid_extensions = {".png", ".jpg", ".jpeg", ".bmp", ".gif", ".tiff", ".webp", ".ico"}
    ext = os.path.splitext(path)[1].lower()

    if ext not in valid_extensions:
        raise ValidationError(f"Unsupported file format: {ext}. Supported: {', '.join(valid_extensions)}")

    return path


def validate_format(fmt):
    """Validate output format.

    Args:
        fmt: Format string (e.g., 'JPEG', 'PNG')

    Returns:
        str: Validated format (uppercase)

    Raises:
        ValidationError: If format is unsupported
    """
    from config.constants import SUPPORTED_FORMATS

    fmt_upper = fmt.strip().upper()

    if fmt_upper not in SUPPORTED_FORMATS:
        raise ValidationError(f"Unsupported format: {fmt}. Supported: {', '.join(SUPPORTED_FORMATS)}")

    return fmt_upper


def validate_opacity(opacity):
    """Validate opacity value.

    Args:
        opacity: Opacity value (0.0 - 1.0)

    Returns:
        float: Validated opacity

    Raises:
        ValidationError: If opacity is invalid
    """
    try:
        o = float(opacity)
    except (ValueError, TypeError):
        raise ValidationError(f"Invalid opacity: {opacity}. Must be a number.")

    if o < 0.0 or o > 1.0:
        raise ValidationError(f"Opacity out of range: {o}. Must be 0.0-1.0.")

    return o


def validate_effect_value(value, name="Effect"):
    """Validate effect parameter value.

    Args:
        value: Effect value to validate
        name: Name of the effect (for error messages)

    Returns:
        float: Validated value

    Raises:
        ValidationError: If value is invalid
    """
    try:
        v = float(value)
    except (ValueError, TypeError):
        raise ValidationError(f"Invalid {name} value: {value}. Must be a number.")

    return v
