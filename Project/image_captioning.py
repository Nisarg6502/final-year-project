# Salesforce/blip-image-captioning-large
import requests
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import time

# Record the starting time
# start_time = time.time()
def img_caption(img_url):
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large").to("cuda")

    raw_image = Image.open(img_url).convert('RGB')

    # unconditional image captioning
    inputs = processor(raw_image, return_tensors="pt").to("cuda")

    out = model.generate(**inputs)
    processed_text = processor.decode(out[0], skip_special_tokens=True)
    return processed_text

    # Record the ending time
    # end_time = time.time()

    # Calculate the elapsed time
    # elapsed_time = end_time - start_time

    # print("Time taken:", elapsed_time, "seconds"

# image = img_caption("image1.jpg")
# print(image)