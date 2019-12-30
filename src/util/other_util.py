from src.util.nlp_tools import nlp_process_text_foo

# check if two rectangles overlap
def overlap_rects(rect1, rect2):
    # If one rectangle is on left side of other
    if (rect1[0] > rect2[2] or rect2[0] > rect1[2]):
        return False
    # If one rectangle is above other
    if (rect1[3] < rect2[1] or rect2[3] < rect1[1]):
        return False
    return True

# preprocess a line to return a dictionary of line, location, its tokens and spacy nlp object
def preprocess_text(text, layout):
    tokens, doc=nlp_process_text_foo(text)
    return {'text':text, 'tokens': tokens, 'doc':doc, 'bbox':layout.bbox}