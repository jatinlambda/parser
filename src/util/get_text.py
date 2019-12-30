from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LTTextBoxHorizontal
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import time
from tika import parser

# import tabula
# import json

# rsrcmgr = PDFResourceManager()
laparams = LAParams(line_overlap=0.1,
                 char_margin=2.0,
                 line_margin=0.0000000001,
                 word_margin=0.05,
                 boxes_flow=0.5,
                 detect_vertical=False,
                 all_texts=False)
# device = PDFPageAggregator(rsrcmgr, laparams=laparams)
# interpreter = PDFPageInterpreter(rsrcmgr, device)


def get_columns(fname):
    document = open(fname, 'rb')

    rsrcmgr = PDFResourceManager()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    pages = []
    for page in PDFPage.get_pages(document):
        pages.append(page)
    num_pages=len(pages)

    def overlap(rect1, rect2):
        # If one rectangle is on left side of other
        if (rect1[0] > rect2[2] or rect2[0] > rect1[2]):
            return False
        # If one rectangle is above other
        if (rect1[3] < rect2[1] or rect2[3] < rect1[1]):
            return False
        return True


    doc_part_rects=[]
    doc_text_boxes=[]

    # Create figure and axes
    # fig, ax = plt.subplots(1)

    leftmost_x = 150
    rightmost_x = 350
    minimum_height_top = 150
    minimum_height_bottom = 250

    round_up=4

    page_num=0
    for page in pages:
        # start = time.process_time()

        interpreter.process_page(page)
        layout = device.get_result()

        doc_text_boxes.append([])
        doc_part_rects.append([])

        # print("before element time", time.process_time() - start)

        topmost_y=900*(num_pages-page_num)
        bottommost_y=900*(num_pages-page_num-1)

        part_rects = [(leftmost_x, bottommost_y, rightmost_x, topmost_y)]
        # layout = sorted(layout, key=lambda element: (element.bbox[3] - element.bbox[1]))
        layout=sorted(layout, key=lambda element : (element.bbox[2]-element.bbox[0]))

        # print("len layout: ", len(layout))


        # start = time.process_time()
        for element in layout:
            if isinstance(element, LTTextBoxHorizontal):
                element.bbox=list(element.bbox)
                element.bbox[1]=(int(element.bbox[1])/round_up)*round_up+bottommost_y
                element.bbox[3] =(int(element.bbox[3])/round_up)*round_up +bottommost_y

                doc_text_boxes[page_num].append(element)
                # rect = patches.Rectangle((element.bbox[0], element.bbox[1]), element.bbox[2]-element.bbox[0], element.bbox[3]-element.bbox[1], linewidth=1, edgecolor='r', facecolor='none')
                # ax.add_patch(rect)

                new_part_rects=[]
                for part_rect in part_rects:
                    if not overlap(part_rect, element.bbox):
                        new_part_rects.append(part_rect)
                    else:
                        if element.bbox[0]<=part_rect[0] and element.bbox[2]>=part_rect[2]:

                            if (part_rect[3]-element.bbox[3])>minimum_height_top:
                                new_part_rects.append((part_rect[0], element.bbox[3], part_rect[2], part_rect[3]))

                            if (element.bbox[1]-part_rect[1])>minimum_height_bottom:
                                new_part_rects.append((part_rect[0], part_rect[1], part_rect[2], element.bbox[1]))

                        elif element.bbox[0]<=part_rect[0] and element.bbox[2]>part_rect[0]:

                            new_part_rects.append((element.bbox[2], part_rect[1], part_rect[2], part_rect[3]))

                            if part_rect[3]==topmost_y and (part_rect[3]-element.bbox[3])>minimum_height_top:
                                new_part_rects.append((part_rect[0], element.bbox[3], part_rect[2], part_rect[3]))

                            if part_rect[1]==bottommost_y and (element.bbox[1]-part_rect[1])>minimum_height_bottom:
                                new_part_rects.append((part_rect[0], part_rect[1], part_rect[2], element.bbox[1]))

                        elif element.bbox[0]<part_rect[2] and element.bbox[2]>=part_rect[2]:

                            new_part_rects.append((part_rect[0], part_rect[1], element.bbox[0], part_rect[3]))

                            if part_rect[3]==topmost_y and (part_rect[3]-element.bbox[3])>minimum_height_top:
                                new_part_rects.append((part_rect[0], element.bbox[3], part_rect[2], part_rect[3]))

                            if part_rect[1]==bottommost_y and (element.bbox[1]-part_rect[1])>minimum_height_bottom:
                                new_part_rects.append((part_rect[0], part_rect[1], part_rect[2], element.bbox[1]))

                        elif element.bbox[0]>part_rect[0] and element.bbox[2]<part_rect[2]:

                            new_part_rects.append((part_rect[0], part_rect[1], element.bbox[0], part_rect[3]))

                            new_part_rects.append((element.bbox[2], part_rect[1], part_rect[2], part_rect[3]))

                            if part_rect[3]==topmost_y and (part_rect[3]-element.bbox[3])>minimum_height_top:
                                new_part_rects.append((part_rect[0], element.bbox[3], part_rect[2], part_rect[3]))

                            if part_rect[1]==bottommost_y and (element.bbox[1]-part_rect[1])>minimum_height_bottom:
                                new_part_rects.append((part_rect[0], part_rect[1], part_rect[2], element.bbox[1]))

                        elif element.bbox[0]==part_rect[2] or element.bbox[2]==part_rect[0]:
                            new_part_rects.append(part_rect)
                        else:
                            print(part_rect)
                            print(element.bbox)
                            raise Exception("Unhandled case in overlaping rectangles")

                part_rects=new_part_rects

        # print("element time", time.process_time() - start)


        largest_lower_rect_height=0
        largest_upper_rect_height = 0
        largest_lower_rect=None
        largest_upper_rect=None
        single_largest_rect_present=False
        single_largest_rect=None

        # part_rects.sort(key=lambda rect : rect[3]-rect[1])
        # print("len part rect : ", len(part_rects))

        for part_rect in part_rects:
            if part_rect[1]==bottommost_y and part_rect[3]==topmost_y:
                single_largest_rect_present=True
                single_largest_rect=part_rect
                break
            elif part_rect[1]==bottommost_y and (part_rect[3]-part_rect[1])>largest_lower_rect_height:
                largest_lower_rect=part_rect
                largest_lower_rect_height=(part_rect[3]-part_rect[1])
            elif part_rect[3]==topmost_y and (part_rect[3]-part_rect[1])>largest_upper_rect_height:
                largest_upper_rect=part_rect
                largest_upper_rect_height=(part_rect[3]-part_rect[1])

        if single_largest_rect_present:
            part_rect = single_largest_rect
            # rect = patches.Rectangle((part_rect[0], part_rect[1]), part_rect[2] - part_rect[0],
            #                          part_rect[3] - part_rect[1], linewidth=1, edgecolor='b', facecolor='none')
            # ax.add_patch(rect)
            doc_part_rects[page_num].append(single_largest_rect)

        else:
            if largest_lower_rect:
                part_rect=largest_lower_rect
                # rect = patches.Rectangle((part_rect[0], part_rect[1]), part_rect[2] - part_rect[0],
                #                                                       part_rect[3] - part_rect[1], linewidth=1, edgecolor='b', facecolor='none')
                # ax.add_patch(rect)
                doc_part_rects[page_num].append(largest_lower_rect)

            if largest_upper_rect:
                part_rect=largest_upper_rect
                # rect = patches.Rectangle((part_rect[0], part_rect[1]), part_rect[2] - part_rect[0],
                #                          part_rect[3] - part_rect[1], linewidth=1, edgecolor='b', facecolor='none')
                # ax.add_patch(rect)
                doc_part_rects[page_num].append(largest_upper_rect)


        page_num += 1

        # tabula.convert_into(fname, ".temp.json", output_format="json", pages=str(page_num))
        # tables = None
        # with open('.temp.json') as json_file:
        #     tables = json.load(json_file)
        # for key in range(len(tables)):
        #     # print(key)
        #     part_rect=[tables[key]['left'], 900*(num_pages-page_num+1)-tables[key]['bottom'], tables[key]['right'], 900*(num_pages-page_num+1)-tables[key]['top']]
        #
        #     rect = patches.Rectangle((part_rect[0], part_rect[1]), part_rect[2] - part_rect[0],
        #                              part_rect[3] - part_rect[1], linewidth=1, edgecolor='y', facecolor='none')
        #     ax.add_patch(rect)


    # print(tables)
    # print()
    # df = tabula.read_pdf(fname, multiple_tables=True, pages='all')
    # print(df)
    flat_doc_text_boxes=[]
    flat_doc_part_rects=[]

    column_score=0
    for i in range(num_pages):
        text_section_height_score=(max(doc_text_boxes[i], key=lambda element: element.bbox[3]).bbox[3] - min(doc_text_boxes[i], key=lambda element: element.bbox[1]).bbox[1]) / 900
        for part_rect in doc_part_rects[i]:
            column_score+=(part_rect[3]-part_rect[1])*text_section_height_score
            flat_doc_part_rects.append(part_rect)
        for element in doc_text_boxes[i]:
            flat_doc_text_boxes.append(element)

    column_score=column_score/(900*num_pages)
    print(column_score)
    # print(len(flat_doc_part_rects))
    if column_score<0.4:
        flat_doc_part_rects=[flat_doc_part_rects[0]]

    return flat_doc_text_boxes, flat_doc_part_rects, num_pages


# def split_column(text_boxes, part_rect, side_first=None):


def get_text(fname):
    doc_text_boxes, doc_part_rects, num_pages=get_columns(fname)
    # print(len(doc_part_rects))

    # fig, ax = plt.subplots(1)
    #
    # for element in doc_text_boxes:
    #     rect = patches.Rectangle((element.bbox[0], element.bbox[1]), element.bbox[2] - element.bbox[0],
    #                              element.bbox[3] - element.bbox[1], linewidth=1, edgecolor='r', facecolor='none')
    #     ax.add_patch(rect)
    #
    # for part_rect in doc_part_rects:
    #     rect = patches.Rectangle((part_rect[0], part_rect[1]), part_rect[2] - part_rect[0],
    #                              part_rect[3] - part_rect[1], linewidth=1, edgecolor='b', facecolor='none')
    #     ax.add_patch(rect)
    #
    # plt.axis([0, 700, 0, 900 * num_pages])
    # plt.show()


    doc_text_boxes.sort(key=lambda element: element.bbox[0])
    doc_text_boxes.sort(key=lambda element: element.bbox[1], reverse=True)

    doc_part_rects.sort(key=lambda rect: rect[1], reverse=True)


    ordered_text_boxes = []
    part_rect_num=0
    num_part_rects=len(doc_part_rects)
    left_column=[]
    right_column=[]

    for element in doc_text_boxes:
        if part_rect_num<num_part_rects:
            if element.bbox[1] >= doc_part_rects[part_rect_num][1] and element.bbox[3] <= doc_part_rects[part_rect_num][3]:
                if element.bbox[0]<=doc_part_rects[part_rect_num][0]:
                    left_column.append(element)
                else:
                    right_column.append(element)
            elif num_part_rects>(part_rect_num+1) and doc_part_rects[part_rect_num][1]==doc_part_rects[part_rect_num+1][3] and\
                            element.bbox[1] >= doc_part_rects[part_rect_num+1][1] and element.bbox[3] <= doc_part_rects[part_rect_num+1][3]:
                part_rect_num += 1
                if element.bbox[0]<=doc_part_rects[part_rect_num][0]:
                    left_column.append(element)
                else:
                    right_column.append(element)
            else:
                if left_column and right_column:
                    if left_column[-1].bbox[1]<right_column[-1].bbox[1]:
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

            if element.bbox[1]<doc_part_rects[part_rect_num][1]:
                part_rect_num+=1
                right_column=[]
                left_column=[]
        else:
            ordered_text_boxes.append([element])


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

    # print(ordered_text_boxes)
    # for box in ordered_text_boxes:
    #     print(box)

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
                    print(line2)
    return result_text, result_layout


def pdf_to_text_tika(fname):
    parsedPDF = parser.from_file(fname)
    result_text = []
    for line in parsedPDF['content'].split('\n'):
        line2 = line.strip()
        if line2 != '':
            result_text.append(line2)
    for text in result_text:
        print(text)
    return result_text, None


if __name__ == "__main__":
    start = time.process_time()
    fname = '/home/jatin/iitb/flexiele/parser/dataset/samplecv/3 Bhirgu Sharma.pdf'
    print(fname)
    text, layout = pdf_to_text_tika(fname)
    print("time", time.process_time() - start)
    print("------------")
    #
    start = time.process_time()
    fname = '/home/jatin/iitb/flexiele/parser/dataset/samplecv/5 Sourabh.pdf'
    print(fname)
    text, layout = pdf_to_text_tika(fname)
    print("time", time.process_time() - start)
    print("------------")
    #
    start = time.process_time()
    fname = '/home/jatin/iitb/flexiele/parser/dataset/samplecv/6 Sujeet.pdf'
    print(fname)
    text, layout = pdf_to_text_tika(fname)
    print("time", time.process_time() - start)
    print("------------")

    start = time.process_time()
    fname = '/home/jatin/iitb/flexiele/parser/dataset/samplecv/iimjobs_Gaurav_Suman.pdf'
    print(fname)
    text, layout = pdf_to_text_tika(fname)
    print("time", time.process_time() - start)
    print("------------")
    #
    start = time.process_time()
    fname = '/home/jatin/iitb/flexiele/parser/dataset/samplecv/iimjobs_Swostik_Rout.pdf'
    print(fname)
    text, layout = pdf_to_text_tika(fname)
    print("time", time.process_time() - start)
    print("------------")
    #
    start = time.process_time()
    fname = '/home/jatin/iitb/flexiele/dataset/more/Copy of IIITN_AMAN_SONI_CV.pdf'
    print(fname)
    text, layout = pdf_to_text_tika(fname)
    print("time", time.process_time() - start)
    print("------------")

    start = time.process_time()
    fname = '/home/jatin/iitb/flexiele/parser/dataset/samplecv/5 yrs Sameer.Sinha.pdf'
    print(fname)
    text, layout = pdf_to_text_tika(fname)
    print("time", time.process_time() - start)
    print("------------")

    # start = time.process_time()
    # fname='/home/jatin/iitb/flexiele/parser/dataset/samplecv/3 Bhirgu Sharma.pdf'
    # print(fname)
    # text, layout=get_text(fname)
    # print("time", time.process_time() - start)
    # print("------------")
    # #
    # start = time.process_time()
    # fname = '/home/jatin/iitb/flexiele/parser/dataset/samplecv/5 Sourabh.pdf'
    # print(fname)
    # text, layout = get_text(fname)
    # print("time", time.process_time() - start)
    # print("------------")
    # #
    # start = time.process_time()
    # fname = '/home/jatin/iitb/flexiele/parser/dataset/samplecv/6 Sujeet.pdf'
    # print(fname)
    # text, layout = get_text(fname)
    # print("time", time.process_time() - start)
    # print("------------")
    #
    # start = time.process_time()
    # fname = '/home/jatin/iitb/flexiele/parser/dataset/samplecv/iimjobs_Gaurav_Suman.pdf'
    # print(fname)
    # text, layout = get_text(fname)
    # print("time", time.process_time() - start)
    # print("------------")
    # #
    # start = time.process_time()
    # fname = '/home/jatin/iitb/flexiele/parser/dataset/samplecv/iimjobs_Swostik_Rout.pdf'
    # print(fname)
    # text, layout = get_text(fname)
    # print("time", time.process_time() - start)
    # print("------------")
    # #
    # start = time.process_time()
    # fname = '/home/jatin/iitb/flexiele/dataset/more/Copy of IIITN_AMAN_SONI_CV.pdf'
    # print(fname)
    # text, layout = get_text(fname)
    # print("time", time.process_time() - start)
    # print("------------")
    #
    # start = time.process_time()
    # fname = '/home/jatin/iitb/flexiele/parser/dataset/samplecv/5 yrs Sameer.Sinha.pdf'
    # print(fname)
    # text, layout = get_text(fname)
    # print("time", time.process_time() - start)
    # print("------------")


