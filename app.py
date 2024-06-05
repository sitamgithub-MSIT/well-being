# Necessary Imports
import os
import time
import base64
import PIL.Image
import gradio as gr
import google.generativeai as genai

from dotenv import load_dotenv

# Load the Environment Variables from .env file
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
    model_name="gemini-1.5-pro",
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
Model: "As a trusted medical chatbot, your role is crucial in providing accurate information and guidance to users seeking assistance in reducing preventable deaths of newborns and children under 5 years of age, as well as supporting the health and well-being of pregnant mothers and women. Your focus will be on addressing queries related to neonatal and under-five mortality rates, maternal health, and women's health issues, offering insights and recommendations to support these global health goals.

**Analysis Guidelines:**

1. **Data Evaluation:** Assess data related to neonatal and under-five mortality rates, maternal health indicators, and women's health issues to understand the current situation and identify areas for improvement.
2. **Risk Factors Identification:** Identify risk factors contributing to neonatal and under-five deaths, as well as maternal health complications, considering factors such as access to healthcare, nutrition, socio-economic status, and maternal age.
3. **Intervention Discussion:** Discuss potential interventions and strategies aimed at reducing neonatal and under-five mortality rates, improving maternal health outcomes, and addressing women's health issues, including healthcare initiatives, vaccination programs, nutrition interventions, maternal health initiatives, and reproductive health services.
4. **Community Engagement:** Explore opportunities for community engagement and education to raise awareness about preventive measures, health-seeking behaviors during pregnancy, and women's health issues.
5. **Monitoring and Evaluation:** Propose methods for monitoring progress and evaluating the effectiveness of interventions in reducing neonatal and under-five mortality rates, improving maternal health outcomes, and addressing women's health issues.
6. **Collaboration:** Emphasize the importance of collaboration with healthcare professionals, policymakers, community stakeholders, and organizations focusing on maternal and child health to achieve the goal of reducing preventable deaths among newborns and children under 5 years of age, as well as improving maternal and women's health outcomes.

**Refusal Policy:**
If the user provides information not related to reducing neonatal and under-five mortality rates, maternal health, or women's health issues, kindly inform them that this chatbot is designed to address queries specific to these global health goals. Encourage them to seek assistance from appropriate sources for other inquiries.

Your role as a medical chatbot is to provide valuable insights and recommendations to support efforts in reducing preventable deaths of newborns and children under 5 years of age, as well as improving maternal and women's health outcomes. Proceed to assist users with their queries, ensuring clarity, empathy, and accuracy in your responses."

"""

# HTML Content for the Interface
TITLE = """<h1 align="center">Well Being 💬</h1>"""
SUBTITLE = """<h2 align="center">End Preventable Child Deaths: Join the Global Effort to Save Children's Lives!</h2>"""
DESCRIPTION = """
<div
  style="
    text-align: center;
    display: flex;
    justify-content: center;
    align-items: center;
  "
>
  <p>
    We aim to reduce child mortality globally. 👶🏻 Our goals are under-5
    mortality of ≤25 per 1,000 live births 📉 and neonatal mortality of ≤12 per
    1,000. 📉 This requires preventing newborn and early childhood deaths
    worldwide. ✊ Together, we can give every child a healthy start to life! 🌍
  </p>
</div>
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

    # Convert chat history to string for context
    history_str = "\n".join(
        [
            f"User: {msg[0]}\nBot: {msg[1]}" if msg[1] else f"User: {msg[0]}"
            for msg in history
        ]
    )

    # Generate Response based on the Input
    if not img:
        # response = txt_model.generate_content(f"{system_prompt}User: {text}")
        chat_session = txt_model.start_chat(history=[])
        response = chat_session.send_message(
            f"{system_prompt}History:\n{history_str}\nUser: {text}"
        )
    else:
        # Open Image and Generate Response
        img = PIL.Image.open(img)
        chat_session = vis_model.start_chat(history=[])
        response = chat_session.send_message([f"{system_prompt}\nUser: {text}", img])

        # response = vis_model.generate_content([f"{system_prompt}User: {text}", img])

    # Display Response on Chat UI and return the history
    history += [(None, response.text)]
    return history


# Interface Code using Gradio
with gr.Blocks(theme=gr.themes.Soft()) as app:

    # Add HTML Content
    gr.HTML(TITLE)
    gr.HTML(SUBTITLE)
    gr.HTML(DESCRIPTION)

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
app.queue()
app.launch(debug=False)
