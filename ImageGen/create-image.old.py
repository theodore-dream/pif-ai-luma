import requests
import os

stable_diffusion_api_key = os.environ["stable_diffusion_api_key"]
print("API key is " + stable_diffusion_api_key)

# Define the request body with the necessary parameters
request_body = {
    "key": stable_diffusion_api_key,
    "prompt": "A beautiful mountain landscape",
    "model_id": "midjourney",  # Replace with a valid model ID
    "samples": 1,
    "negative_prompt": "",
    "width": 1024,
    "height": 768,
    "prompt_strength": 1.0,
    "num_inference_steps": 50,
    "guidance_scale": 1,
    "seed": "",
    "enhance_prompt": "yes",
    "webhook": "",
    "upscale": "no",
    "track_id": ""
}

# Send a POST request to the 'dreambooth' API endpoint
url_dreambooth = 'https://stablediffusionapi.com/api/v3/dreambooth'
headers = {"Content-Type": "application/json"}
response_dreambooth = requests.post(url_dreambooth, headers=headers, json=request_body)

# Print the response from the 'dreambooth' endpoint
print("Response from 'dreambooth' endpoint:")
print(response_dreambooth.text)
