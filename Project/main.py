import streamlit as st
from summarization import summarize
from pexels import search_images, query_images
from keywords import extract_keywords
from text_to_speech import tts_deepgram
from image_captioning import img_caption
from PIL_Testing import images_to_video
from PIL_Testing import create_subtitle_clips
from PIL_Testing import process_press_release
from image_database import initialize_database, store_image, query_images
from audio_to_sub import transcribe_audio, srt_from_transcription
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from typing_extensions import Concatenate
import PyPDF2
import os
import matplotlib.pyplot as plt
import pysrt
from PIL import Image
import io
from IPython.display import display

######################################################################################
# Load environment variables from .env file 
######################################################################################
load_dotenv()

# Set your Pexels API key
pexels_api = os.getenv("PEXELS_API_KEY")

# Set your Deepgram API key
deepgram_api_key = os.getenv("DEEPGRAM_API_KEY")
######################################################################################
######################################################################################
#
#
#
#
#
#
######################################################################################
# Streamlit
######################################################################################
# Streamlit Main Page
st.title("VidQuill")
st.subheader("Convert Press Releases to short Video")

st.write("VidQuill is a tool that converts press releases to short videos. It uses AI to summarize the press release, extract keywords, search for relevant images, and create a video with subtitles. It also provides an option to convert the text to speech and caption the images. The tool is designed to help businesses and individuals create engaging video content for their press releases. VidQuill is a one-stop solution for all your video creation needs!")

# Streamlit Sidebar Utilities
st.sidebar.title(":green[Toolbar]")
st.sidebar.write("Select the options below to create a video from your press release.")

## Press Release Input
st.sidebar.header(":green[Press Release Input]")
main_placeholder = st.empty()
text = st.sidebar.text_area("Enter the text of the press release here: ")
pdf = st.sidebar.file_uploader("Upload the Press Release in a PDF file")
input_button = st.sidebar.button("Submit Press Release")
st.sidebar.divider()

## Image Captioning and Database Storage
st.sidebar.header(":green[Image Captioning and Database Storage]")
images = st.sidebar.file_uploader("Upload the images to caption and store in database",accept_multiple_files=True, type=['jpg', 'png'])
caption_and_store_image = st.sidebar.button("Caption and Store Images")
st.sidebar.divider()

## Query Database
st.sidebar.header(":green[Query Database]")
query = st.sidebar.text_area("Enter the query to search database of images here: ")
query_database_button = st.sidebar.button("Query Database based on the Caption")
######################################################################################
######################################################################################
#
#
#
#
#
#
######################################################################################
# Pdf input Processing to text
######################################################################################
# passing the pdf to the reader
if pdf:
    pdfreader = PdfReader(pdf)

    # Extracting the text from the pdf
    text = ''
    for i, page in enumerate(pdfreader.pages):
        content = page.extract_text()
        if content:
            text += content
######################################################################################
######################################################################################
#
#
#
#
#
#
######################################################################################
# The following code initializes the database connection and creates a table to store images.
######################################################################################
# Database connection:
conn = initialize_database()

# Custom tag input (Just let it be here dont do anything)
custom_tags = st.text_input("Custom tags input here")

# Caption and store the images button
if caption_and_store_image:
    if images is not None:
        for image in images:
            image = Image.open(image)
            st.image(image, width=400)
            caption= "Something"
            # caption = img_caption(image)
            st.write(caption)
            # custom_tags = st.text_input("Custom tags input here")
            if custom_tags:
                store_image(conn=conn, image=image, tags = custom_tags)
            else:
                store_image(conn=conn, image=image, tags = caption)
######################################################################################
######################################################################################
#
#
#
#
#
#
######################################################################################
# Query Database
######################################################################################
# Query the database for images based on tags/caption
if query_database_button:
    result = query_images(conn=conn,tags=query)

    for row in result:

        image_data = row[0]
        image = Image.open(io.BytesIO(image_data))
        st.image(image)
######################################################################################
######################################################################################
#
#
#
#
#
#
######################################################################################
######################################################################################
# Input Button Activation Section
######################################################################################
######################################################################################
if input_button:

    ##################################################################################
    # Summarization
    ##################################################################################
    generated_summary = summarize(text)
    st.divider()
    st.header("Summary of the Press Release")

    # Display the summary title
    summary_title = generated_summary['Title']
    main_placeholder = st.empty()
    main_placeholder.subheader(summary_title)

    # Display the summary points
    points = generated_summary['Summary']
    summary_points = " ".join(points)
    main_placeholder.write(summary_points)

    title_and_summary = summary_title + ": " + summary_points
    ##################################################################################
    ##################################################################################
    #
    #
    #
    #
    #
    #
    ##################################################################################
    # Keywords Extraction
    ##################################################################################
    keywords = extract_keywords(title_and_summary)
    # st.write(keywords)

    keywords_list = keywords['Keywords']
    st.write(keywords)

    # Query sql database
    for keyword in keywords_list:
        result= query_images(conn=conn,tags=keyword)
        for row in result:

            image_data = row[0]
            image = Image.open(io.BytesIO(image_data))
            st.image(image)
    ##################################################################################
    ##################################################################################
    #
    #
    #
    #
    #
    #
    ##################################################################################
    ##################################################################################
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
    # query_ids = search_images(query=["Moon", "Space", "Stars"], api_key= pexels_api)
    # images = query_images(query_ids=query_ids, api_key=pexels_api)

    # for image in images:
    #     st.image(image, caption='Your Image', use_column_width=True)
    #
    #
    #
    #
    #
    #

    ##################################################################################
    # Video Stitching
    ##################################################################################
    # Stitch images to create a video
    stitched_video_path = images_to_video(images)

    ##################################################################################
    ##################################################################################
    #
    #
    #
    #
    #
    #
    ##################################################################################
    #Text to speech
    ##################################################################################
    st.divider()
    st.subheader("Video Features")
    # Toggle button for voiceover feature
    # voiceover_toggle = st.toggle("Enable VoiceOver")

    # if voiceover_toggle:
    #voice_options
    voice_option_dict = {
        "Asteria (Female)": "asteria",
        "Luna (Female)": "luna",
        "Stella (Female)": "stella",
        "Athena (Female)": "athena",
        "Hera (Female)": "hera",
        "Orion (Male)": "orion",
        "Arcas (Male)": "arcas",
        "Perseus (Male)": "perseus",
        "Angus (Male)": "angus",
        "Orpheus (Male)": "orpheus",
        "Helios (Male)": "helios",
        "Zeus (Male)": "zeus"
    }

    #display the voice options
    voice_opt_display = list(voice_option_dict.keys())

    voice_option = st.selectbox(
        "Select the voice option:", 
        voice_opt_display, 
        index=None,
        placeholder="Select voice option...",
    )

    if voice_option:
        voice_option_value = voice_option_dict[voice_option]
        st.write(f"You selected: {voice_option}")

        tts_deepgram(text, voice_option_value, deepgram_api_key)

        AUDIO_FILE = "./your_output_file.mp3"
        st.header("Generated Voiceover")
        audio_file = open(AUDIO_FILE, 'rb')
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format='audio/mp3')

    AUDIO_FILE = "./your_output_file.mp3"    
    # Transcribe the audio and generate srt file
    dg_response = transcribe_audio(AUDIO_FILE)
    srt_from_transcription(dg_response)
    
# #Image captioning
# img_url = './images.jpg' #Add path to image
# captioned_text = img_caption(img_url)
# st.write(captioned_text)

    # Toggle button for subtitling feature
    subtitling_toggle = st.toggle("Enable Subtitling")


    # Generate srt file if subtitling is enabled
    if subtitling_toggle:
        srt_file = 'subtitling.txt'
        subtitles = pysrt.open(srt_file)
        create_subtitle_clips(subtitles)
        process_press_release(stitched_video_path)
    
