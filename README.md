# Flux Pro GUI
A simple GUI to call the Black Forest Labs API more easily to use the Flux.1 Pro, Flux1.1 Pro and the Flux1.1 Pro Ultra models. Allows for inference and finetuning.

## Installation
> Before you install the Flux Pro GUI, please install all the requirements:
> - [Git](https://git-scm.com/)
> - [Python](https://www.python.org/downloads/) (tested with version 3.12.9)
> - [Anaconda](https://www.anaconda.com/download) (you can use `venv` instead)

Start by cloning the repo and moving into the cloned directory.
```bash
git clone https://github.com/brayevalerien/Flux-Pro-GUI
cd Flux-Pro-GUI
```

Then create and activate an Anaconda environment, before installing the required libraries.
```bash
conda create -n flux-pro-gui -y
conda activate flux-pro-gui
pip install -r requirements.txt
```

<!-- TODO: finish writing down the installation process -->

## Features
- Inference with Flux.1 Pro, Flux Pro 1.1, Flux Pro 1.1 Ultra, and Flux1 Pro Finetune models
- Finetuning: upload your dataset, train, list, check status, and delete finetunes
- Inference with your own finetuned models (select 'Flux1 Pro Finetune' and choose a finetune ID)
- Robust error handling and clear user feedback for API/network issues
- Easy API key entry and management

## Usage
For the moment, you can start the GUI by activating your conda environment and starting `src/webui.py`:
```bash
conda activate flux-pro-gui
python src/webui.py
```
It should automatically open a new tab in your default browser. If not, manually go to http://127.0.0.1:7860.

### Entering your BFL API key
- Enter your BFL API key in the field at the top of the app before using any features.
- You can get your API key at [https://docs.bfl.ml/](https://docs.bfl.ml/)

### Using Finetuning
1. Go to the **Finetuning** tab.
2. Upload your dataset (ZIP), set parameters, and click **Train** to submit a finetune job.
3. Use **List My Finetunes** to see your finetunes. Select one to check status or delete.
4. Wait until the status is **Ready** before using your finetune for inference.

### Using Inference with Finetunes
1. Go to the **Inference** tab.
2. Select **Flux1 Pro Finetune** from the model dropdown.
3. Click **Refresh Finetunes** and select your finetune from the dropdown.
4. Enter your prompt and other parameters, then click **Generate**.

### Troubleshooting
- If you see error messages, check the error boxes for details (e.g., invalid API key, network issues, or no finetunes available).
- Make sure your API key is correct and your finetune is **Ready** before running inference.

## Resources
- [BFL API reference](https://api.us1.bfl.ai/scalar)