import re
import os
# import nltk  #used in extract insti function
from spacy.matcher import Matcher
from . import constants as cs
from spacy import displacy
# from src.util.tokenizer_utils import word_tokenize
import spacy
import numpy as np
from src.util.headers_dict import bucket2title, title2bucket, line2feature
from src.util.other_util import overlap_rects
import string
from src.util.entity_extractor import group_extractor
import pandas as pd
# from nltk.stem import WordNetLemmatizer
# from nltk.corpus import stopwords



result = string.punctuation
result = result.replace(" ","")
punctuation_list = []
for x in result:
    punctuation_list.append(x)
# load pre-trained model
# nlp = spacy.load('en_core_web_md')
nlp = spacy.load('en_core_web_md')
# initialize matcher with a vocab
matcher = Matcher(nlp.vocab)
matcher2 = Matcher(nlp.vocab)

def extract_email(s, line):
    email = re.findall("[a-zA-Z0-9]+@(?:[a-zA-Z0-9]+\.{0,})+[a-zA-Z]+", line)
    if email:
        try:
            return email[0].split()[0].strip(';')
        except IndexError:
            return None


def extract_sex(parts, line):
    sex_found = False
    sex = None
    for w in parts:
        if 'sex' in w:
            sex_found = True
            continue
        if sex_found and ':' not in w:
            if w == 'male':
                sex = 'male'
            else:
                sex = 'female'
            break
    return sex


def extract_education(parts, line):
    found = False
    education = None
    for w in parts:
        if 'education' in w:
            found = True
            continue
        if found and ':' not in w:
            education = w
            break
    return education


def extract_mobile(parts, line):
    phone = re.findall(re.compile(r'(?:(?:\+?([1-9]|[0-9][0-9]|[0-9][0-9][0-9])\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([0-9][1-9]|[0-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?'), line)
    
    if phone:
        number = ''.join(phone[0])
        if len(number) > 10:
            return '+' + number
        else:
            return number


def extract_experience(parts, line):
    found = False
    result = None
    for w in parts:
        if w.find('experience') != -1:
            found = True
            continue
        if found and ':' not in w:
            result = w
            break
    return result


def extract_expertise(parts, line):
    length = 4
    line = line.lower()
    index = line.find('know')
    if index == -1:
        length = 2
        index = line.find('familiar')
    if index == -1:
        length = 2
        index = line.find('use')
    if index == -1:
        length = 2
        index = line.find('master')
    if index == -1:
        length = 4
        index = line.find('understand')
    if index == -1:
        length = 4
        index = line.find('develop')

    result = None
    if index == -1:
        return None
    else:
        result = line[index + length:].replace(':', '').strip()
        if result == '':
            return None
    return result


def extract_ethnicity(parts, line):
    race_found = False
    race = None
    for w in parts:
        if w.find('race') != -1:
            race_found = True
            continue
        if race_found and w.find(':') == -1:
            race = w
            break
    return race


def extract_name(parts, line):
    print(line)
    nlp_text = nlp(line)

    # First name and Last name are always Proper Nouns
    pattern = [{'POS': 'PROPN'}, {'POS': 'PROPN'}]

    matcher.add('NAME', None, pattern)
    pattern2 = [{'POS': 'PROPN'}, {'POS': 'PROPN'}, {'POS': 'PROPN'}]
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


    



# def extract_duration(personal_info_line):
# 	nlp = spacy.load("en_core_web_sm")
# 	doc = nlp(personal_info_line)
# 	for ent in doc.ents:
# 		if ent.label_ is "DATE":
# 			return ent.text
#
# def extract_objective(parts, line):
#     found = False
#     result = None
#     for w in parts:
#         if w.find('objective') != -1:
#             found = True
#             continue
#         if found and ':' not in w:
#             result = w
#             break
#     return result

# def extract_insti(lines):
#
#     #text is assumed to be sentences after sentence tokenisation of text.
#     lines = [nltk.word_tokenize(el) for el in lines]
#     lines = [nltk.pos_tag(el) for el in lines]
#
#     indianColleges = open('indianColleges.txt','r').read().lower()
#     indianColleges = set(indianColleges.split())
#     indianDegrees = open('indianDegrees.txt','r').read().lower()
#     indianDegrees = set(indianDegrees.split())
#     print(indianDegrees)
#     #instiregex = r'INSTI: {<DT.>?<NNP.*>+<IN.*>?<NNP.*>+}'
#     instiregex = r'INSTI: {<JJ.>?<NN.>?<IN.>?<DT.>?<NNP.*>+<IN.>?<NNP.*>+}'
#     chunkParser = nltk.RegexpParser(instiregex)
#
#     insti = []
#     degrees = []
#     for tagged_tokens in lines:
# 		print(tagged_tokens)
# 		chunked_tokens = chunkParser.parse(tagged_tokens)
# 		for subtree in chunked_tokens.subtrees():
# 			#print(subtree)
# 			if subtree.label() == 'INSTI':
# 				for ind,leaf in enumerate(subtree.leaves()):
# 					#print(ind,leaf)
# 					if leaf[0].lower() in indianColleges and 'NNP' in leaf[1]:
# 					#	print(leaf)
# 						hit = " ".join([el[0] for el in tagged_tokens])
# 						insti.append(hit)
# 			else:
# 				for ind,leaf in enumerate(subtree.leaves()):
# 					if leaf[0].lower() in indianDegrees:
# 						#print(leaf[0].lower())
# 						new_hit = " ".join([el[0] for el in tagged_tokens])
# 						degrees.append(new_hit)
#     return insti,degrees
#
#     """
#     insti = []
#     indianColleges = open('indianColleges.txt','r').read().lower()
#     indianColleges = set(indianColleges.split())
#     lst_of_groups = group_extractor(lines)
#     for l in lst_of_groups:
#         a = l.split(" ")
#         for x in a:
#             if(x in indianColleges):
#                 insti.append(l)
#                 break;
#
#     return insti
#     """
#     # insti = []
#     # indianColleges = open('file.csv','r').read.lower()
#     # indianColleges = list(indianColleges.split(",,,,\n"))
#     #
#     # for college in indianColleges:
#     #     if(college[1:-1] in lines.lower()):
#     #         insti.append(college)
#
#     return insti

# def extract_degree(lines):
#     indianDegrees = open('../util/indianDegrees.txt', 'r').read().lower()
#     indianDegrees = list(indianDegrees.split())
#     degree = []
#     for line in lines:
#         for punct in punctuation_list:
#             line_without_punct = line.replace(punct," ")
#
#         words = line_without_punct.lower().split(" ")
#         for x in words:
#            # print(x)
#             if(x in indianDegrees):
#                 degree.append(x)
#
#     return degree
# def extract_skills(nlp_text, noun_chunks):
#     '''
#     Helper function to extract skills from spacy nlp text
#     :param nlp_text: object of `spacy.tokens.doc.Doc`
#     :param noun_chunks: noun chunks extracted from nlp text
#     :return: list of skills extracted
#     '''
#     tokens = [token.text for token in nlp_text if not token.is_stop]
#     data = pd.read_csv(os.path.join(os.path.dirname(__file__), 'skills.csv'))
#     skills = list(data.columns.values)
#     skillset = []
#     # check for one-grams
#     for token in tokens:
#         if token.lower() in skills:
#             skillset.append(token)
#
#     # check for bi-grams and tri-grams
#     for token in noun_chunks:
#         token = token.text.lower().strip()
#         if token in skills:
#             skillset.append(token)
#     return [i.capitalize() for i in set([i.lower() for i in skillset])]
#
# def cleanup(token, lower = True):
#     if lower:
#        token = token.lower()
#     return token.strip()

# def extract_education(nlp_text):
#     '''
#     Helper function to extract education from spacy nlp text
#     :param nlp_text: object of `spacy.tokens.doc.Doc`
#     :return: tuple of education degree and year if year if found else only returns education degree
#     '''
#     edu = {}
#     # Extract education degree
#     for index, text in enumerate(nlp_text):
#         for tex in text.split():
#             tex = re.sub(r'[?|$|.|!|,]', r'', tex)
#             if tex.upper() in cs.EDUCATION and tex not in cs.STOPWORDS:
#                 edu[tex] = text + nlp_text[index + 1]
#
#     # Extract year
#     education = []
#     for key in edu.keys():
#         year = re.search(re.compile(cs.YEAR), edu[key])
#         if year:
#             education.append((key, ''.join(year.group(0))))
#         else:
#             education.append(key)
#     return education

# def extract_experience(resume_text):
#     '''
#     Helper function to extract experience from resume text
#     :param resume_text: Plain resume text
#     :return: list of experience
#     '''
#     wordnet_lemmatizer = WordNetLemmatizer()
#     stop_words = set(stopwords.words('english'))
#
#     # word tokenization
#     word_tokens = nltk.word_tokenize(resume_text)
#
#     # remove stop words and lemmatize
#     filtered_sentence = [w for w in word_tokens if not w in stop_words and wordnet_lemmatizer.lemmatize(w) not in stop_words]
#     sent = nltk.pos_tag(filtered_sentence)
#
#     # parse regex
#     cp = nltk.RegexpParser('P: {<NNP>+}')
#     cs = cp.parse(sent)
#
#     # for i in cs.subtrees(filter=lambda x: x.label() == 'P'):
#     #     print(i)
#
#     test = []
#
#     for vp in list(cs.subtrees(filter=lambda x: x.label()=='P')):
#         test.append(" ".join([i[0] for i in vp.leaves() if len(vp.leaves()) >= 2]))
#
#     # Search the word 'experience' in the chunk and then print out the text after it
#     x = [x[x.lower().index('experience') + 10:] for i, x in enumerate(test) if x and 'experience' in x.lower()]
#     return x

# def extract_insti(lines):
#     """
#     # text is assumed to be sentences after sentence tokenisation of text.
#     lines = [nltk.word_tokenize(el) for el in lines]
#     lines = [nltk.pos_tag(el) for el in lines]
#
#     indianColleges = open('indianColleges.txt', 'r').read().lower()
#     indianColleges = set(indianColleges.split())
#
#     print(indianDegrees)
#     # instiregex = r'INSTI: {<DT.>?<NNP.*>+<IN.*>?<NNP.*>+}'
#     instiregex = r'INSTI: {<JJ.>?<NN.>?<IN.>?<DT.>?<NNP.*>+<IN.>?<NNP.*>+}'
#     chunkParser = nltk.RegexpParser(instiregex)
#
#     insti = []
#     degrees = []
#     for tagged_tokens in lines:
#         print(tagged_tokens)
#         chunked_tokens = chunkParser.parse(tagged_tokens)
#         for subtree in chunked_tokens.subtrees():
#             # print(subtree)
#             if subtree.label() == 'INSTI':
#                 for ind, leaf in enumerate(subtree.leaves()):
#                     # print(ind,leaf)
#                     if leaf[0].lower() in indianColleges and 'NNP' in leaf[1]:
#                         #	print(leaf)
#                         hit = " ".join([el[0] for el in tagged_tokens])
#                         insti.append(hit)
#             else:
#                 for ind, leaf in enumerate(subtree.leaves()):
#                     if leaf[0].lower() in indianDegrees:
#                         # print(leaf[0].lower())
#                         new_hit = " ".join([el[0] for el in tagged_tokens])
#                         degrees.append(new_hit)
#     return insti, degrees
#     """
#
#     insti = []
#     indianColleges = open('../util/indianColleges.txt','r').read().lower()
#     indianColleges = set(indianColleges.split())
#
#     indianDegrees = open('../util/indianColleges.txt', 'r').read().lower()
#     indianDegrees = set(indianDegrees.split())
#
#
#
#     lst_of_groups = group_extractor(lines)
#     for l in lst_of_groups:
#         a = l.split(" ")
#         for x in a:
#             if x.lower() in indianColleges:
#                 insti.append(l)
#                 break;
#
#      #entries = []
#      #for line in lines:
#       #   entries = entries + re.split('\t|\s\s+', line)
#     # print(entries)
#
#     return insti
#
#     """
#
# def extract_skills(text):
#     skills_list = open('../util/new_file.txt','r').read().lower()
#
#     skills_list = list(skills_list.split("\n"))
#     #print(skills_list)
#
#     #word_list = re.split('<space> | \n', text)
#     word_list = nltk.word_tokenize(text)
#     #print(word_list)
#     final_skill = []
#
#     for word in word_list:
#         #print(word.lower())
#         #print(word.lower())
#         #print(skills_list[-3])
#         if word.lower() in skills_list:
#            # print(word)
#             final_skill.append(word)
#
#     return final_skill
# """
# def extract_date(text):
#    # print(text)
#    # print(nlp(text).ents)
#     return [en.text for en in nlp(text).ents if en.label_ == 'DATE']
#
# # def extract_insti_degree(lines):
# #
# #     insti = []
# #     degree = []
# #     indianColleges = open('../util/indianColleges.txt', 'r').read().lower()
# #     indianColleges = set(indianColleges.split())
# #
# #     indianDegrees = open('../util/indianColleges.txt', 'r').read().lower()
# #     indianDegrees = set(indianDegrees.split())
# #
# #     entries = []
# #     for line in lines:
# #         entries = entries + re.split('\t|\s\s+', line)
# #
# #     print(entries)
# #
# #     lst_of_groups = group_extractor('\n'.join(lines))
# #     for l in lst_of_groups:
# #         a = l.split(" ")
# #         for x in a:
# #             if x.lower() in indianColleges:
# #                 insti.append(l)
# #                 break;
# #     return insti
#
#
# def process_main_text2(text):
#     doc = nlp(text.lower())
#     result = []
#     for token in doc:
#         if token.text in nlp.Defaults.stop_words:
#             continue
#         if token.is_punct:
#             continue
#         if token.lemma_ == '-PRON-':
#             continue
#         result.append(token.lemma_)
#     return result

def process_main_text1(text):
    doc = nlp(text.lower())
    result = []
    for token in doc:
        if token.is_punct:
            continue
        if token.lemma_ == '-PRON-':
            continue
        result.append(token.lemma_)
    return result


def process_main_text0(text):
    doc = nlp(text.lower())
    result = []
    for token in doc:
        if token.is_punct:
            continue
        result.append(token.text)
    return result


def calculate_similarity_with_processing(title, line, process_main_tex_foo=process_main_text1):
    # print(title, line)
    # process_main_tex_foo=process_main_text1
    title = nlp(' '.join(process_main_tex_foo(title)))
    line = nlp(' '.join(process_main_tex_foo(line)))
    for token in line:
        token_id=nlp.vocab.strings[token.text]
        if token_id not in nlp.vocab:
            return 0
    return title.similarity(line)


def get_label(line):
    # print("Line : ", line)
    global_max_bucket=0
    global_max_bucket_name="other"
    # mean_bucket=np.zeros([len(bucket2title), 1])
    # std_bucket=np.zeros([len(bucket2title), 1])

    for index, bucket in enumerate(bucket2title):
        scores = np.zeros([len(bucket2title[bucket]), 1])
        for count, title in enumerate(bucket2title[bucket]):
            scores[count]=calculate_similarity_with_processing(title, line)
        # mean_bucket[index]=np.mean(scores)
        # std_bucket[index]=np.std(scores)
        max_bucket=np.amax(scores)
        # print("--bucket : ", bucket, "  --mean : ", np.mean(scores), "  --max local bucket : ", max_bucket)

        if global_max_bucket<max_bucket:
            global_max_bucket=max_bucket
            global_max_bucket_name=bucket


    # prob=np.exp(-(global_max_bucket-mean_bucket)*(global_max_bucket-mean_bucket)/(2*std_bucket))
    # print("Max Bucket : ", global_max_bucket_name, global_max_bucket, max(mean_bucket))
    # print()
    # print()

    # print()
    return global_max_bucket_name, global_max_bucket


def extract_headers(texts, layouts=None):
    max_words_in_header=3
    prob_no_word=0
    thresh_prob1=0.09
    similarity_thresh_prob1=0.7
    thresh_prob2 = 0.6
    similarity_thresh_prob2 = 0.65

    headers={}
    for index, line in enumerate(texts):
        # if layouts and index>0 and index<(len(texts)-1):
        prob=1
        doc =nlp(line)

        for token in doc:
            token_id = nlp.vocab.strings[token.text]
            if token_id not in nlp.vocab:
                prob=prob*0.1

        main_text=process_main_text1(line)

        num_words=len(main_text)
        if num_words==0:
            prob=0
            continue
        elif num_words>max_words_in_header:
            prob=prob*np.exp(-2*(num_words-max_words_in_header))

        if doc[-1].text=='.':
            continue

        words=re.findall("[A-Za-z][^ ]*", line)
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

        if prob>thresh_prob1:
            label, similarity=get_label(line)
           # print("--line ", line)
           # print("--num_words ", num_words, "--prob", prob, "--label ", label, " --similarity : ", similarity)
            if similarity>similarity_thresh_prob1:
            #    print("--------------TITLE---------------------")
                headers[line]={"label":label, "similarity":similarity}
            elif prob>thresh_prob2 and similarity>similarity_thresh_prob2:
             #   print("--------------OTHER TITLE---------------------")
                headers[line] = {"label": "others", "similarity": similarity}

    return headers



def extract_buckets(data, headers):
    # lines="\n".join(data)
    # doc = nlp(lines)
    # displacy.serve(doc, style="ent")

    # print("--------------------- Printing sentences  ----------------------------------------------------------------------")
    # print()
    # lines = " ".join(data)
    # doc = nlp(lines)
    # for sent in doc.sents:
    #     print(sent.text)
    # print()
    # print()

    last_label='Personal Details'
    buckets=[]
    for line in data:
        if headers.get(line, None) is not None:
            last_label=headers[line]["label"]
        buckets.append({"line":line, "label":last_label})
       # print(last_label, '\t', line)

    return buckets




# def extract_address(lines):
#     method1=False
#
#     max_score=-1
#     max_score_line=''
#     for line in lines:
#         for feature in line2feature:
#             score=calculate_similarity_with_processing(line, feature, process_main_text0)
#             #print("address score : ",score, line)
#             if score>max_score:
#                 max_score=score
#                 max_score_line=line












