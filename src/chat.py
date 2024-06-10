# Necessary Imports
from src.utils import image_to_base64


# Function that takes User Inputs and displays it on ChatUI
def query_message(history, txt, img):
    """
    Adds a query message to the chat history.

    Parameters:
    history (list): The chat history.
    txt (str): The text message.
    img (str): The image file path.

    Returns:
    list: The updated chat history.
    """
    if not img:
        history += [(txt, None)]
        return history

    # Convert Image to Base64
    base64 = image_to_base64(img)

    # Display Image on Chat UI and return the history
    data_url = f"data:image/jpeg;base64,{base64}"
    history += [(f"{txt} ![]({data_url})", None)]
    return history
