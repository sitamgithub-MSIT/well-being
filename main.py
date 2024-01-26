import PIL.Image
import gradio as gr
import base64
import time
import os
import google.generativeai as genai

# Set Google API key
os.environ["GOOGLE_API_KEY"] = "YOUR KEY"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# Create the Model
txt_model = genai.GenerativeModel("gemini-pro")
vis_model = genai.GenerativeModel("gemini-pro-vision")

sample_prompt = """You are a medical practitioner and an expert in analyzing medical-related images working for a very reputed hospital. You will be provided with images and you need to identify the anomalies, any disease or health issues. You need to generate the result in a detailed manner. Write all the findings, next steps, recommendation, etc. You only need to respond if the image is related to a human body and health issues. You must have to answer but also write a disclaimer saying that "Consult with a Doctor before making any decisions."

Remember, if certain aspects are not clear from the image, it's okay to state 'Unable to determine based on the provided image.'

Now analyze the image and answer the above questions in the same structured manner defined above."""


# Image to Base 64 Converter
def image_to_base64(image_path):
    with open(image_path, "rb") as img:
        encoded_string = base64.b64encode(img.read())
    return encoded_string.decode("utf-8")


# Function that takes User Inputs and displays it on ChatUI
def query_message(history, txt, img):
    if not img:
        history += [(txt, None)]
        return history
    base64 = image_to_base64(img)
    data_url = f"data:image/jpeg;base64,{base64}"
    history += [(f"{txt} ![]({data_url})", None)]
    return history


# Function that takes User Inputs, generates Response and displays on Chat UI
def llm_response(history, text, img):
    health_keywords = [
        "health",
        "disease",
        "anomaly",
        "medical",
        "findings",
        "recommendation",
        "wellness",
        "fitness",
        "nutrition",
        "exercise",
        "diet",
        "weight loss",
        "mental health",
        "physical health",
        "healthy lifestyle",
        "preventive care",
        "symptoms",
        "treatment",
        "medicine",
        "vaccination",
        "immunization",
        "stress",
        "sleep",
        "hygiene",
        "well-being",
        "public health",
        "healthcare",
        "doctor",
        "hospital",
        "prescription",
        "pharmacy",
        "alternative medicine",
        "holistic health",
        "chronic illness",
        "acute illness",
        "allergies",
        "asthma",
        "diabetes",
        "hypertension",
        "cardiovascular health",
        "respiratory health",
        "digestive health",
        "orthopedics",
        "mental disorders",
        "cognitive health",
        "aging",
        "pediatrics",
        "women's health",
        "men's health",
        "reproductive health",
        "pregnancy",
        "childbirth",
        "aging gracefully",
        "brain",
        "heart",
        "lungs",
        "liver",
        "kidneys",
        "kidney",
        "stomach",
        "intestines",
        "pancreas",
        "spleen",
        "gallbladder",
        "bladder",
        "skin",
        "eyes",
        "ears",
        "nose",
        "mouth",
        "tongue",
        "throat",
        "esophagus",
        "muscles",
        "bones",
        "joints",
    ]

    if not img:
        if any(keyword in text.lower() for keyword in health_keywords):
            response = txt_model.generate_content(text)
            history += [(None, response.text)]
        else:
            history += [(None, "I can only respond to health-related questions.")]
    else:
        img = PIL.Image.open(img)
        if any(keyword in text.lower() for keyword in health_keywords):
            response = vis_model.generate_content([text, img])
            history += [(None, response.text)]
        else:
            history += [
                (
                    None,
                    "I can only respond to health-related questions based on images.",
                )
            ]

    return history


# Interface Code
with gr.Blocks() as app:
    with gr.Row():
        image_box = gr.Image(type="filepath")

        chatbot = gr.Chatbot(scale=2, height=750)
    text_box = gr.Textbox(
        placeholder="Enter text and press enter, or upload an image",
        container=False,
    )

    btn = gr.Button("Submit")
    clicked = btn.click(query_message, [chatbot, text_box, image_box], chatbot).then(
        llm_response, [chatbot, text_box, image_box], chatbot
    )
app.queue()
app.launch(share=True)
