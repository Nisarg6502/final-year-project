from keybert import KeyBERT

def extract_keywords(doc):
    keybert_model = KeyBERT('distilbert-base-nli-mean-tokens')

    keywords = keybert_model.extract_keywords(doc, top_n=10)

    return keywords