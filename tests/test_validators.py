"""
Test — Validators moduli.
"""

import pytest
import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from utils.validators import (
    ValidationError,
    validate_dimensions,
    validate_angle,
    validate_quality,
    validate_image_path,
    validate_format,
    validate_opacity,
    validate_effect_value,
)


class TestValidateDimensions:
    def test_valid_dimensions(self):
        w, h = validate_dimensions(800, 600)
        assert w == 800
        assert h == 600

    def test_string_dimensions(self):
        w, h = validate_dimensions("800", "600")
        assert w == 800

    def test_invalid_string(self):
        with pytest.raises(ValidationError):
            validate_dimensions("abc", 600)

    def test_negative(self):
        with pytest.raises(ValidationError):
            validate_dimensions(-100, 600)

    def test_zero(self):
        with pytest.raises(ValidationError):
            validate_dimensions(0, 600)

    def test_too_large(self):
        with pytest.raises(ValidationError):
            validate_dimensions(25000, 600)


class TestValidateAngle:
    def test_valid_angle(self):
        assert validate_angle(90) == 90.0

    def test_float_angle(self):
        assert validate_angle(45.5) == 45.5

    def test_string_angle(self):
        assert validate_angle("90") == 90.0

    def test_invalid_string(self):
        with pytest.raises(ValidationError):
            validate_angle("abc")

    def test_out_of_range(self):
        with pytest.raises(ValidationError):
            validate_angle(500)


class TestValidateQuality:
    def test_valid(self):
        assert validate_quality(85) == 85

    def test_min(self):
        assert validate_quality(1) == 1

    def test_max(self):
        assert validate_quality(100) == 100

    def test_zero(self):
        with pytest.raises(ValidationError):
            validate_quality(0)

    def test_over_max(self):
        with pytest.raises(ValidationError):
            validate_quality(101)


class TestValidateFormat:
    def test_jpeg(self):
        assert validate_format("JPEG") == "JPEG"

    def test_lowercase(self):
        assert validate_format("jpeg") == "JPEG"

    def test_png(self):
        assert validate_format("PNG") == "PNG"

    def test_invalid(self):
        with pytest.raises(ValidationError):
            validate_format("INVALID")


class TestValidateOpacity:
    def test_valid(self):
        assert validate_opacity(0.5) == 0.5

    def test_min(self):
        assert validate_opacity(0.0) == 0.0

    def test_max(self):
        assert validate_opacity(1.0) == 1.0

    def test_over_max(self):
        with pytest.raises(ValidationError):
            validate_opacity(1.5)

    def test_negative(self):
        with pytest.raises(ValidationError):
            validate_opacity(-0.1)


class TestValidateImagePath:
    def test_valid_path(self):
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            path = f.name

        try:
            result = validate_image_path(path)
            assert result == path
        finally:
            os.unlink(path)

    def test_nonexistent(self):
        with pytest.raises(ValidationError):
            validate_image_path("/nonexistent/file.png")

    def test_empty(self):
        with pytest.raises(ValidationError):
            validate_image_path("")

    def test_wrong_extension(self):
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as f:
            path = f.name

        try:
            with pytest.raises(ValidationError):
                validate_image_path(path)
        finally:
            os.unlink(path)


class TestValidateEffectValue:
    def test_valid(self):
        assert validate_effect_value(1.0) == 1.0

    def test_invalid(self):
        with pytest.raises(ValidationError):
            validate_effect_value("abc")
