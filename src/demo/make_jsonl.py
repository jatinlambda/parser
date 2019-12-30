import sys
import os


def main():
    sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..'))
    current_dir = os.path.dirname(os.path.abspath(__file__))

    from src.parser_classes.rule_based_parser import ResumeParser
    from src.util.io_utils import read_pdf_and_docx


    data_dir_path = current_dir + '/../../dataset/samplecv'

    collected = read_pdf_and_docx(data_dir_path, command_logging=True)

    for file_path, file_content in collected.items():

        print('parsing file: ', file_path)

        parser = ResumeParser(file_path)
        parser.parse(file_content)

        lines=[]
        for line in parser.texts:
            if line['bucket']=='Skills' or line['bucket']=='Experience' or line['bucket']=='Projects':
                lines.append(line)




        if parser.unknown is False:
            print(parser.summary())

        print('++++++++++++++++++++++++++++++++++++++++++')

    print('count: ', len(collected))


if __name__ == '__main__':
    main()
