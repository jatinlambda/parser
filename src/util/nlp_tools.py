import spacy
# model to be used throughout project
nlp = spacy.load('en_core_web_md')

# preprocess text data
# remove punctuations, pronouns and return lemmaized list of tokens
def process_main_text1(text):
    doc = nlp(text.lower())
    result = []
    for token in doc:
        if token.is_punct:
            continue
        if token.lemma_ == '-PRON-':
            continue
        result.append(token.lemma_)
    return result, doc

# preprocess text data
# remove punctuations and return lemmaized list of tokens
def process_main_text0(text):
    doc = nlp(text.lower())
    result = []
    for token in doc:
        if token.is_punct:
            continue
        result.append(token.text)
    return result, doc

nlp_process_text_foo=process_main_text1

# calculate similarity of 2 preprocessed data lines using spacy similarity
# takes nlp objects return float similarity
def calculate_similarity_with_processing(title, line):
    for token in line:
        token_id=nlp.vocab.strings[token.text]
        if token_id not in nlp.vocab:
            return 0
    return title.similarity(line)

