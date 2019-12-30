"""
Run this code to test the parser
It takes resumes in dataset/samplecv folder, make resume parser object for each resume, converts to text and extract buckets
"""

import sys
import os


def main():
    sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..'))
    current_dir = os.path.dirname(os.path.abspath(__file__))

    from src.parser_classes.rule_based_parser import ResumeParser
    from src.util.io_utils import read_pdf_and_docx


    data_dir_path = current_dir + '/../../dataset/samplecv' # directory to scan for any pdf and docx files
    collected = read_pdf_and_docx(data_dir_path, command_logging=True)

    for file_path, file_content in collected.items():
        print('parsing file: ', file_path)
        parser = ResumeParser(file_path)
        parser.parse(file_content, print_line=False)

        if parser.unknown is False:
            print(parser.summary())

        parser.save_json()

        print('++++++++++++++++++++++++++++++++++++++++++')

    print('count: ', len(collected))


if __name__ == '__main__':
    main()
