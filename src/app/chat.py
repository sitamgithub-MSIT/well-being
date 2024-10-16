# Necessary imports
import sys
from typing import List, Tuple, Optional
from src.utils import image_to_base64

# local imports
from src.logger import logging
from src.exception import CustomExceptionHandling


def query_message(
    history: List[Tuple[str, Optional[str]]], txt: str, img: Optional[str]
) -> List[Tuple[str, Optional[str]]]:
    """
    Adds a query message to the chat history.

    Args:
        - history (List[Tuple[str, Optional[str]]]): The chat history.
        - txt (str): The text message.
        - img (Optional[str]): The image file path.

    Returns:
        List[Tuple[str, Optional[str]]]: The updated chat history.
    """
    try:
        # Add Text Message to Chat History
        if not img:
            history.append((txt, None))
            logging.info("Added text message to chat history.")
            return history

        # Convert Image to Base64
        base64 = image_to_base64(img)

        # Display Image on Chat UI and return the history
        data_url = f"data:image/jpeg;base64,{base64}"
        history.append((f"{txt} ![]({data_url})", None))
        logging.info("Added text message with image to chat history.")
        return history

    # Handle exceptions that may occur during chat history update
    except Exception as e:
        # Custom exception handling
        raise CustomExceptionHandling(e, sys) from e
