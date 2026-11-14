import os
import requests
from google import genai
from google.genai import types

# 1. Environment variables se secrets uthana
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
base_prompt = os.environ.get("VIDEO_PROMPT", "Cinematic drone shot of mountains")
img1 = os.environ.get("IMAGE_URL_1", "")
img2 = os.environ.get("IMAGE_URL_2", "")

# 2. Gemini API Setup (Latest Google GenAI SDK)
client = genai.Client(api_key=GEMINI_API_KEY)

def get_gemini_selection():
    prompt_text = f"""
    You are an expert AI video director. I have two reference image styles:
    Image 1 URL: {img1}
    Image 2 URL: {img2}
    
    Base Prompt Concept: {base_prompt}
    
    Task: 
    1. Write a rich, detailed 40-second video cinematic story based on the base prompt.
    2. Choose which image style (1 or 2) fits better.
    Output format strictly: 
    CHOSEN_IMAGE: [1 or 2]
    STORY: [Your detailed prompt description matching the visual style]
    """
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt_text,
    )
    
    text = response.text
    # Simple parsing
    chosen = "1"
    story = base_prompt
    for line in text.split('\n'):
        if "CHOSEN_IMAGE:" in line:
            chosen = "2" if "2" in line else "1"
        if "STORY:" in line:
            story = line.replace("STORY:", "").strip()
            
    return chosen, story

chosen_img_num, final_story = get_gemini_selection()
selected_image_url = img2 if chosen_img_num == "2" else img1
enhanced_prompt = f"{final_story}, matching the exact visual style and quality of reference image: {selected_image_url}"

print(f"Selected Image: {chosen_img_num}")
print(f"Enhanced Prompt: {enhanced_prompt}")

# 3. Video Generation Model Setup (Hugging Face Diffusers - LTX-Video / CogVideoX for High Quality)
def generate_ai_video(prompt):
    import torch
    from diffusers import LTXPipeline
    from diffusers.utils import export_to_video

    print("Loading High-Quality Video Model (LTX-Video)...")
    # T4/P100 GPU ke liye optimized high-quality open-source video model
    pipe = LTXPipeline.from_pretrained(
        "Lightricks/LTX-Video", 
        torch_dtype=torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16
    ).to("cuda")
    
    # Memory optimization
    pipe.enable_attention_slicing()

    print("Generating 40-second equivalent premium video frames...")
    # High quality settings
    video_frames = pipe(
        prompt=prompt,
        num_inference_steps=50,
        height=512,
        width=768,
        num_frames=120  # Smooth high frame count
    ).frames

    output_path = "output_video.mp4"
    export_to_video(video_frames, output_path, fps=24)
    print(f"Video saved successfully at {output_path}")
    return output_path

# Video generate karo
# video_file = generate_ai_video(enhanced_prompt)
