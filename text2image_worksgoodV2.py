import openai
from PIL import Image
import os
import sys
import configparser
import requests
import datetime

# Initialize the configuration
config = configparser.ConfigParser()
configpath = "C:\\Users\\natha\\src\\venv\\OpenAI_API\\examples\\image\config.ini"
config.read(configpath)
api_key = config.get("OpenAI", "api_key")

image_sizes = ['256x256', '512x512', '1024x1024']

if config['ImageGeneration']['image_resolution'] not in image_sizes:
    print(f'\n NOTE: Config did not include valid resolution.  Exiting!')
    print(f'Acceptable: {repr(image_sizes)}')
    sys.exit(0)

# Initialize OpenAI API
openai.api_key = api_key

def text_to_image(myprompt, num_images, image_size="1024x1024"):
    try:
        response = openai.Image.create(
            prompt=myprompt,
            n=1,
            size=image_size)
        if response:
            print(f'getting an image url...')
            image_url = response['data'][0]['url']
            return image_url
        else:
            print("No image assets found in the response.")
            return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

def save_image_from_url(url, outputdir):
    try:
        current_datetime = datetime.datetime.now()
        formatted_dt = current_datetime.strftime("%Y%m%d%H%M%S")
        filepath = f'{outputdir}imagegen_{formatted_dt}.png'
        print(f'Saving to {filepath}')
        response = requests.get(url)
        if response.status_code == 200:
            with open(filepath, "wb") as image_file:
                image_file.write(response.content)
            print(f"Image saved to {filepath}")
            return True
        else:
            print(f"Failed to download the image. Status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"An error occurred while saving the image: {str(e)}")
        return False

def main(config):
    # Get image generation parameters from the configuration
    model = config.get("ImageGeneration", "model")
    num_images = int(config.get("ImageGeneration", "num_images"))
    image_format = config.get("ImageGeneration", "image_format")
    image_resolution = config.get("ImageGeneration", "image_resolution")
    output_dir = config.get("ImageGeneration", "output_dir")
    
    while True:
        print("\nText-to-Image Generation Menu:")
        print("1. Generate Image from Text")
        print("2. Exit")
        
        choice = input("Select an option: ")
        
        if choice == "1":
            prompt = input("Enter a textual description: ")
            print(f'prompt={prompt}')
            image_url = text_to_image(prompt, num_images, image_resolution)
            #dir_path = "C:\\Users\\natha\\src\\venv\\OpenAI_API\\examples\\output\\"
            if image_url:
                print('we have an image to save...')
                save_image_from_url(image_url, output_dir)
        elif choice == "2":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main(config)