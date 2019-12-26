def overlap_rects(rect1, rect2):
    # If one rectangle is on left side of other
    if (rect1[0] > rect2[2] or rect2[0] > rect1[2]):
        return False
    # If one rectangle is above other
    if (rect1[3] < rect2[1] or rect2[3] < rect1[1]):
        return False
    return True

def multiple_rects_in_line(rect1, rect2, rect3):
    if rect1!=rect2 and rect1[3]>=rect2[3] and rect1[1]<=rect2[3]:
        return True
    if rect2!=rect3 and rect2[3]>=rect3[3] and rect2[1]<=rect3[3]:
        return True
    return False

# def preprocess_text(text, layout):
