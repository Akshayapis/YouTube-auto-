import os
import requests

print("--- Step 1: Fetching Prompt from OpenRouter ---")
OPENROUTER_API_KEY = "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"
base_prompt = "Pahale in dono img ko deko ek ek krke dono ko to jante hoge instagram youTube pr 1 no pr hey aur dono k video kise kise hote hey bahut tip ki hote hey ok. To es dono mine koi ek slict karo jis ka es time pr video baht play ho ok air fir 40s ka txt tip krdo ok bhai best ho ek dam best Story ok and 8k quality air iise img mi hey vise carictar ok bhai bahut kucch ho ok bahut log ho ok alg alg tum ko pata hoga best txt promt do"
img1 = "https://i.ibb.co/PvvnF4Ss/1794655006382.png"
img2 = "https://i.ibb.co/jvj0BxYP/1794654866543.png"

url = "https://openrouter.ai/api/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json"
}

prompt_text = f"""
You are an expert AI viral video director for Instagram and YouTube. 
Image 1: {img1}
Image 2: {img2}
User Prompt: {base_prompt}
Choose ONE image (1 or 2) and write a powerful detailed 40s video prompt matching its style.
Format strictly:
CHOSEN_IMAGE: [1 or 2]
STORY: [Your prompt]
"""

payload = {
    "model": "google/gemini-2.5-flash",
    "messages": [{"role": "user", "content": prompt_text}],
    "max_tokens": 1500
}

response = requests.post(url, headers=headers, json=payload)
res_data = response.json()
text = res_data["choices"][0]["message"]["content"]

chosen = "1"
story = base_prompt
for line in text.split('\n'):
    if "CHOSEN_IMAGE:" in line:
        chosen = "2" if "2" in line else "1"
    if "STORY:" in line:
        story = line.replace("STORY:", "").strip()

selected_img = img2 if chosen == "2" else img1
final_prompt = f"{story}, 8k resolution, photorealistic, cinematic lighting, style from {selected_img}"
print(f"Final Prompt: {final_prompt}")

print("--- Step 2: Generating Video on Kaggle GPU ---")
import torch
from diffusers import DiffusionPipeline
from diffusers.utils import export_to_video

pipe = DiffusionPipeline.from_pretrained(
    "ali-vilab/text-to-video-ms-1.7b", 
    torch_dtype=torch.float16
).to("cuda")
pipe.enable_attention_slicing()

video_frames = pipe(final_prompt, num_inference_steps=30, height=320, width=576, num_frames=48).frames

output_file = "output_video.mp4"
export_to_video(video_frames, output_file, fps=16)
print("Video generated successfully on Kaggle GPU!")

print("--- Step 3: Pushing Video back to GitHub ---")
os.system("git config --global user.name 'Kaggle AI Bot'")
os.system("git config --global user.email 'bot@kaggle.com'")
os.system(f"git clone https://{os.environ.get('GH_PAT')}@github.com/{os.environ.get('REPO_NAME')}.git repo_dir")
os.system(f"cp {output_file} repo_dir/")
os.system("cd repo_dir && git add output_video.mp4 && git commit -m 'Auto-generated video from Kaggle GPU [skip ci]' && git push")
print("Video successfully pushed back to GitHub repository!")
