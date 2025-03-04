import time
import gradio as gr
import requests
from client import respond
from huggingface_hub.errors import HfHubHTTPError


"""
API Huggingface some time return 503 error, so we need to retry multiple times
"""


def robust_respond(*args, **kwargs):
    max_retries = 10
    wait_time = 2

    for attempt in range(max_retries):
        try:
            yield from respond(*args, **kwargs)
            return
        except HfHubHTTPError as e:
            if "503" in str(e):
                print(
                    f"Attempt {attempt+1}: Hugging Face API is down. Retrying in {wait_time}s..."
                )
                time.sleep(wait_time)
                wait_time *= 2
            else:
                yield f"Error: {str(e)}"
                return

    yield "Server busy right now !"


chatbot = gr.Chatbot(height=600)

demo = gr.ChatInterface(
    robust_respond,
    additional_inputs=[
        gr.Textbox(value="", label="System message"),
        gr.Slider(minimum=1, maximum=2048, value=512, step=1, label="Max new tokens"),
        gr.Slider(minimum=0.1, maximum=4.0, value=0.7, step=0.1, label="Temperature"),
        gr.Slider(
            minimum=0.1,
            maximum=1.0,
            value=0.95,
            step=0.05,
            label="Top-P",
        ),
    ],
    fill_height=True,
    chatbot=chatbot,
    theme="Nymbo/Nymbo_Theme",
)
