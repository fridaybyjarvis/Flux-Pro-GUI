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

## Usage
For the moment, you can start the GUI by activating your conda environment and starting `src/webui.py`:
```bash
conda activate flux-pro-gui
python src/webui.py
```

It should automatically open a new tab in your default browser. If not, manually go to http://127.0.0.1:7860.

<!-- TODO: go into more details or adjust instructions when the project is done -->

## Resources
- [BFL API reference](https://api.us1.bfl.ai/scalar)