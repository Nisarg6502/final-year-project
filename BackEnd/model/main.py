import streamlit as st
from summarization import load_model, summarize
from keywords import extract_keywords
import fitz
import os

def extract_text_from_pdf(pdf):
    """Extracts text from a PDF file using the latest PyMuPDF library."""

    try:
        doc = fitz.open(pdf) 
        text = "" 
        for page in doc: 
            text+=page.get_text() 
        return text

    except FileNotFoundError as e:
        print(f"Error: PDF file not found at '{pdf}'.")

def save_uploadedfile(uploadedfile):
     with open(uploadedfile.name,"wb") as f:
         f.write(uploadedfile.getbuffer())
     return st.success("Saved File:{} to tempDir".format(uploadedfile.name))

st.title("Convert Press Releases to short Video")
st.sidebar.title("Submit your Press Release!")

model, tokenizer = load_model()
if model and tokenizer:
    st.write("model loaded")

main_placeholder = st.empty()
next_placeholder = st.empty()

text = st.sidebar.text_area("Enter the text of the press release here: ")

pdf = st.sidebar.file_uploader("Upload the Press Release in a PDF file", type=['pdf'])


input_button = st.sidebar.button("Submit Press Release")

if input_button:
    
    if pdf is not None:
        save_uploadedfile(pdf)
        st.success("Saved File")

        pdf_path = pdf.name  # Replace with the actual path to your PDF
        text = extract_text_from_pdf(pdf_path)
        st.success("Text extracted successfully!")
        # text = pdf.read()
        main_placeholder.write(text)
    
    generated_summary = summarize(model, tokenizer, text)
    keywords = extract_keywords(text)
    next_placeholder.write(generated_summary)
    st.write(keywords)