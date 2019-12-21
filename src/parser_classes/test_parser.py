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
        # print(headers)
        buckets = extract_buckets(self.raw, headers)
        education_lines=[]
        for entry in buckets:
            if entry['label']=="Eduaction":
                education_lines.append(entry['line'])
        print(extract_insti(education_lines))


    def summary(self):
        print("Skiping Summary")
        return ""
