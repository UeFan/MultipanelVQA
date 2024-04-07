

import base64
from mimetypes import guess_type

from openai import AzureOpenAI
import os
api_base = os.getenv('API_BASE')
api_key= os.getenv('API_KEY')
deployment_name = os.getenv('DEPLOYMENT_NAME_VISION')
api_version = '2024-03-01-preview' # this might change in the future


client = AzureOpenAI(
    api_key=api_key,  
    api_version=api_version,
    base_url=f"{api_base}/openai/deployments/{deployment_name}"
)




# Function to encode a local image into data URL 
def local_image_to_data_url(image_path):
    # Guess the MIME type of the image based on the file extension
    mime_type, _ = guess_type(image_path)
    if mime_type is None:
        mime_type = 'application/octet-stream'  # Default MIME type if none is found

    # Read and encode the image file
    with open(image_path, "rb") as image_file:
        base64_encoded_data = base64.b64encode(image_file.read()).decode('utf-8')

    # Construct the data URL
    return f"data:{mime_type};base64,{base64_encoded_data}"

def call_model(image_path, prompt):
    # Path to your image
    # image_path = "/data3/yue/DocVQA_task1/images/ffbf0023_4.png"


    
    try:
        response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                # { "role": "system", "content": "You are a helpful assistant." },
                { "role": "user", "content": [  
                    { 
                        "type": "text", 
                        "text": prompt
                    },
                    { 
                        "type": "image_url",
                        "image_url": {
                        "url": local_image_to_data_url(image_path)
                        }
                    }
                ] } 
            ],
            max_tokens=2000
        )
        response = json.loads(response.json() )

        return response['choices'][0]['message']['content']
    except Exception as e:
        print(e)
        # print(response)
        return 'I do not know.'