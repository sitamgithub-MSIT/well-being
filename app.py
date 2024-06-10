# Necessary Imports
import gradio as gr

# Import the necessary functions from the src folder
from src.chat import query_message
from src.llm_response import llm_response


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
