# import pandas as pd 
# import torch
# from transformers import T5ForConditionalGeneration, T5Tokenizer


# def load_model():

#     # Path to the directory containing the unzipped model files
#     model_dir = "fine_tuned_t5_model_on_cnn"

#     # Create model architecture (assuming T5ForConditionalGeneration)
#     model = T5ForConditionalGeneration.from_pretrained(model_dir)

#     # Load the tokenizer from the Hugging Face model hub
#     tokenizer = T5Tokenizer.from_pretrained("t5-small")

#     return model, tokenizer


# def summarize(model, tokenizer, text):

#     # News article
#     sample_news_article = text

#     # Tokenize the preprocessed text
#     tokenized_input = tokenizer(sample_news_article, return_tensors="pt", padding=True, truncation=True)

#     # Move the tokenized input to the CUDA device (if available)
#     device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
#     tokenized_input = {key: val.to(device) for key, val in tokenized_input.items()}

#     # Move the model to the same device as the tokenized input
#     model.to(device)

#     # Pass the tokenized input through the fine-tuned T5 model to generate a summary
#     output = model.generate(input_ids=tokenized_input['input_ids'], 
#                             attention_mask=tokenized_input['attention_mask'], 
#                             max_length=500,  # Specify the maximum length of the summary
#                             num_beams=3,  # Specify the number of beams for beam search
#                             early_stopping=True)  # Enable early stopping to stop generation when all beam hypotheses reach the maximum length

#     # Decode the generated summary from token IDs to text
#     generated_summary = tokenizer.decode(output[0], skip_special_tokens=True)

#     return generated_summary

from langchain.docstore.document import Document
from langchain import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain_community.chat_models import ChatAnyscale


def summarize(text):

    docs = [Document(page_content=text)]

    llm = ChatAnyscale(model_name="meta-llama/Llama-2-7b-chat-hf", temperature=0.0)

    template = '''Write a one line title and provide a concise and short summary in 4-5 points for the following text.
    Text: `{text}`
    '''
    prompt = PromptTemplate(
        input_variables=['text'],
        template=template
    )

    chain = load_summarize_chain(
        llm,
        chain_type='stuff',
        prompt=prompt,
        verbose=False
    )
    output_summary = chain.run(docs)

    return output_summary