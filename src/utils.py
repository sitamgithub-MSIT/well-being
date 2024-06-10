# Necessary Imports
import base64


# Image to Base 64 Converter Function
def image_to_base64(image_path):
    """
    Convert an image file to a base64 encoded string.

    Args:
        image_path (str): The path to the image file.

    Returns:
        str: The base64 encoded string representation of the image.
    """
    # Open Image and Encode it to Base64
    with open(image_path, "rb") as img:
        encoded_string = base64.b64encode(img.read())

    # Return the Encoded String
    return encoded_string.decode("utf-8")
