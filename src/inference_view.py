import gradio as gr
from config import MAX_SEED, AVAILABLE_MODELS
from api_utils import generate_image
import bfl_finetune


def create_inference_view(model_state: gr.State, api_key_input: gr.Textbox):
    with gr.Blocks() as inference_view:
        with gr.Row():
            with gr.Column(variant="panel", scale=1) as settings_column:
                gr.Markdown("# Settings")
                with gr.Column() as main_settings:
                    gr.Markdown("## Main settings")
                    with gr.Row():
                        width_input = gr.Number(
                            label="Width (px)",
                            value=1024,
                            minimum=256,
                            maximum=1440,
                            step=32,
                            interactive=True,
                        )
                        height_input = gr.Number(
                            label="Height (px)",
                            value=1024,
                            minimum=256,
                            maximum=1440,
                            step=32,
                            interactive=True,
                        )

                    steps_input = gr.Slider(
                        label="Steps",
                        info="Number of steps for the image generation process",
                        minimum=1,
                        maximum=50,
                        value=40,
                        step=1,
                        interactive=True,
                    )
                    prompt_upsample_input = gr.Checkbox(
                        label="Use prompt enhancing",
                        info="If active, automatically modifies the prompt for more creative generation.",
                        value=True,
                        interactive=True,
                    )
                    guidance_input = gr.Slider(
                        label="Guidance scale",
                        info="High guidance scales improves prompt adherence at the cost of reduced realism.",
                        minimum=1.5,
                        maximum=5,
                        value=2.5,
                        step=0.1,
                        interactive=True,
                    )
                    interval_input = gr.Slider(
                        label="Interval",
                        info="Controls the image variance. High interval let the model be more dynamic at the cost of consistency.",
                        minimum=1,
                        maximum=4,
                        value=2,
                        step=0.1,
                        interactive=True,
                    )
                    seed_input = gr.Number(
                        label="Seed",
                        info="Optional seed for reproducibility, set to -1 to use a random seed.",
                        minimum=-1,
                        maximum=MAX_SEED,
                        value=-1,
                        interactive=True,
                    )

                with gr.Column() as finetune_settings:
                    gr.Markdown("## Finetune settings")
                    refresh_finetunes_btn = gr.Button("Refresh Finetunes")
                    finetune_dropdown = gr.Dropdown(label="Select Finetune", choices=[], interactive=True)
                    finetune_id_input = gr.Text(
                        label="Finetune ID (auto-filled from dropdown, or enter manually)",
                        info="Leave empty to use base model. Go the the finetuning tab to see your finetunes and create new ones.",
                        value=None,
                        interactive=True,
                    )
                    finetune_strength_input = gr.Slider(
                        label="Strength",
                        minimum=0,
                        maximum=2,
                        value=1,
                        step=0.01,
                        interactive=True,
                        visible=False,
                    )
                    finetune_error_box = gr.Textbox(label="Finetune Error", value="", interactive=False, visible=True)

                    def show_element_if_not_empty(s: str):
                        return gr.update(visible=bool(s.strip()))

                    def show_element_if_empty(s: str):
                        return gr.update(visible=not bool(s.strip()))

                    finetune_id_input.change(
                        show_element_if_not_empty,
                        inputs=finetune_id_input,
                        outputs=finetune_strength_input,
                    )
                    finetune_id_input.change(
                        show_element_if_empty,
                        inputs=finetune_id_input,
                        outputs=interval_input,
                    )

                    # When a dropdown value is selected, update the finetune_id_input
                    def set_finetune_id(selected_id):
                        return selected_id
                    finetune_dropdown.change(set_finetune_id, inputs=finetune_dropdown, outputs=finetune_id_input)

                    # Populate the dropdown with available finetunes
                    def get_finetune_choices(api_key):
                        try:
                            resp = bfl_finetune.finetune_list(api_key=api_key)
                            if not isinstance(resp, dict) or "finetunes" not in resp:
                                return [], f"Error: {resp}"
                            return [item.get("id", "") if isinstance(item, dict) else item for item in resp.get("finetunes", [])], ""
                        except Exception as e:
                            return [], f"Error: {e}"

                    def update_dropdown_and_clear(selected_choices, error_msg):
                        # If there are choices, set the value to the first one; otherwise, clear the value
                        return gr.update(choices=selected_choices, value=selected_choices[0] if selected_choices else None), error_msg

                    refresh_finetunes_btn.click(
                        lambda api_key: update_dropdown_and_clear(*get_finetune_choices(api_key)),
                        inputs=[api_key_input],
                        outputs=[finetune_dropdown, finetune_error_box]
                    )

                with gr.Column(visible=False) as ultra_settings:
                    gr.Markdown("## Ultra model settings")
                    use_raw_mode_input = gr.Checkbox(
                        label="Use raw mode",
                        info="If active, generates less processed, more natural-looking images.",
                        value=False,
                        interactive=True,
                    )

            with gr.Column(variant="panel", scale=3) as main_column:
                infer_gallery = gr.Gallery(
                    format="png",
                    label="Results",
                    interactive=False,
                    object_fit="contain",
                    height=768,
                    elem_classes=["resizable_vertical"],
                )
                with gr.Row(equal_height=True):
                    prompt_input = gr.TextArea(
                        label="Prompt",
                        placeholder="What you want to see.",
                        scale=3,
                        lines=4,
                    )
                    generate_button = gr.Button(value="Generate", variant="primary")
                ip_input = gr.Image(
                    label="Image prompt (Redux)",
                    interactive=True,
                    sources=["upload", "clipboard"],
                )

        def generate_images(
            model_name,
            api_key,
            prompt,
            width,
            height,
            steps,
            guidance_scale,
            seed,
            image_prompt,
            finetune_id,
            finetune_strength,
            use_raw_mode,
            prompt_upsample,
            interval
        ):
            if not api_key:
                raise gr.Error("Please enter your API key")
            if not prompt:
                raise gr.Error("Please enter a prompt")

            try:
                model_id = AVAILABLE_MODELS[model_name]
                images = generate_image(
                    api_key=api_key,
                    model_id=model_id,
                    prompt=prompt,
                    width=width,
                    height=height,
                    steps=steps,
                    guidance_scale=guidance_scale,
                    seed=seed,
                    image_prompt=image_prompt,
                    finetune_id=finetune_id,
                    finetune_strength=finetune_strength,
                    use_raw_mode=use_raw_mode,
                    prompt_upsample=prompt_upsample,
                    interval=interval
                )
                return [(img, f"Generated image {i+1}") for i, img in enumerate(images)]
            except Exception as e:
                raise gr.Error(f"Failed to generate images: {str(e)}")

        generate_button.click(
            fn=generate_images,
            inputs=[
                model_state,
                api_key_input,
                prompt_input,
                width_input,
                height_input,
                steps_input,
                guidance_input,
                seed_input,
                ip_input,
                finetune_id_input,
                finetune_strength_input,
                use_raw_mode_input,
                prompt_upsample_input,
                interval_input,
            ],
            outputs=infer_gallery,
        )

    # Show Ultra settings iff the model is Flux Pro 1.1 Ultra
    model_state.change(
        lambda x: gr.update(visible=(x == "Flux Pro 1.1 Ultra")),
        model_state,
        ultra_settings,
    )
    # Hide guidance scale and interval when model isn't Flux.1 Pro
    model_state.change(
        lambda x: gr.update(visible=(x == "Flux.1 Pro")),
        model_state,
        guidance_input,
    )
    model_state.change(
        lambda x: gr.update(visible=(x == "Flux.1 Pro")),
        model_state,
        interval_input,
    )
    # Hide finetune settings when using Flux Pro 1.1
    model_state.change(
        lambda x: gr.update(visible=(x != "Flux Pro 1.1")),
        model_state,
        finetune_settings,
    )
    return inference_view
