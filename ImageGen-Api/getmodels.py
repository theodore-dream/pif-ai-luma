import requests
import os

stable_diffusion_api_key = os.environ["stable_diffusion_api_key"]
print("API key is " + stable_diffusion_api_key)

# Print information about the API endpoints
print("The following URL points to all models: https://stablediffusionapi.com/api/v3/finetune_list")

# Define the request body with the API key
request_body = {
    "key": stable_diffusion_api_key
}

# Send a POST request to the 'finetune_list' API endpoint
url_finetune = 'https://stablediffusionapi.com/api/v3/finetune_list'
headers = {'Content-Type': 'application/json'}
response_finetune = requests.post(url_finetune, headers=headers, json=request_body)

# Get the JSON data from the response
response_data = response_finetune.json()

print("Response from 'finetune_list' endpoint:")
print(response_data)

# Check if the response status is 'success'
if response_data['status'] == 'success':
    # Unpack the model list data
    model_list = response_data['data']
    
    # Print the model list data
    print("\nModel list data:")
    for model in model_list:
        print(model)
else:
    print("Error: Unable to get the model list.")


# Send a POST request to the 'dreambooth' API endpoint
#url_dreambooth = 'https://stablediffusionapi.com/api/v3/dreambooth'
#response_dreambooth = requests.post(url_dreambooth, headers=headers, json=request_body)
#print("Response from 'dreambooth' endpoint:")
#print(response_dreambooth.text)

# Send a POST request to the 'dreambooth-image-to-image' API endpoint
#url_image_to_image = 'https://stablediffusionapi.com/docs/features/v4/dreambooth-image-to-image'
#response_image_to_image = requests.post(url_image_to_image, headers=headers, json=request_body)
#print("Response from 'dreambooth-image-to-image' endpoint:")
#print(response_image_to_image.text)
