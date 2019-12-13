import re
import spacy
from spacy.matcher import Matcher
from src.util.tokenizer_utils import word_tokenize
import spacy
import numpy as np
from src.util.headers_dict import bucket2title, title2bucket, indexes_title

# load pre-trained model
nlp = spacy.load('en_core_web_md')

# initialize matcher with a vocab
matcher = Matcher(nlp.vocab)

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
    nlp_text = nlp(line)

    # First name and Last name are always Proper Nouns
    pattern = [{'POS': 'PROPN'}, {'POS': 'PROPN'}]

    matcher.add('NAME', None, pattern)

    matches = matcher(nlp_text)

    for match_id, start, end in matches:
        span = nlp_text[start:end]
        return span.text


def extract_objective(parts, line):
    found = False
    result = None
    for w in parts:
        if w.find('objective') != -1:
            found = True
            continue
        if found and ':' not in w:
            result = w
            break
    return result


def process_main_text2(text):
    doc = nlp(text.lower())
    result = []
    for token in doc:
        if token.text in nlp.Defaults.stop_words:
            continue
        if token.is_punct:
            continue
        if token.lemma_ == '-PRON-':
            continue
        result.append(token.lemma_)
    return result

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


# def calculate_similarity_with_processing2(title, line):
#     title = nlp(' '.join(process_main_text2(title)))
#     line = nlp(' '.join(process_main_text2(line)))
#     for token in line:
#         token_id=nlp.vocab.strings[token.text]
#         if token_id not in nlp.vocab:
#             return 0
#     return title.similarity(line)

def calculate_similarity_with_processing(title, line):
    # print(title, line)
    process_main_tex_foo=process_main_text1
    title = nlp(' '.join(process_main_tex_foo(title)))
    line = nlp(' '.join(process_main_tex_foo(line)))
    for token in line:
        token_id=nlp.vocab.strings[token.text]
        if token_id not in nlp.vocab:
            return 0
    return title.similarity(line)

# def get_label(line):
#     label="default"
#     scores=np.zeros([len(title2bucket),1])
#     # print("Line : ", line)
#     for index, title in enumerate(title2bucket, start=0):
#         scores[index]=calculate_similarity_with_processing1(title, line)
#         # print("title : ", title, scores[index], calculate_similarity_with_processing2(title, line))
#
#     max_index=np.argmax(scores, axis=0)
#     print(max_index)
#     max_index=max_index[0]
#     # print("Max title : ", indexes_title[max_index], np.amax(scores))
#     # print()
#     # print()
#     return label


def get_label(line):
    # print("Line : ", line)
    global_max_bucket=0
    global_max_bucket_name="other"
    mean_bucket=np.zeros([len(bucket2title), 1])
    # std_bucket=np.zeros([len(bucket2title), 1])

    for index, bucket in enumerate(bucket2title):
        scores = np.zeros([len(bucket2title[bucket]), 1])
        for count, title in enumerate(bucket2title[bucket]):
            scores[count]=calculate_similarity_with_processing(title, line)
        mean_bucket[index]=np.mean(scores)
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


def extract_headers(data):
    weight_num_words=100
    max_words_in_header=4
    weight_full_stop=1000
    weight_capital_letter=1000
    weight_no_word=10000
    prob_no_word=0
    thresh_prob1=0.09
    thresh_prob2=0.7

    # print(data)
    headers=[]
    for line in data:

        cost=0
        prob=1
        doc =nlp(line)

        main_text=process_main_text1(line)

        num_words=len(main_text)
        if num_words>max_words_in_header or num_words==0:
            cost=cost+weight_num_words*np.exp(num_words-max_words_in_header)
            prob=prob*np.exp(-2*(num_words-max_words_in_header))

        word_found=False
        for token in doc:
            if token.pos_!="PUNCT":
                word_found=True
                break

        if not word_found:
            cost=cost+weight_no_word
            prob=prob*prob_no_word

        if doc[-1].pos_=="PUNCT" and doc[-1].text=='.':
            cost=cost+weight_full_stop
            prob=prob*0.1

        first_word=re.search("^[a-z]+$", doc[0].text)
        if first_word is not None:
            cost=cost+weight_capital_letter
            prob=prob*0.1

        if prob>thresh_prob1:
            label, similarity=get_label(line)
            # print("--line ", line, "     --main line ", main_text)
            # print("--num_words ", num_words, "--cost ", cost, "--prob", prob, "--label ", label, " --similarity : ", similarity)
            if similarity>thresh_prob2:
                # print("--------------TITLE---------------------")
                headers.append({"line":line, "label":label, "similarity":similarity})

            # print()
            # for token in doc:
            #     print("-----token  ", token.text, token.pos_, token.tag_,  token.shape_)
            # print()
            # print()
    return headers


def extract_buckets(data, headers):
    last_label='Personal Details'
    buckets=[]
    header_index=0
    for line in data:
        if line==headers[header_index]["line"]:
            last_label=header_index[header_index]["label"]
            header_index+=1
        buckets.append({"line":line, "label":last_label})
        print(last_label, '\t', line)

    return buckets