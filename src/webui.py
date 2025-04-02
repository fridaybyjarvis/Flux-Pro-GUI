import gradio as gr
from inference_view import create_inference_view
from finetuning_view import create_finetuning_view

from config import AVAILABLE_MODELS

css = """
.resizable_vertical {
  resize: vertical;
  overflow: auto !important;
}
"""


with gr.Blocks(css=css) as demo:
    gr.Markdown("# Flux Pro GUI")
    with gr.Row():
        model_input = gr.Dropdown(
            label="Model",
            info="Please note that finetuning is not available for Flux 1.1 Pro",
            choices=AVAILABLE_MODELS.keys(),
            interactive=True,
        )
        api_key_input = gr.Textbox(
            label="API key",
            info="Get your BFL API key at https://docs.bfl.ml/",
            interactive=True,
            max_lines=1,
            type="password",
            scale=4,
        )
    with gr.Tabs():
        with gr.Tab(label="Inference"):
            create_inference_view()
        with gr.Tab(label="Finetuning"):
            create_finetuning_view()


if __name__ == "__main__":
    demo.launch(inbrowser=True)
