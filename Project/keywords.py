# from keybert import KeyBERT
# from langchain.chains import LLMChain
# from langchain import PromptTemplate
# from langchain.chains.summarize import load_summarize_chain
# from langchain_community.chat_models import ChatAnyscale
# import re

from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.chat_models import ChatOpenAI
from langchain_community.chat_models import ChatAnyscale

def extract_keywords(output_summary):
    
    llm = ChatOpenAI(model_name ="gpt-3.5-turbo", temperature=0,streaming=True)
    # llm = ChatAnyscale(model_name="meta-llama/Llama-2-70b-chat-hf", temperature=0.0)
    # Define your desired data structure.
    class Keywords(BaseModel):
        Keywords: list[str] = Field(description="A list of keywords")

    json_parser = JsonOutputParser(pydantic_object=Keywords)

    prompt = PromptTemplate(
        template="""
            You are an expert keyword extractor who answers only in json style format nothing else.
            Your job is to extract the top 10 keywords from the news article summary in the provided format only, as a list of string keywords.
            Do not output anything else other than the json format.
            {format_instructions}
            News Article Summary:\n{entire_text}
            """,
        input_variables=["entire_text"],
        partial_variables={"format_instructions": json_parser.get_format_instructions()},
    )

    chain = prompt | llm | json_parser

    output_keywords = chain.invoke({"entire_text": output_summary})
    # print(output_keywords)
    return output_keywords