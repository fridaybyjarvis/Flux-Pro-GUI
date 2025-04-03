import gradio as gr

from config import CAPTIONING_MODES, FINETUNE_TYPE, LORA_RANKS, PRIORITY


def create_finetuning_view(model_state: gr.State):
    with gr.Row() as finetuning_view:
        with gr.Column(variant="panel", scale=1) as your_finetunes_column:
            gr.Markdown("# Your finetunes")
            with gr.Column() as trained_finetunes_column:
                gr.Markdown("## Available")
                gr.Markdown("The following models are ready for inference.")
                gr.Markdown("**Not implemented yet.**")
                gr.Markdown("## Processing")
                gr.Markdown(
                    "The following models are currently in training, please wait before using them."
                )
                gr.Markdown("**Not implemented yet.**")
        with gr.Column(variant="panel", scale=2) as setting_column:
            gr.Markdown("# Train a new finetune")
            gr.Markdown("## 1. Upload your dataset")
            gr.File(label="Dataset", file_count="directory", interactive=True)
            gr.Markdown("## 2. Set para-data")
            with gr.Row(equal_height=True):
                trigger_word_input = gr.Text(
                    label="Trigger word",
                    info="Once trained, use this word in the caption to trigger the finetune (optional).",
                    scale=1,
                )
                comment_input = gr.Text(
                    label="Comment",
                    info="Comment or name of the fine-tuned model, will appear in the model info.",
                    scale=2,
                )
            gr.Markdown("## 3. Tweak training settings")
            with gr.Accordion(label="Optimization settings", open=True):
                type_input = gr.Radio(
                    label="Finetune type",
                    info="Type of finetuning, LoRA is a standard Low Rank Adapter while Full trains the full model with a post hoc LoRA extraction.",
                    choices=FINETUNE_TYPE,
                    value=list(FINETUNE_TYPE.keys())[0],
                    interactive=True,
                )
                rank_input = gr.Radio(
                    label="LoRA rank",
                    info="Rank of the finetuned model. If the full model is finetuned, this will be the rank of the extracted LoRA model.",
                    choices=LORA_RANKS,
                    value=LORA_RANKS[0],
                    interactive=True,
                )
                iteration_input = gr.Slider(
                    label="Iterations",
                    info="Number of iterations for fine-tuning.",
                    minimum=100,
                    maximum=1000,
                    value=300,
                    interactive=True,
                )
                lr_input = gr.Slider(
                    label="Learning rate",
                    info="Learning rate for fine-tuning.",
                    minimum=1e-6,
                    maximum=5e-3,
                    value=1e-4,
                    interactive=True,
                )
            with gr.Accordion(label="Captioning setting", open=True):
                use_captioning_input = gr.Checkbox(
                    label="Use auto-captioning",
                    info="Wether to enable captioning during finetuning.",
                    value=False,
                )
                captioning_mode_input = gr.Radio(
                    label="Captioning mode",
                    choices=CAPTIONING_MODES,
                    value=list(CAPTIONING_MODES.keys())[0],
                    interactive=True,
                    visible=False,
                )
                use_captioning_input.change(
                    lambda x: gr.update(visible=x),
                    use_captioning_input,
                    captioning_mode_input,
                )
            with gr.Accordion(label="Other settings", open=True):
                priority_input = gr.Radio(
                    label="Priority",
                    info="Priority of the job. Speed will prioritize iteration speed over quality while Quality will priorize quality over speed. Noone nows w*f High res only is.",
                    choices=PRIORITY,
                    value=list(PRIORITY.keys())[0],
                    interactive=True,
                )
            train_button = gr.Button(value="Train", variant="primary")
    return finetuning_view
