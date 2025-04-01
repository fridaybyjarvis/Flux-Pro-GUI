import gradio as gr
from inference_view import create_inference_view
from finetuning_view import create_finetuning_view


with gr.Blocks() as demo:
    gr.Markdown("# Flux Pro GUI")
    # TODO: API key input and model selection menu
    with gr.Tabs():
        with gr.Tab(label="Inference"):
            create_inference_view()
        with gr.Tab(label="Finetuning"):
            create_finetuning_view()


if __name__ == "__main__":
    demo.launch(inbrowser=True)
