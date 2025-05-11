import gradio as gr
import bfl_finetune
from config import CAPTIONING_MODES, FINETUNE_TYPE, LORA_RANKS, PRIORITY


def create_finetuning_view(model_state: gr.State, api_key_input: gr.Textbox):
    with gr.Row() as finetuning_view:
        with gr.Column(variant="panel", scale=1):
            gr.Markdown("# Your finetunes")
            list_button = gr.Button("List My Finetunes")
            finetune_list_output = gr.Dataframe(headers=["ID", "Comment", "Status"], interactive=False)
            selected_finetune = gr.Textbox(label="Selected Finetune ID", interactive=True)
            status_button = gr.Button("Check Status/Details")
            status_output = gr.Textbox(label="Finetune Status/Details", interactive=False)
            delete_button = gr.Button("Delete Selected Finetune", variant="stop")
            delete_output = gr.Textbox(label="Delete Status", interactive=False)

        with gr.Column(variant="panel", scale=2):
            gr.Markdown("# Train a new finetune")
            dataset = gr.File(label="Dataset (ZIP)", file_count="single", interactive=True)
            trigger_word_input = gr.Text(label="Trigger word", info="Once trained, use this word in the caption to trigger the finetune (optional).", scale=1)
            comment_input = gr.Text(label="Comment", info="Comment or name of the fine-tuned model, will appear in the model info.", scale=2)
            type_input = gr.Radio(label="Finetune type", info="Type of finetuning.", choices=FINETUNE_TYPE, value=list(FINETUNE_TYPE.keys())[0], interactive=True)
            rank_input = gr.Radio(label="LoRA rank", info="Rank of the finetuned model.", choices=LORA_RANKS, value=LORA_RANKS[0], interactive=True)
            iteration_input = gr.Slider(label="Iterations", info="Number of iterations for fine-tuning.", minimum=100, maximum=1000, value=300, interactive=True)
            lr_input = gr.Slider(label="Learning rate", info="Learning rate for fine-tuning.", minimum=1e-6, maximum=5e-3, value=1e-4, interactive=True)
            use_captioning_input = gr.Checkbox(label="Use auto-captioning", info="Whether to enable captioning during finetuning.", value=False)
            priority_input = gr.Radio(label="Priority", info="Priority of the job.", choices=PRIORITY, value=list(PRIORITY.keys())[0], interactive=True)
            train_button = gr.Button(value="Train", variant="primary")
            train_status_box = gr.Textbox(label="Training Status", value="", interactive=False)

    def train_callback(dataset, trigger_word, comment, type_val, rank_val, iterations, lr, use_captioning, priority, api_key):
        if not dataset or not api_key:
            return "Error: Please upload a dataset (ZIP) and provide an API key."
        try:
            # Map UI values to API values
            priority_map = {"Quality": "quality", "Speed": "speed", "High resolution only": "high_res_only"}
            finetune_type_map = {"LoRA": "lora", "Full": "full"}
            priority = priority_map.get(priority, priority)
            type_val = finetune_type_map.get(type_val, type_val)

            zip_path = dataset.name
            resp = bfl_finetune.request_finetuning(zip_path, comment, trigger_word, api_key=api_key, iterations=iterations, learning_rate=lr, captioning=use_captioning, priority=priority, finetune_type=type_val, lora_rank=rank_val)
            finetune_id = resp.get("id", "unknown")
            return f"Finetuning submitted (finetune id: {finetune_id})"
        except Exception as e:
            return f"Error submitting finetuning: {e}"

    def list_finetunes(api_key):
        try:
            resp = bfl_finetune.finetune_list(api_key=api_key)
            if not isinstance(resp, dict) or "finetunes" not in resp:
                # Show the error as a single row
                return [["Error", str(resp), ""]]
            rows = []
            for item in resp.get("finetunes", []):
                if isinstance(item, dict):
                    rows.append([item.get("id", ""), item.get("finetune_comment", ""), item.get("status", "")])
                else:
                    rows.append([item, "", ""])
            return rows
        except Exception as e:
            return [["Error", str(e), ""]]

    def status_finetune(finetune_id, api_key):
        if not finetune_id or not api_key:
            return "Please provide a finetune ID and API key."
        try:
            resp = bfl_finetune.finetune_details(finetune_id, api_key=api_key)
            return str(resp)
        except Exception as e:
            return f"Error: {e}"

    def delete_finetune(finetune_id, api_key):
        if not finetune_id or not api_key:
            return "Please provide a finetune ID and API key."
        try:
            resp = bfl_finetune.finetune_delete(finetune_id, api_key=api_key)
            return str(resp)
        except Exception as e:
            return f"Error: {e}"

    train_button.click(
        fn=train_callback,
        inputs=[dataset, trigger_word_input, comment_input, type_input, rank_input, iteration_input, lr_input, use_captioning_input, priority_input, api_key_input],
        outputs=train_status_box,
        queue=False
    )
    list_button.click(fn=list_finetunes, inputs=[api_key_input], outputs=finetune_list_output)
    status_button.click(fn=status_finetune, inputs=[selected_finetune, api_key_input], outputs=status_output)
    delete_button.click(fn=delete_finetune, inputs=[selected_finetune, api_key_input], outputs=delete_output)

    return finetuning_view
