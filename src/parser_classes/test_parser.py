from src.util.parser_rules import *
from src.util.tokenizer_utils import word_tokenize
from src.util.headers_dict import bucket2title, title2bucket, headers_dict_init


class ResumeParser(object):

    def __init__(self):
        self.name = None
        self.unknown = True

    def parse(self, texts, print_line=False):
        headers_dict_init()
        self.raw = texts
        headers = extract_headers(self.raw)
        buckets = extract_buckets(self.raw, headers)


        self.education_lines=[]
        self.personal_lines=[]
        self.experience_lines=[]
        self.skills_lines=[]
        self.other_lines=[]
        self.project_lines=[]
        self.qualification_lines=[]
        self.hobbies_lines=[]
        self.extra_curricular_lines=[]
        self.objective_lines=[]

        for entry in buckets:
            if entry['label']=='Personal Details':
                self.personal_lines.append(entry['line'])
            elif entry['label']=='Experience':
                self.experience_lines.append(entry['line'])
            elif entry['label']=='Skills':
                self.skills_lines.append(entry['line'])
            elif entry['label']=='Projects':
                self.project_lines.append(entry['line'])
            elif entry['label']=='Qualifications':
                self.qualification_lines.append(entry['line'])
            elif entry['label']=='Education':
                self.education_lines.append(entry['line'])
            elif entry['label']=='Hobbies':
                self.hobbies_lines.append(entry['line'])
            elif entry['label']=='Extra curricular':
                self.extra_curricular_lines.append(entry['line'])
            elif entry['label']=='Objective':
                self.objective_lines.append(entry['line'])

        print(" ---name : ", extract_name(self.personal_lines))
        print(" ---mobile : ", extract_mobile(self.personal_lines))
        print(" ---email : ", extract_email(self.personal_lines))
        print(" ---address : ", extract_address(self.personal_lines))

        print(extract_insti(self.education_lines))


    def summary(self):
        print("Skiping Summary")
        return ""
