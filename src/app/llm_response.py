# Necessary imports
import os
import sys
from typing import List, Tuple, Optional
import PIL.Image
import google.generativeai as genai
from dotenv import load_dotenv

# local imports
from src.config import generation_config, safety_settings, model_name
from src.app.prompt import system_prompt
from src.logger import logging
from src.exception import CustomExceptionHandling


# Load the Environment Variables from .env file
load_dotenv()

# Set the Gemini API Key
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

# Create the Gemini Models for Text and Vision respectively
txt_model = genai.GenerativeModel(
    model_name=model_name,
    generation_config=generation_config,
    safety_settings=safety_settings,
    system_instruction=system_prompt,
)
vis_model = genai.GenerativeModel(
    model_name=model_name,
    generation_config=generation_config,
    safety_settings=safety_settings,
    system_instruction=system_prompt,
)


def llm_response(
    history: List[Tuple[Optional[str], Optional[str]]], text: str, img: Optional[str]
) -> List[Tuple[Optional[str], Optional[str]]]:
    """
    Generate a response based on the input.
    Args:
        - history (List[Tuple[Optional[str], Optional[str]]]): A list of previous chat history.
        - text (str): The input text.
        - img (Optional[str]): The path to an image file (optional).
    Returns:
        List[Tuple[Optional[str], Optional[str]]]: The updated chat history.
    """
    try:
        if not img:
            chat_session = txt_model.start_chat(history=[])

            # Convert chat history to string for context
            history_str = "\n".join(
                [
                    f"User: {msg[0]}\n{msg[1]}" if msg[1] else f"User: {msg[0]}"
                    for msg in history
                ]
            )

            # Generate Response
            response = chat_session.send_message(
                f"History:\n{history_str}\nUser: {text}"
            )
        else:
            # Open Image and Generate Response
            try:
                img = PIL.Image.open(img)

            except Exception as e:
                # Custom exception handling
                raise CustomExceptionHandling(e, sys) from e

            # Start Chat Session for Image and Generate Response
            chat_session = vis_model.start_chat(history=[])
            response = chat_session.send_message([f"User: {text}", img])

        # Display Response on Chat UI and return the history
        history.append((None, response.text))
        logging.info("Response added to chat history.")
        return history

    # Handle exceptions that may occur during llm response generation
    except Exception as e:
        # Custom exception handling
        raise CustomExceptionHandling(e, sys) from e
