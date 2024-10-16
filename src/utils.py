# Necessary imports
import sys
import base64
from typing import Optional

# local imports
from src.logger import logging
from src.exception import CustomExceptionHandling


def image_to_base64(image_path: str) -> Optional[str]:
    """
    Convert an image file to a base64 encoded string.

    Args:
        image_path (str): The path to the image file.

    Returns:
        Optional[str]: The base64 encoded string representation of the image, or None if an error occurs.
    """
    try:
        # Open the image file and convert it to a base64 encoded string
        with open(image_path, "rb") as img:
            encoded_string = base64.b64encode(img.read())

        # Log the successful conversion
        logging.info(f"Image at {image_path} successfully encoded to base64.")

        # Return the base64 encoded string
        return encoded_string.decode("utf-8")

    # Handle exceptions that may occur during the conversion
    except Exception as e:
        # Custom exception handling
        raise CustomExceptionHandling(e, sys) from e
