import gradio as gr
import sys, unittest.mock as mock
m = mock.MagicMock()
m.__version__ = '2.15.0'
sys.modules['tf_keras'] = m
from deepface import DeepFace
from diffusers import AutoPipelineForText2Image
import torch
import os
import cv2
import numpy as np

# --- 1. Load the Image Generation Model onto the CPU ---
print("Loading Image Generation Model (SD Turbo) on CPU to save space...")
pipe = AutoPipelineForText2Image.from_pretrained(
    "stabilityai/sd-turbo",
    variant="fp16"
)

# --- 2. Define the Face Matching Logic ---
def find_match(user_image, db_path):
    if user_image is None:
        return []
        
    if not os.path.exists(db_path) or len(os.listdir(db_path)) == 0:
        return []

    try:
        # Use yunet detector to find multiple faces (opencv onnx backend)
        dfs = DeepFace.find(
            img_path=user_image, 
            db_path=db_path, 
            model_name="SFace", 
            detector_backend="yunet",
            enforce_detection=False,
            threshold=100.0,
            silent=True
        )
        
        results = []
        for df in dfs:
            if len(df) > 0:
                best_match_row = df.iloc[0]
                file_path = best_match_row['identity']
                distance = best_match_row['distance']
                match_percentage = max(0, min(100, int((1 - (distance / 0.6)) * 100)))
                filename = os.path.basename(file_path)
                celeb_name = os.path.splitext(filename)[0].replace("_", " ")
                results.append((celeb_name, match_percentage, file_path))
                
        return results

    except Exception as e:
        print(f"Error in find_match: {e}")
        return []

# --- 3. Gradio Tab Functions ---
def process_caricature(user_image):
    matches = find_match(user_image, "celebrities")
    
    if not matches:
        return "Could not find a clear face or match. Try again!", None
        
    # Just take the first face found for caricature
    celeb_name, match_percentage, file_path = matches[0]
        
    result_text = f"You look {match_percentage}% like {celeb_name}!"
    
    prompt = f"A highly exaggerated, funny cartoon caricature illustration of {celeb_name}, large head, digital art, colorful, highly detailed"
    print(f"Generating caricature for: {celeb_name} on CPU...")
    generated_image = pipe(prompt=prompt, num_inference_steps=2, guidance_scale=0.0).images[0]
    
    return result_text, generated_image

def process_live_face(frame):
    if frame is None:
        return "Waiting for video...", []
        
    # For the live version, we use the indian_celebs folder!
    matches = find_match(frame, "indian_celebs")
    
    if not matches:
        return "Scanning... No face found.", []
        
    result_texts = []
    result_images = []
    
    for i, (celeb_name, match_percentage, file_path) in enumerate(matches):
        result_texts.append(f"🔥 Face {i+1}: {match_percentage}% like **{celeb_name}**!")
        celeb_img = cv2.imread(file_path)
        if celeb_img is not None:
            celeb_img = cv2.cvtColor(celeb_img, cv2.COLOR_BGR2RGB)
            result_images.append((celeb_img, celeb_name))
            
    return "\n\n".join(result_texts), result_images

# --- 4. Build the Web Interface with Gradio ---
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🎭 AI Doppelgänger Hub")
    gr.Markdown("Find your celebrity match! Choose between live real-time matching with Indian stars, or static caricature generation.")
    
    with gr.Tabs():
        # TAB 1: Live Indian Celebrity Match
        with gr.Tab("Live Indian Celebrity Match"):
            with gr.Row():
                with gr.Column():
                    gr.Markdown("### 📸 Live Webcam")
                    # setting streaming=True triggers the function every time the webcam frame updates
                    live_image = gr.Image(sources=["webcam"], streaming=True, type="numpy", label="Live Video")
                with gr.Column():
                    gr.Markdown("### ⭐ Your Matches")
                    live_celeb_name = gr.Markdown(label="Match Results")
                    live_celeb_img = gr.Gallery(label="Matched Celebrities", columns=2)

            live_image.stream(
                fn=process_live_face,
                inputs=[live_image],
                outputs=[live_celeb_name, live_celeb_img]
            )
            
        # TAB 2: Caricature Generator (Original)
        with gr.Tab("Caricature Generator (Global Celebs)"):
            with gr.Row():
                with gr.Column():
                    input_image = gr.Image(sources=["webcam"], type="numpy", label="Take your photo")
                    submit_btn = gr.Button("Find My Match & Generate Caricature", variant="primary")
                    
                with gr.Column():
                    output_text = gr.Markdown(label="Match Results")
                    output_image = gr.Image(label="Celebrity Caricature")

            submit_btn.click(
                fn=process_caricature,
                inputs=[input_image],
                outputs=[output_text, output_image]
            )

if __name__ == "__main__":
    demo.launch(share=True)
