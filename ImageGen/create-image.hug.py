import requests
import os
from huggingface_hub.inference_api import InferenceApi

from diffusers import DiffusionPipeline

repo_id = "PublicPrompts/All-In-One-Pixel-Model5"
pipe = DiffusionPipeline.from_pretrained(repo_id)


#setup the hugging face api token 
api_token = os.environ["hugging_face_api_key"]
print("API key is " + api_token)

import requests

def query(payload, model_id, api_token):
    headers = {"Authorization": f"Bearer {api_token}"}
    API_URL = f"https://api-inference.huggingface.co/models/{model_id}"
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

def main():
    # Set the model ID to the one you want to use
    model_id = "PublicPrompts/All-In-One-Pixel-Model"

    # Define your prompt
    prompt = "Create a pixel art of a cat"

    # Construct the payload
    payload = {
        "inputs": {
            "prompt": prompt,
            "max_tokens": 50
        }
    }

    # Call the query function
    response = query(payload, model_id, api_token)

    # Print the result
    print(response)

if __name__ == "__main__":
    main()

from huggingface_hub.inference_api import InferenceApi

def main():
    # Replace YOUR_API_TOKEN with your actual Hugging Face API token
    api_token = "YOUR_API_TOKEN"

    # Set the model ID to the one you want to use
    model_id = "PublicPrompts/All-In-One-Pixel-Model"

    # Define your prompt
    prompt = "Create a pixel art of a cat"

    # Create an instance of the InferenceApi
    inference = InferenceApi(repo_id=model_id, token=api_token)

    # Call the InferenceApi with your inputs
    response = inference(inputs=prompt)

    # Print the result
    print(response)

if __name__ == "__main__":
    main()
