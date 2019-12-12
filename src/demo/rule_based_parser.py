import sys
import os


def main():
    sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..'))

    from src.parser_classes.rule_based_parser import ResumeParser
    from src.util.io_utils import read_pdf_and_docx

    import pickle

    current_dir = os.path.dirname(os.path.abspath(__file__))

    data_dir_path = current_dir + '/../../dataset/samplecv' # directory to scan for any pdf and docx files

    collected = read_pdf_and_docx(data_dir_path, command_logging=True)

    fp=open('outfile', 'wb')
    for file_path, file_content in collected.items():

        print('parsing file: ', file_path)

        # print(file_content)

        parser = ResumeParser()
        parser.parse(file_content)
        print(parser.raw) # print out the raw contents extracted from pdf or docx files



        pickle.dump(parser.raw, fp)

        if parser.unknown is False:
            print(parser.summary())

        print('++++++++++++++++++++++++++++++++++++++++++')

    print('count: ', len(collected))


if __name__ == '__main__':
    main()
