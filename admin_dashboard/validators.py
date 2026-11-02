
import warnings

from django.core.exceptions import ValidationError
from PIL import Image, UnidentifiedImageError


MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5 MB
MAX_IMAGE_PIXELS = 25_000_000

ALLOWED_IMAGE_FORMATS = {
    "JPEG",
    "PNG",
    "WEBP",
}


def validate_product_image(image_file):
    """
    Validate uploaded product images.
    Allowed formats: JPEG, PNG, WEBP.
    Maximum size: 5 MB.
    Maximum pixels: 25 million.
    """

    if not image_file:
        raise ValidationError("Please upload an image.")

    if image_file.size > MAX_IMAGE_SIZE:
        raise ValidationError(
            "Image size cannot exceed 5 MB."
        )

    try:
        image_file.seek(0)

        with warnings.catch_warnings():
            warnings.simplefilter(
                "error",
                Image.DecompressionBombWarning
            )

            with Image.open(image_file) as image:

                if image.format not in ALLOWED_IMAGE_FORMATS:
                    raise ValidationError(
                        "Only JPEG, PNG and WEBP images are allowed."
                    )

                if image.width * image.height > MAX_IMAGE_PIXELS:
                    raise ValidationError(
                        "Image dimensions are too large."
                    )

                image.verify()

    except ValidationError:
        raise

    except (
        UnidentifiedImageError,
        OSError,
        Image.DecompressionBombError,
        Image.DecompressionBombWarning,
    ):
        raise ValidationError(
            "Invalid or corrupted image file."
        )

    finally:
        image_file.seek(0)

    return image_file
