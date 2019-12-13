from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import os


def pdf_to_text_pdfminer(fname, pages=None):
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)

    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    infile = open(fname, 'rb')
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close()
    result = []
    for line in text.split('\n'):
        line2 = line.strip()
        if line2 != '':
            result.append(line2)
    return result

def pdf_to_text_pdftotext(fname, pages=None):
    os.system("pdftotext -layout "+fname+" .temp.txt")
    with open(".temp.txt") as file:
        lines=file.readlines()
    result=[]
    for line in lines:
        line=line.strip()
        if line!='':
            result.append(line)
    # print("************************")
    # print(result)
    return result
