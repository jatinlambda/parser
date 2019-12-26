# from io import StringIO
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LTTextBoxHorizontal
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from src.util.other_util import overlap_rects
import time
import os

laparams = LAParams(line_overlap=0.1,
                        char_margin=2.0,
                        line_margin=0.0001,
                        word_margin=0.1,
                        boxes_flow=0.5,
                        detect_vertical=False,
                        all_texts=False)

# def pdf_to_text_pdfminer(fname, pages=None):
#     if not pages:
#         pagenums = set()
#     else:
#         pagenums = set(pages)
#
#     output = StringIO()
#     manager = PDFResourceManager()
#     converter = TextConverter(manager, output, laparams=LAParams())
#     interpreter = PDFPageInterpreter(manager, converter)
#
#     infile = open(fname, 'rb')
#     for page in PDFPage.get_pages(infile, pagenums):
#         interpreter.process_page(page)
#     infile.close()
#     converter.close()
#     text = output.getvalue()
#     output.close()
#     result = []
#     for line in text.split('\n'):
#         line2 = line.strip()
#         if line2 != '':
#             result.append(line2)
#     return result

def pdf_to_text_pdfminer(fname, pages=None):

    def get_columns(fname):
        document = open(fname, 'rb')

        rsrcmgr = PDFResourceManager()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        pages = []
        for page in PDFPage.get_pages(document):
            pages.append(page)
        num_pages = len(pages)

        doc_part_rects = []
        doc_text_boxes = []

        # Create figure and axes
        fig, ax = plt.subplots(1)

        leftmost_x = 150
        rightmost_x = 350
        minimum_height = 200
        round_up = 4

        page_num = 0
        for page in pages:
            # start = time.process_time()

            interpreter.process_page(page)
            layout = device.get_result()

            # print("before element time", time.process_time() - start)

            topmost_y = 900 * (num_pages - page_num)
            bottommost_y = 900 * (num_pages - page_num - 1)

            part_rects = [(leftmost_x, bottommost_y, rightmost_x, topmost_y)]
            # layout = sorted(layout, key=lambda element: (element.bbox[3] - element.bbox[1]))
            layout = sorted(layout, key=lambda element: (element.bbox[2] - element.bbox[0]))
            # print("len layout: ", len(layout))


            start = time.process_time()
            for element in layout:
                if isinstance(element, LTTextBoxHorizontal):
                    element.bbox = list(element.bbox)
                    element.bbox[1] = (int(element.bbox[1]) / round_up) * round_up + bottommost_y
                    element.bbox[3] = (int(element.bbox[3]) / round_up) * round_up + bottommost_y

                    doc_text_boxes.append(element)
                    rect = patches.Rectangle((element.bbox[0], element.bbox[1]), element.bbox[2] - element.bbox[0],
                                             element.bbox[3] - element.bbox[1], linewidth=1, edgecolor='r',
                                             facecolor='none')
                    ax.add_patch(rect)

                    new_part_rects = []
                    for part_rect in part_rects:
                        if not overlap_rects(part_rect, element.bbox):
                            new_part_rects.append(part_rect)
                        else:
                            if element.bbox[0] <= part_rect[0] and element.bbox[2] >= part_rect[2]:

                                if (part_rect[3] - element.bbox[3]) > minimum_height:
                                    new_part_rects.append((part_rect[0], element.bbox[3], part_rect[2], part_rect[3]))

                                if (element.bbox[1] - part_rect[1]) > minimum_height:
                                    new_part_rects.append((part_rect[0], part_rect[1], part_rect[2], element.bbox[1]))

                            elif element.bbox[0] <= part_rect[0] and element.bbox[2] > part_rect[0]:

                                new_part_rects.append((element.bbox[2], part_rect[1], part_rect[2], part_rect[3]))

                                if (part_rect[3] - element.bbox[3]) > minimum_height:
                                    new_part_rects.append((part_rect[0], element.bbox[3], part_rect[2], part_rect[3]))

                                if (element.bbox[1] - part_rect[1]) > minimum_height:
                                    new_part_rects.append((part_rect[0], part_rect[1], part_rect[2], element.bbox[1]))

                            elif element.bbox[0] < part_rect[2] and element.bbox[2] >= part_rect[2]:

                                new_part_rects.append((part_rect[0], part_rect[1], element.bbox[0], part_rect[3]))

                                if (part_rect[3] - element.bbox[3]) > minimum_height:
                                    new_part_rects.append((part_rect[0], element.bbox[3], part_rect[2], part_rect[3]))

                                if (element.bbox[1] - part_rect[1]) > minimum_height:
                                    new_part_rects.append((part_rect[0], part_rect[1], part_rect[2], element.bbox[1]))

                            elif element.bbox[0] > part_rect[0] and element.bbox[2] < part_rect[2]:

                                new_part_rects.append((part_rect[0], part_rect[1], element.bbox[0], part_rect[3]))

                                new_part_rects.append((element.bbox[2], part_rect[1], part_rect[2], part_rect[3]))

                                if (part_rect[3] - element.bbox[3]) > minimum_height:
                                    new_part_rects.append((part_rect[0], element.bbox[3], part_rect[2], part_rect[3]))

                                if (element.bbox[1] - part_rect[1]) > minimum_height:
                                    new_part_rects.append((part_rect[0], part_rect[1], part_rect[2], element.bbox[1]))

                            elif element.bbox[0] == part_rect[2] or element.bbox[2] == part_rect[0]:
                                new_part_rects.append(part_rect)
                            else:
                                print(part_rect)
                                print(element.bbox)
                                raise Exception("Unhandled case in overlaping rectangles")

                    part_rects = new_part_rects

            # print("element time", time.process_time() - start)


            largest_lower_rect_height = 0
            largest_upper_rect_height = 0
            largest_lower_rect = None
            largest_upper_rect = None
            single_largest_rect_present = False
            single_largest_rect = None

            # part_rects.sort(key=lambda rect : rect[3]-rect[1])
            # print("len part rect : ", len(part_rects))

            for part_rect in part_rects:
                if part_rect[1] == bottommost_y and part_rect[3] == topmost_y:
                    single_largest_rect_present = True
                    single_largest_rect = part_rect
                    break
                elif part_rect[1] == bottommost_y and (part_rect[3] - part_rect[1]) > largest_lower_rect_height:
                    largest_lower_rect = part_rect
                    largest_lower_rect_height = (part_rect[3] - part_rect[1])
                elif part_rect[3] == topmost_y and (part_rect[3] - part_rect[1]) > largest_upper_rect_height:
                    largest_upper_rect = part_rect
                    largest_upper_rect_height = (part_rect[3] - part_rect[1])

            if single_largest_rect_present:
                part_rect = single_largest_rect
                rect = patches.Rectangle((part_rect[0], part_rect[1]), part_rect[2] - part_rect[0],
                                         part_rect[3] - part_rect[1], linewidth=1, edgecolor='b', facecolor='none')
                ax.add_patch(rect)
                doc_part_rects.append(single_largest_rect)

            else:
                if largest_lower_rect:
                    part_rect = largest_lower_rect
                    rect = patches.Rectangle((part_rect[0], part_rect[1]), part_rect[2] - part_rect[0],
                                             part_rect[3] - part_rect[1], linewidth=1, edgecolor='b', facecolor='none')
                    ax.add_patch(rect)
                    doc_part_rects.append(largest_lower_rect)

                if largest_upper_rect:
                    part_rect = largest_upper_rect
                    rect = patches.Rectangle((part_rect[0], part_rect[1]), part_rect[2] - part_rect[0],
                                             part_rect[3] - part_rect[1], linewidth=1, edgecolor='b', facecolor='none')
                    ax.add_patch(rect)
                    doc_part_rects.append(largest_upper_rect)

            page_num += 1

        plt.axis([0, 700, 0, 900 * num_pages])
        # plt.show()
        # print(time.process_time() - start)
        return doc_text_boxes, doc_part_rects


    def get_text(fname):
        doc_text_boxes, doc_part_rects = get_columns(fname)

        doc_text_boxes.sort(key=lambda element: element.bbox[0])
        doc_text_boxes.sort(key=lambda element: element.bbox[1], reverse=True)

        doc_part_rects.sort(key=lambda rect: rect[1], reverse=True)

        ordered_text_boxes = []
        part_rect_num = 0
        num_part_rects = len(doc_part_rects)
        left_column = []
        right_column = []

        for element in doc_text_boxes:
            if element.bbox[1] >= doc_part_rects[part_rect_num][1] and element.bbox[3] <= doc_part_rects[part_rect_num][
                3]:
                if element.bbox[0] <= doc_part_rects[part_rect_num][0]:
                    left_column.append(element)
                else:
                    right_column.append(element)
            elif num_part_rects > (part_rect_num + 1) and doc_part_rects[part_rect_num][1] == \
                    doc_part_rects[part_rect_num + 1][3] and \
                            element.bbox[1] >= doc_part_rects[part_rect_num + 1][1] and element.bbox[3] <= \
                    doc_part_rects[part_rect_num + 1][3]:
                part_rect_num += 1
                if element.bbox[0] <= doc_part_rects[part_rect_num][0]:
                    left_column.append(element)
                else:
                    right_column.append(element)
            else:
                if left_column and right_column:
                    if left_column[-1].bbox[1] < right_column[-1].bbox[1]:
                        ordered_text_boxes.append(right_column)
                        ordered_text_boxes.append(left_column)
                    else:
                        ordered_text_boxes.append(left_column)
                        ordered_text_boxes.append(right_column)
                elif left_column:
                    ordered_text_boxes.append(left_column)
                elif right_column:
                    ordered_text_boxes.append(right_column)
                ordered_text_boxes.append([element])

            if element.bbox[1] < doc_part_rects[part_rect_num][1] and num_part_rects > (part_rect_num + 1):
                part_rect_num += 1
                right_column = []
                left_column = []

        if left_column and right_column:
            if left_column[-1].bbox[1] < right_column[-1].bbox[1]:
                ordered_text_boxes.append(right_column)
                ordered_text_boxes.append(left_column)
            else:
                ordered_text_boxes.append(left_column)
                ordered_text_boxes.append(right_column)
        elif left_column:
            ordered_text_boxes.append(left_column)
        elif right_column:
            ordered_text_boxes.append(right_column)

        # new_ordered_text_boxes=[]
        # text=[]
        # new_ordered_text_boxes = [item for sublist in ordered_text_boxes for item in sublist]
        # text = [element.get_text() for element in new_ordered_text_boxes]
        result_text=[]
        result_layout=[]
        for sublist in ordered_text_boxes:
            for element in sublist:
                text_line = element.get_text()
                for line in text_line.split('\n'):
                    line2 = line.strip()
                    if line2 != '':
                        result_text.append(line2)
                        result_layout.append(element)
                        # print(line2)
                # new_ordered_text_boxes.append(sublist)
                # text.append(text_line)

        return result_text, result_layout

    return get_text(fname)


def pdf_to_text_pdftotext(fname, pages=None):
    os.system('pdftotext -layout "' + fname + '" .temp.txt')
    with open(".temp.txt" ,'r', errors='ignore') as file:
        lines=file.readlines()
    result=[]
    for line in lines:
        line=line.strip()
        if line!='':
            result.append(line)
    # print("************************")
    # print(result)
    return result, None
