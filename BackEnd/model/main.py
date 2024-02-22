import streamlit as st
from summarization import load_model, summarize
from keywords import extract_keywords

st.title("Convert Press Releases to short Video")
st.sidebar.title("Submit your Press Release!")

model, tokenizer = load_model()
if model and tokenizer:
    st.write("model loaded")

main_placeholder = st.empty()

text = st.sidebar.text_area("Enter the text of the press release here: ")

pdf = st.sidebar.file_uploader("Upload the Press Release in a PDF file")


input_button = st.sidebar.button("Submit Press Release")

if input_button:
    generated_summary = summarize(model, tokenizer, text)
    keywords = extract_keywords(text)
    main_placeholder.write(generated_summary)
    st.write(keywords)