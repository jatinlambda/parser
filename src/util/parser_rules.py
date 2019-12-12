import re
import spacy
from spacy.matcher import Matcher
from src.util.tokenizer_utils import word_tokenize
import spacy
import numpy as np

# load pre-trained model
nlp = spacy.load('en_core_web_sm')

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

    

headers = {}

titles = ['Experience','Skills','Projects','Qualifications','Education','Hobbies','Extra curricular','Personal Details']

for title in titles:
    headers[title] = []


headers['Personal Details'].append('Personal Details')
headers['Personal Details'].append('Personal Information')
headers['Personal Details'].append('Personal Info')
headers['Personal Details'].append('Personal Interests')
headers['Personal Details'].append('Personal Profile')
headers['Personal Details'].append('Personal particulars')

headers['Experience'].append('Experience')
headers['Experience'].append('experience')
headers['Experience'].append('work experience')
headers['Experience'].append('working experience')
headers['Experience'].append('expertise')
headers['Experience'].append('professional experience')
headers['Experience'].append('internships')

headers['Skills'].append('Skills')
headers['Skills'].append('skills')
headers['Skills'].append('specialties')
headers['Skills'].append('key skills')
headers['Skills'].append('additional skills')
headers['Skills'].append('Technical Skills')
headers['Skills'].append('Management Skills')

headers['Projects'].append('Projects')
headers['Projects'].append('key projects')
headers['Projects'].append('projects')
headers['Projects'].append('projects done')
headers['Projects'].append('projects completed')
headers['Projects'].append('projects undertaken')
headers['Projects'].append('academic projects')
headers['Projects'].append('Major Projects')
headers['Projects'].append('Other Projects')


headers['Qualifications'].append('Qualifications')
headers['Qualifications'].append('qualifications')
headers['Qualifications'].append('core qualifications')
headers['Qualifications'].append('technical qualifications')
headers['Qualifications'].append('academic qualifications')
headers['Qualifications'].append('educational qualifications')
headers['Qualifications'].append('achievements')
headers['Qualifications'].append('awards and honours')
headers['Qualifications'].append('awards')
headers['Qualifications'].append('certifications')

headers['Education'].append('education')
headers['Education'].append('educational details')
headers['Education'].append('academics')

headers['Hobbies'].append('hobbies')

headers['Extra curricular'].append('extra_curriculars')
headers['Extra curricular'].append('extra_curricular activities')


headers2 = {}

def reverse_adj():
    for k,v in headers.items():
        for m in v:
            headers2[m] = k




def extract_headers(data):
    weight_num_words=100
    max_words_in_header=3
    weight_full_stop=1000
    weight_capital_letter=1000
    weight_no_word=10000
    prob_no_word=0

    def process_main_text(text):
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

    # print(data)
    for line in data:
        cost=0
        prob=1
        doc =nlp(line)

        main_text=process_main_text(line)

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

        print("--line ", line, "--main line ", main_text)
        print("--num_words ", num_words, "--cost ", cost, "--prob", prob)
        print()
        for token in doc:
            print("-----token  ", token.text, token.pos_, token.tag_,  token.shape_)
        print()
        print()