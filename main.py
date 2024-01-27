# Necessary Imports
import os
import time
import base64
import PIL.Image
import gradio as gr
import google.generativeai as genai

from dotenv import load_dotenv

# Load the Environment Variables
load_dotenv()

# Set the Gemini API Key
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

# Set up the model configuration for content generation
generation_config = {
    "temperature": 0.4,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 1400,
}

# Define safety settings for content generation
safety_settings = [
    {"category": f"HARM_CATEGORY_{category}", "threshold": "BLOCK_MEDIUM_AND_ABOVE"}
    for category in [
        "HARASSMENT",
        "HATE_SPEECH",
        "SEXUALLY_EXPLICIT",
        "DANGEROUS_CONTENT",
    ]
]

# Create the Gemini Models for Text and Vision respectively
txt_model = genai.GenerativeModel(
    model_name="gemini-pro",
    generation_config=generation_config,
    safety_settings=safety_settings,
)
vis_model = genai.GenerativeModel(
    model_name="gemini-pro-vision",
    generation_config=generation_config,
    safety_settings=safety_settings,
)

# System Prompt
system_prompt = """
Model: "As a trusted medical chatbot, your role is crucial in providing accurate information and guidance to users seeking medical assistance. 
You will be presented with symptoms, medical history, or queries related to various health concerns, and your task is to offer insightful analysis, recommendations, and information to aid users in understanding their health conditions and making informed decisions.

**Analysis Guidelines:**

1. **Symptom Evaluation:** Carefully assess the symptoms described by the user to understand their medical condition accurately.
2. **Medical History Review:** Consider any relevant medical history provided by the user to contextualize their current health concerns and potential risk factors.
3. **Diagnosis Discussion:** Based on the presented symptoms and medical history, discuss possible diagnoses or conditions that align with the user's situation.
4. **Treatment Options:** Provide information on recommended treatments, therapies, or lifestyle changes for managing the identified medical condition.
5. **Preventive Measures:** Offer preventive strategies or advice to help users minimize the risk of future health issues or complications.
6. **Important Note:** While your guidance is valuable, it's essential to emphasize the importance of consulting with qualified healthcare professionals for accurate diagnosis and personalized medical care.

**Refusal Policy:**
If the user provides information or queries not related to medical concerns, kindly inform them that this chatbot is designed to address only medical inquiries. Politely encourage them to seek assistance from appropriate sources for non-medical matters.

Your role as a medical chatbot is to empower users with knowledge and guidance to support their health and well-being. Proceed to assist users with their medical inquiries, ensuring clarity, empathy, and accuracy in your responses."

"""


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
        response = txt_model.generate_content(f"{system_prompt}User: {text}")
    else:
        # Open Image and Generate Response
        img = PIL.Image.open(img)
        response = vis_model.generate_content([f"{system_prompt}User: {text}", img])

    # Display Response on Chat UI and return the history
    history += [(None, response.text)]
    return history


# Interface Code using Gradio
with gr.Blocks() as demo:
    with gr.Row():
        # Image UI
        image_box = gr.Image(type="filepath")

        # Chat UI
        chatbot = gr.Chatbot(scale=2, height=750)
    text_box = gr.Textbox(
        placeholder="Enter text and press enter, or upload an image",
        container=False,
    )

    # Button to Submit the Input and Generate Response
    btn = gr.Button("Submit")
    clicked = btn.click(query_message, [chatbot, text_box, image_box], chatbot).then(
        llm_response, [chatbot, text_box, image_box], chatbot
    )

# Launch the Interface
if __name__ == "__main__":
    demo.launch()
