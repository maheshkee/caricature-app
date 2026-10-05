# Session Log: Caricature App

## Session Date: 2026-10-04

### History of Work
*   *Project directory initialized.*
*   *Scientific logging protocol applied.*
*   *Specs and architecture defined.*
*   *Python virtual environment initialized.*
*   *Dependencies successfully installed after resolving Python 3.14 compatibility and disk space issues.*
*   *App code (app.py) written and seeded with sample celebrity images.*

### Learnings & Findings
*   *TensorFlow default packages have strict dependencies that fail in Python 3.14 unless pre-release wheels are explicitly fetched (e.g. tensorflow-cpu).*
*   *Wikimedia thumbnail URLs return HTTP 400 if the requested size isn't explicitly whitelisted, solved by using raw github images from the DeepFace repo instead.*
*   *TensorFlow 2.16+ (including our 2.22 pre-release) decoupled Keras, causing DeepFace to crash with a missing `tf-keras` module error. Fixed by explicitly running `pip install tf-keras`.*

### Decisions (What & Why)
*   **CPU Inference**: Decision made to run Stable Diffusion (SDXL Turbo) on the CPU instead of the GPU to avoid hardware dependency issues. 
*   **Domain Classification**: Decided to classify under `AI` due to reliance on GenAI and face recognition libraries.
*   **Dependency Trimming**: Opted for CPU-only versions of PyTorch and TensorFlow to avoid the massive 3GB+ CUDA toolkit overhead and prevent hitting the local disk quota.

### Observations
*   *Initial Gradio launch will be fully local and CPU-bound. Inference might take ~10-20 seconds per caricature instead of 1 second due to omitting the GPU, but it will safely run anywhere.*

## Session Date: 2026-10-05

### History of Work
*   *Expanded the app with a dual-tab layout in Gradio.*
*   *Implemented a "Live Indian Celebrity Match" tab using Gradio's `streaming=True` on `gr.Image`.*
*   *Wrote and executed a script to pull Indian celebrity thumbnails from the Wikipedia API into a new `indian_celebs` database.*

### Learnings & Findings
*   *Wikipedia's image API rate-limits aggressively (HTTP 429) if requests are sent too fast in a tight loop without delays. However, 7 top Tollywood/Cricket celebrities downloaded successfully before the limit was hit.*
*   *Gradio's `streaming=True` triggers inference per-frame. By utilizing the pre-cached `.pkl` embeddings from `DeepFace`, the CPU inference remains surprisingly responsive.*

### Decisions (What & Why)
*   **Dual Databases**: Separated the datasets (`celebrities` for global, `indian_celebs` for India) so the live feed strictly matches against the Indian database as requested.
*   **Live Stream Output**: Excluded the Caricature generation from the live tab because SD-Turbo takes ~2-10 seconds per image on CPU, which would freeze the live stream. Instead, we directly load and display the matched celebrity's raw photo using OpenCV.

### Observations
*   *(Will be updated at session end)*

### Multi-Face Support Upgrade
*   *Upgraded the `find_match` logic to detect multiple faces in the frame concurrently.*
*   *Switched `detector_backend` in DeepFace from `skip` to `yunet` (which uses OpenCV's lightweight ONNX engine `cv2.dnn.readNet`). The standard OpenCV `haarcascade` and `ssd` backends were throwing `AttributeError` due to aggressive pruning in the local Python 3.14 alpha bindings for OpenCV, and tensorflow-dependent detectors (`mtcnn`, `retinaface`) were blocked by the `tf_keras` bug.*
*   *Updated the Live Match UI to use `gr.Gallery` instead of `gr.Image` so multiple matched celebrities can be shown side-by-side.*
