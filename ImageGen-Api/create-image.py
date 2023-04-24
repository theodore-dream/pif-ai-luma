import requests
import os

stable_diffusion_api_key = os.environ["stable_diffusion_api_key"]
print("API key is " + stable_diffusion_api_key)

# Define the request body with the necessary parameters
request_body = {
    "key": stable_diffusion_api_key,
    "prompt": "ultra realistic close up portrait ((beautiful pale cyberpunk female with heavy black eyeliner)), blue eyes, shaved side haircut, hyper detail, cinematic lighting, magic neon, dark red city, Canon EOS R3, nikon, f/1.4, ISO 200, 1/160s, 8K, RAW, unedited, symmetrical balance, in-frame, 8K",
    "negative_prompt": "((out of frame)), ((extra fingers)), mutated hands, ((poorly drawn hands)), ((poorly drawn face)), (((mutation))), (((deformed))), (((tiling))), ((naked)), ((tile)), ((fleshpile)), ((ugly)), (((abstract))), blurry, ((bad anatomy)), ((bad proportions)), ((extra limbs)), cloned face, (((skinny))), glitchy, ((extra breasts)), ((double torso)), ((extra arms)), ((extra hands)), ((mangled fingers)), ((missing breasts)), (missing lips), ((ugly face)), ((fat)), ((extra legs)), anime",
    "model_id": "midjourney",  # Replace with a valid model ID
    "samples": 1,
    "negative_prompt": "",
    "width": 512,
    "height": 512,
    "prompt_strength": 1.0,
    "num_inference_steps": 20,
    "guidance_scale": 7.5,
    "safety_checker": "no",
    "enhance_prompt": "yes",
    "upscale": "no",
    "webhook": None,
    "seed": None,
    "track_id": None
}

# Send a POST request to the 'text2img' API endpoint. Alt: dreambooth
url_dreambooth = 'https://stablediffusionapi.com/api/v3/text2img'
headers = {"Content-Type": "application/json"}
response_dreambooth = requests.post(url_dreambooth, headers=headers, json=request_body)

# Print the response from the 'dreambooth' endpoint
print("Response from 'dreambooth' endpoint:")
print(response_dreambooth.text)
print("Script complete")