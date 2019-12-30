import re
import os
import nltk  #used in extract insti function
from spacy.matcher import Matcher
from . import constants as cs
from src.util.nlp_tools import nlp, calculate_similarity_with_processing
import numpy as np
from src.util.headers_dict import title2bucket
import string
from src.util.entity_extractor import group_extractor
import pandas as pd
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords



result = string.punctuation
result = result.replace(" ","")
punctuation_list = []
for x in result:
    punctuation_list.append(x)

# initialize matcher with a vocab
matcher = Matcher(nlp.vocab)
matcher2 = Matcher(nlp.vocab)

def extract_email(s, line):
    line = [x["text"] for x in line]
    line = '\n'.join(line)
    email = re.findall("[a-zA-Z0-9]+@(?:[a-zA-Z0-9]+\.{0,})+[a-zA-Z]+", line)            #regex to match email in text
    if email:
        try:
            return email[0].split()[0].strip(';')
        except IndexError:
            return None

def extract_mobile(parts, line):
    line = [x["text"] for x in line]
    line = '\n'.join(line)
    phone = re.findall(re.compile(r'(?:(?:\+?([1-9]|[0-9][0-9]|[0-9][0-9][0-9])\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([0-9][1-9]|[0-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?'), line)
    
    if phone:
        number = ''.join(phone[0])
        if len(number) > 10:
            return '+' + number
        else:
            return number

def extract_name(parts, line):
    line = [x["text"] for x in line]
    line = '\n'.join(line)
    #print(line)
    nlp_text = nlp(line)

    # First name and Last name are always Proper Nouns
    pattern = [{'POS': 'PROPN'}, {'POS': 'PROPN'}]             

    matcher.add('NAME', None, pattern)
    pattern2 = [{'POS': 'PROPN'}, {'POS': 'PROPN'}, {'POS': 'PROPN'}]        #second matcher object : to match names having length 3 instead of 2.
    matcher2.add('NAME', None, pattern2)

    matches = matcher(nlp_text)
    matches2 = matcher2(nlp_text)

    indianNames = open('../util/allNames.txt', 'r').read().lower()
    indianNames = set(indianNames.split())

    for match_id, start, end in matches2:
        span = nlp_text[start:end]
        lst = span.text.split(" ")
        if lst[0].lower in indianNames and lst[1].lower in indianNames and lst[2].lower in indianNames:
            return span.text


    for match_id, start, end in matches:
        span = nlp_text[start:end]
        lst = span.text.split(" ")
        #print(lst[0],lst[1])
        #print(lst[0].lower(),lst[1].lower())
        if lst[0].lower() in indianNames and lst[1].lower() in indianNames:
            return span.text
    

def extract_skills(nlp_text):
    '''
    Helper function to extract skills from spacy nlp text
    :param nlp_text: object of `spacy.tokens.doc.Doc`
    :param noun_chunks: noun chunks extracted from nlp text
    :return: list of skills extracted
    '''
    tokens = [token.text for token in nlp_text if not token.is_stop]
    data = pd.read_csv(os.path.join(os.path.dirname(__file__), 'skills.csv'))
    skills = list(data.columns.values)
    skillset = []
    # check for one-grams
    for token in tokens:
        if token.lower() in skills:
            skillset.append(token)

    # check for bi-grams and tri-grams
    noun_chunks=nlp_text.noun_chunks
    for token in noun_chunks:
        token = token.text.lower().strip()
        if token in skills:
            skillset.append(token)
    return [i.capitalize() for i in set([i.lower() for i in skillset])]

def cleanup(token, lower = True):
    if lower:
       token = token.lower()
    return token.strip()

def extract_education(nlp_text):
    '''
    Helper function to extract education from spacy nlp text
    :param nlp_text: object of `spacy.tokens.doc.Doc`
    :return: tuple of education degree and year if year if found else only returns education degree
    '''
    edu = {}
    # Extract education degree
    for index, text in enumerate(nlp_text):
        for tex in text.split():
            tex = re.sub(r'[?|$|.|!|,]', r'', tex)
            if tex.upper() in cs.EDUCATION and tex not in cs.STOPWORDS:
                edu[tex] = text + nlp_text[index + 1]

    # Extract year
    education = []
    for key in edu.keys():
        year = re.search(re.compile(cs.YEAR), edu[key])
        if year:
            education.append((key, ''.join(year.group(0))))
        else:
            education.append(key)
    return education

def extract_experience(resume_text):
    '''
    Helper function to extract experience from resume text
    :param resume_text: Plain resume text
    :return: list of experience
    '''
    wordnet_lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))

    # word tokenization
    word_tokens = nltk.word_tokenize(resume_text)

    # remove stop words and lemmatize
    filtered_sentence = [w for w in word_tokens if not w in stop_words and wordnet_lemmatizer.lemmatize(w) not in stop_words]
    sent = nltk.pos_tag(filtered_sentence)

    # parse regex
    cp = nltk.RegexpParser('P: {<NNP>+}')
    cs = cp.parse(sent)

    # for i in cs.subtrees(filter=lambda x: x.label() == 'P'):
    #     print(i)

    test = []

    for vp in list(cs.subtrees(filter=lambda x: x.label()=='P')):
        test.append(" ".join([i[0] for i in vp.leaves() if len(vp.leaves()) >= 2]))

    # Search the word 'experience' in the chunk and then print out the text after it
    x = [x[x.lower().index('experience') + 10:] for i, x in enumerate(test) if x and 'experience' in x.lower()]
    return x

def extract_insti(lines):
    insti = []
    indianColleges = open('../util/indianColleges.txt','r').read().lower()
    indianColleges = set(indianColleges.split())
    lst_of_groups = group_extractor(lines)
    for l in lst_of_groups:
        a = l.split(" ")
        for x in a:
            if x.lower() in indianColleges:
                insti.append(l)
                break

    return insti



# get the label/title of a possible header line using spacy similarity with possible header lines
# line belong to that bucket or title which have maximum similarity with possible headers
def get_label(line):
    global_max_bucket=0
    global_max_bucket_name="other"

    for title in title2bucket:
        score=calculate_similarity_with_processing(title2bucket[title]['doc'], line['doc'])
        if global_max_bucket<score:
            global_max_bucket=score
            global_max_bucket_name=title2bucket[title]['bucket']
    return global_max_bucket_name, global_max_bucket


# get lines which are headers and the bucket they belong to
def extract_headers(texts):
    max_words_in_header=3   # assumption a header will have only these many words
    thresh_prob1=0.09       # thresh hold probability to say a line is a header
    similarity_thresh_prob1=0.7    # thresh hold similarity to say line belongs to a bucket

    # iterate over each line
    for index, line in enumerate(texts):
        prob=1
        line['isHeader'] = False

        # check if there is any word which doesn't exist in spacy model vocabulary
        for token in line['doc']:
            token_id = nlp.vocab.strings[token.text]
            if token_id not in nlp.vocab:
                prob=prob*0.1

        # modify prob using number of tokens after stripping punctuations in line
        num_words=len(line['tokens'])
        # header can't have 0 words
        if num_words==0:
            continue
        elif num_words>max_words_in_header:
            prob=prob*np.exp(-2*(num_words-max_words_in_header))

        # a header doesn't end with a full stop
        if line['doc'][-1].text=='.':
            continue

        # get words stating with alphabetic character
        words=re.findall("[A-Za-z][^ ]*", line['text'])
        # a header will have either all upper case characters or words starting with upper case character
        if words:
            first_word=True
            for word in words:
                if word.islower():
                    if first_word:
                        prob=0
                        first_word=False
                    else:
                        prob=prob*0.2
                elif word.isupper():
                    continue
                if word[0].isupper():
                    prob=prob*0.8
        else:
            continue

        # check similarity only if probabilty of being header line > thresh hold
        if prob>thresh_prob1:
                label, similarity=get_label(line)
                # print("--line ", line['text'])
                # print("--num_words ", num_words, "--prob", prob, "--label ", label, " --similarity : ", similarity)
                if similarity>similarity_thresh_prob1:
                   # print("--------------TITLE---------------------")
                   line['isHeader']=True
                   line['bucket']=label
                   line['similarity']=similarity





# classify the lines into buckets using headers obtained from extract headers
# logic is to classify the line according to last seen header
def extract_buckets(data):
    last_label = 'Personal Details'
    for line in data:
        if line.get('isHeader', None):
            last_label=line['bucket']
        else:
            line['bucket']=last_label














