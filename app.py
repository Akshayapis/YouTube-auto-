import os
import requests
from google import genai
from google.genai import types

# 1. Environment variables se secrets aur YAML se prompt/URLs uthana
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

base_prompt = os.environ.get(
    "VIDEO_PROMPT", 
    "Pahale in dono img ko deko ek ek krke dono ko to jante hoge instagram youTube pr 1 no pr hey aur dono k video kise kise hote hey bahut tip ki hote hey ok. To es dono mine koi ek slict karo jis ka es time pr video baht play ho ok air fir 40s ka txt tip krdo ok bhai best ho ek dam best Story ok and 8k quality air iise img mi hey vise carictar ok bhai bahut kucch ho ok bahut log ho ok alg alg tum ko pata hoga best txt promt do"
)

img1 = os.environ.get("IMAGE_URL_1", "")
img2 = os.environ.get("IMAGE_URL_2", "")

# 2. Gemini API Setup (Google AI Studio API Key)
client = genai.Client(api_key=GEMINI_API_KEY)

def get_gemini_selection():
    prompt_text = f"""
    You are an expert AI viral video director for Instagram and YouTube. 
    Here are the two reference image URLs:
    - Image 1 URL: {img1}
    - Image 2 URL: {img2}
    
    User Instructions / Prompt: {base_prompt}
    
    Task for you:
    1. Analyze both images based on current Instagram and YouTube viral trends.
    2. Choose ONE image (either 1 or 2) which is currently trending higher and gives better performance.
    3. Write a powerful, highly detailed 40 to 50 seconds video generation prompt in English (optimized for AI video models) that captures this exact style, same character, 8K ultra-realistic quality, multiple people/crowd, and viral aesthetic.
    
    Output format strictly in this exact format:
    CHOSEN_IMAGE: [1 or 2]
    STORY: [Your detailed 40-50s high-quality video generation prompt matching the selected image style]
    """
    
    response = client.models.generate_content(
        model='gemini-2.5-flash', # Updated working model name
        contents=prompt_text,
    )
    
    text = response.text
    chosen = "1"
    story = ""
    
    for line in text.split('\n'):
        if "CHOSEN_IMAGE:" in line:
            chosen = "2" if "2" in line else "1"
        if "STORY:" in line:
            story = line.replace("STORY:", "").strip()
            
    if not story:
        story = text 
            
    return chosen, story

chosen_img_num, final_story = get_gemini_selection()
selected_image_url = img2 if chosen_img_num == "2" else img1

enhanced_prompt = f"{final_story}, 8k resolution, photorealistic, cinematic lighting, maintaining exact character and style from reference image: {selected_image_url}"

print(f"=== GEMINI RESULT ===")
print(f"Selected Image Number by Gemini: {chosen_img_num}")
print(f"Selected Image URL: {selected_image_url}")
print(f"Generated 40-50s Video Prompt: {enhanced_prompt}")
