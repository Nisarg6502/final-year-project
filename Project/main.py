import streamlit as st
# from summarization import load_model, summarize
from summarization import summarize
from pexels import search_images, query_images
from keywords import extract_keywords
from text_to_speech import tts_deepgram
from image_captioning import img_caption
from dotenv import load_dotenv
from PyPDF2 import PdfReader
import PyPDF2
import os
import matplotlib.pyplot as plt
from PIL_Testing import images_to_video

# Load environment variables from .env file
load_dotenv()

pexels_api = os.getenv("PEXELS_API_KEY")

# Set your Deepgram API key
deepgram_api_key = os.getenv("DEEPGRAM_API_KEY")


st.title("Convert Press Releases to short Video")
st.sidebar.title("Submit your Press Release!")

# model, tokenizer = load_model()
# if model and tokenizer:
#     st.write("model loaded")

main_placeholder = st.empty()

text = st.sidebar.text_area("Enter the text of the press release here: ")

pdf = st.sidebar.file_uploader("Upload the Press Release in a PDF file")


# provide the path of  pdf file/files.
# pdfreader = PdfReader('/content/sample_pdf.pdf')

# from typing_extensions import Concatenate
# # read text from pdf
# text = ''
# for i, page in enumerate(pdfreader.pages):
#     content = page.extract_text()
#     if content:
#         text += content

input_button = st.sidebar.button("Submit Press Release")


if input_button:

    # input from text
    # generated_summary = summarize(text)
    # keywords = extract_keywords(generated_summary)
    # main_placeholder.write(generated_summary)
    # st.write(keywords)

    # #Input from pdf
    # if pdf:
    #     pdf_reader = PyPDF2.PdfReader(pdf)
    #     num_pages = len(pdf_reader.pages)

    #     for page_num in range(num_pages):
    #         page = pdf_reader.pages[page_num]
    #         text = page.extract_text()
    #         generated_summary = summarize(text)
    #         keywords = extract_keywords(text)
    #         main_placeholder.write(generated_summary)
    #         st.write(keywords)

    # #Images Pexel
    query_ids = search_images(query=["Moon", "Space", "Stars"], api_key= pexels_api)
    images = query_images(query_ids=query_ids, api_key=pexels_api)

    for image in images:
        st.image(image, caption='Your Image', use_column_width=True)
    
    images_to_video(images,output_dir='Images', video_size=(1920, 1080))

    #Text to speech
    # voice_options
    # voice_option_dict = {
    #     "Asteria (Female)": "asteria",
    #     "Luna (Female)": "luna",
    #     "Stella (Female)": "stella",
    #     "Athena (Female)": "athena",
    #     "Hera (Female)": "hera",
    #     "Orion (Male)": "orion",
    #     "Arcas (Male)": "arcas",
    #     "Perseus (Male)": "perseus",
    #     "Angus (Male)": "angus",
    #     "Orpheus (Male)": "orpheus",
    #     "Helios (Male)": "helios",
    #     "Zeus (Male)": "zeus"
    # }

    #display the voice options
    # voice_opt_display = list(voice_option_dict.keys())

    # voice_option = st.selectbox(
    #     "Select the voice option:", 
    #     voice_opt_display, 
    #     placeholder="Select voice option...",
    # )

    # if voice_option:
    #     voice_option_value = voice_option_dict[voice_option]
    #     st.write(f"You selected: {voice_option}")

    #     # voice_option = "zeus"
    #     tts_deepgram(text, voice_option_value, deepgram_api_key)

    # #Image captioning
    # img_url = './images.jpg' #Add path to image
    # captioned_text = img_caption(img_url)
    # st.write(captioned_text)
    
