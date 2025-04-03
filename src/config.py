# Available models with their BFL API ID
# To get the finetuned version, append "-finetuned". Flux Pro 1.1 cannot be finetuned.
AVAILABLE_MODELS = {
    "Flux.1 Pro": "flux-pro",
    "Flux Pro 1.1": "flux-pro-1.1",
    "Flux Pro 1.1 Ultra": "flux-pro-1.1-ultra",
}
# Auto-captioning modes for the finetuning endpoint
CAPTIONING_MODES = {
    "General (full details)": "general",
    "Character": "character",
    "Style": "style",
    "Product": "product",
}
FINETUNE_TYPE = {
    "LoRA": "lora",
    "Full": "full",
}
LORA_RANKS = [16, 32]
PRIORITY = {
    "Quality": "quality",
    "Speed": "speed",
    "High resolution only": "high_res_only",
}

MAX_SEED = 2**64 - 1
