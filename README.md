# 🎭 AI Doppelgänger & Caricature Hub

A fun, dual-tab AI application built with Gradio, DeepFace, and Stable Diffusion! 

1. **Live Indian Celebrity Match**: Stream your webcam and see instantly which Indian actor/cricketer you or your friends resemble the most. Supports scanning multiple faces in the same frame!
2. **Caricature Generator**: Snap a photo and let Stable Diffusion (SD-Turbo) generate a funny cartoon caricature of the celebrity you look like.

## 🚀 Quick Setup

This project provides an automated setup script that creates a virtual environment and installs the required CPU-optimized packages safely (saving you ~10GB of disk space by avoiding CUDA binaries).

### macOS / Linux
Open your terminal inside this folder and run:
```bash
chmod +x setup.sh
./setup.sh
```

### Windows
Open your terminal (PowerShell/Command Prompt) inside this folder and run:
```bat
python -m venv venv
venv\Scripts\activate
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements.txt
```

## 🎮 Running the App
Once installed, simply activate your environment and run the app!

**macOS / Linux:**
```bash
source venv/bin/activate
python app.py
```

**Windows:**
```bat
venv\Scripts\activate
python app.py
```

Then click the `http://127.0.0.1:7860` link that appears in your terminal to open the UI in your browser!

### First Time Setup Notes
- The first time you run `app.py`, it will download the **Stable Diffusion Turbo** weights (~2GB) and **OpenCV Face Detection** weights from Hugging Face and GitHub. 
- Please make sure you have at least **3GB of free disk space** for these one-time downloads!

## 🧠 Technical Architecture & Workarounds
- **TensorFlow Keras Workaround**: TensorFlow 2.22 decoupled `tf-keras`, causing standard imports of `DeepFace` to crash. This project natively mocks `tf-keras` inside `app.py` before `DeepFace` is imported, completely fixing the backend!
- **Multiple Faces**: We use the `yunet` ONNX detector in OpenCV which correctly identifies multiple faces simultaneously without crashing on limited Linux/CPU environments.
- **SD-Turbo CPU Optimization**: SDXL was too massive (~13GB). We switched to `stabilityai/sd-turbo` using `variant="fp16"` which only downloads a tiny 2GB file but is cast efficiently for CPU inference.
