import streamlit as st
# from summarization import load_model, summarize
from summarization import summarize
from pexels import search_images, query_images
from keywords import extract_keywords
from dotenv import load_dotenv
from PyPDF2 import PdfReader
import PyPDF2
import os
import matplotlib.pyplot as plt

# Load environment variables from .env file
load_dotenv()

pexels_api = os.getenv("PEXELS_API_KEY")

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
    generated_summary = summarize(text)
    keywords = extract_keywords(generated_summary)
    main_placeholder.write(generated_summary)
    st.write(keywords)

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
    query_ids = search_images(query=keywords[:3], api_key= pexels_api)
    images = query_images(query_ids=query_ids, api_key=pexels_api)

    for image in images:
        st.image(image, caption='Your Image', use_column_width=True)
