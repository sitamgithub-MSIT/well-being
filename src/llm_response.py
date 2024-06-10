# Necessary Imports
import os
import PIL.Image
import google.generativeai as genai

# Import the necessary requirements from the src folder
from dotenv import load_dotenv
from src.config import generation_config, safety_settings, model_name
from src.prompt import system_prompt

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


# Function that takes User Inputs, generates Response and displays on Chat UI
def llm_response(history, text, img):
    """
    Generate a response based on the input.

    Parameters:
    history (list): A list of previous chat history.
    text (str): The input text.
    img (str): The path to an image file (optional).

    Returns:
    list: The updated chat history.
    """

    # Generate Response based on the Input
    if not img:
        # response = txt_model.generate_content(f"{system_prompt}User: {text}")
        chat_session = txt_model.start_chat(history=[])

        # Convert chat history to string for context
        history_str = "\n".join(
            [
                f"User: {msg[0]}\n{msg[1]}" if msg[1] else f"User: {msg[0]}"
                for msg in history
            ]
        )

        response = chat_session.send_message(f"History:\n{history_str}\nUser: {text}")
    else:
        # Open Image and Generate Response
        img = PIL.Image.open(img)
        chat_session = vis_model.start_chat(history=[])
        response = chat_session.send_message([f"User: {text}", img])

        # response = vis_model.generate_content([f"{system_prompt}User: {text}", img])

    # Display Response on Chat UI and return the history
    history += [(None, response.text)]
    return history
