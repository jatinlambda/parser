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

    def summary(self):
        print("Skiping Summary")
        return ""
