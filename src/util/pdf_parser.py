import sys
import os
from pdf_to_text import pdf_to_text

def pdf_parser():

    current_dir = os.path.dirname(__file__)
    data_dir_path = current_dir + '/../../dataset/samplecv' # directory to scan for any pdf and docx files

    for file_name in os.listdir(data_dir_path):
        if file_name[-4:]=='.pdf':
            print(data_dir_path+'/'+file_name)
            print()
            lines=pdf_to_text(data_dir_path+'/'+file_name)
            for line in lines:
                print(line)
            print()
            break


def main():
    pdf_parser()


if __name__ == '__main__':
    main()