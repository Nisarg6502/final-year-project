# from keybert import KeyBERT
from langchain.chains import LLMChain
from langchain import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain_community.chat_models import ChatAnyscale
import re

def extract_keywords(output_summary):
    llm = ChatAnyscale(model_name="meta-llama/Llama-2-7b-chat-hf", temperature=0.0)

    # Create a new prompt template for keyword extraction
    keyword_prompt = PromptTemplate(
        input_variables=["output_summary"],
        template='''Extract keywords from the following summary and return the output in this format only as keywords:["keyword1","keyword2",...]. Summary:  {output_summary}''',
    )

    # Create a new LLM chain with the keyword extraction prompt
    keyword_chain = LLMChain(llm=llm, prompt=keyword_prompt)

    # Run the keyword chain on the summary
    keywords = keyword_chain.run(output_summary)

    # Extract the keywords using regular expression
    keywords_match = re.search(r'Keywords:\s*\[([^]]*)\]', keywords)

    if keywords_match:
        keywords_str = keywords_match.group(1)  # Extract the string within square brackets
        keywords_list = [keyword.strip().strip('"') for keyword in keywords_str.split(',')]
        # print(keywords_list)
    else:
        print("Keywords not found.")

    return keywords_list