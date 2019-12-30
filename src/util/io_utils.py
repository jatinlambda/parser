import os
from src.util.pdf_utils import pdf_to_text_tool
from src.util.docx_utils import docx_to_text


#converts pdf and docx files to text format and returns a dictionary
def read_pdf_and_docx(dir_path, collected=None, command_logging=False, callback=None):
    if collected is None:
        collected = dict()
    for f in os.listdir(dir_path):
        file_path = os.path.join(dir_path, f)
        if os.path.isfile(file_path):
            txt = None
            layout = None
            if f.lower().endswith('.docx'):
                if command_logging:
                    print('extracting text from docx: ', file_path)
                txt, layout = docx_to_text(file_path)
            elif f.lower().endswith('.pdf'):
                if command_logging:
                    print('extracting text from pdf: ', file_path)
                    txt, layout = pdf_to_text_tool(file_path)
            if txt is not None and len(txt) > 0:
                if callback is not None:
                    callback(len(collected), file_path, txt)
                collected[file_path] = {"text": txt, "layout": layout}
        elif os.path.isdir(file_path):
            read_pdf_and_docx(file_path, collected, command_logging, callback)
    return collected

