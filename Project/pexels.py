from pexelsapi.pexels import Pexels
import random
import requests
# import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO

def search_images(query, api_key):

    query_ids = []

    pexel = Pexels(api_key=api_key)

    for keyword in query:
        search_photos = pexel.search_photos(query=keyword, orientation='landscape', size='500', color='', locale='', page=1, per_page=15)

        photos_metadata = search_photos['photos']
        image_ids = [photo['id'] for photo in photos_metadata]
        
        random_image_id = random.choice(image_ids)
        query_ids.append(random_image_id)

    return query_ids

def query_images(query_ids, api_key):

    images = []

    # Replace 'YOUR_API_KEY' with your actual API key
    headers = {
        "Authorization": api_key
    }

    for id in query_ids:

        # Make the API call to fetch the image
        response = requests.get(f"https://api.pexels.com/v1/photos/{id}", headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            # Get the URL of the image from the API response
            image_url = response.json()["src"]["original"]

            # Fetch the image content
            image_response = requests.get(image_url)

            # Read the image using PIL
            img = Image.open(BytesIO(image_response.content))
            images.append(img)

        else:
            print("Failed to fetch image. Status code:", response.status_code)

    return images
