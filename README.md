# Caricature App

## Requirements
*   **User Interface:** A web app accessible via local browser and remotely via smartphone camera.
*   **Core Functionality:** Capture user photo, identify closest celebrity match from a local database, and generate a caricature.
*   **Execution Environment:** Must execute inference locally utilizing the **CPU**.

## Specifications
*   **Language/Environment:** Python 3.x with isolated `venv`.
*   **Frontend Framework:** Gradio
*   **Face Recognition:** `deepface` library (VGG-Face model).
*   **Image Generation:** `diffusers` library utilizing `stabilityai/sdxl-turbo` (standard CPU precision).

## Architecture Flow
1.  **Data Layer:** Local directory (`celebrities/`) containing named images acting as the vector database.
2.  **UI Layer:** Gradio captures image array and passes to backend.
3.  **Processing Layer (Backend):**
    *   *Match Module:* Extracts embeddings, compares against Data Layer, determines celebrity name.
    *   *Generative Module:* Constructs prompt and passes to SDXL pipeline for CPU inference.
4.  **Output Layer:** Returns match percentage and generated image to UI.
