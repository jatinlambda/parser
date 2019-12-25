from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LTTextBoxHorizontal
from shapely.geometry import Polygon
import tabula




def get_columns(fname):
    document = open(fname, 'rb')

    rsrcmgr = PDFResourceManager()
    laparams = LAParams(line_overlap=0.1,
                 char_margin=2.0,
                 line_margin=0.001,
                 word_margin=0.1,
                 boxes_flow=0.5,
                 detect_vertical=False,
                 all_texts=False)
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    num_pages=sum(1 for _ in PDFPage.get_pages(document))
    pages = PDFPage.get_pages(document)

    def overlap(rect1, rect2):
        try:
            p1 = Polygon([(rect1[0], rect1[1]), (rect1[2], rect1[1]), (rect1[2], rect1[3]), (rect1[0], rect1[3])])
            p2 = Polygon([(rect2[0], rect2[1]), (rect2[2], rect2[1]), (rect2[2], rect2[3]), (rect2[0], rect2[3])])
            return (p1.intersects(p2))
        except:
            return True

    doc_part_rects=[]
    doc_text_boxes=[]

    import matplotlib.pyplot as plt
    import matplotlib.patches as patches

    # Create figure and axes
    fig, ax = plt.subplots(1)

    leftmost_x = 150
    rightmost_x = 400
    minimum_height = 100
    round_up=4

    page_num=0
    for page in pages:
        interpreter.process_page(page)
        layout = device.get_result()

        topmost_y=900*(num_pages-page_num)
        bottommost_y=900*(num_pages-page_num-1)

        part_rects = [(leftmost_x, bottommost_y, rightmost_x, topmost_y)]
        layout=sorted(layout, key=lambda element : (element.bbox[2]-element.bbox[1]))

        for element in layout:
            if isinstance(element, LTTextBoxHorizontal):
                element.bbox=list(element.bbox)
                for key in range(4):
                    element.bbox[key]=int(element.bbox[key]/round_up)*round_up
                element.bbox[1]=element.bbox[1]+900*(num_pages-page_num-1)
                element.bbox[3] = element.bbox[3] +900*(num_pages-page_num-1)

                doc_text_boxes.append(element)
                # data.append({'x0': element.bbox[0], 'y0':element.bbox[1], 'text':element.get_text()})
                rect = patches.Rectangle((element.bbox[0], element.bbox[1]), element.bbox[2]-element.bbox[0], element.bbox[3]-element.bbox[1], linewidth=1, edgecolor='r', facecolor='none')
                ax.add_patch(rect)
                # print(element.bbox)


                new_part_rects=[]
                for part_rect in part_rects:
                    if not overlap(part_rect, element.bbox):
                        new_part_rects.append(part_rect)
                    else:
                        if element.bbox[0]<=part_rect[0] and element.bbox[2]>=part_rect[2]:

                            if (part_rect[3]-element.bbox[3])>minimum_height:
                                new_part_rects.append((part_rect[0], element.bbox[3], part_rect[2], part_rect[3]))

                            if (element.bbox[1]-part_rect[1])>minimum_height:
                                new_part_rects.append((part_rect[0], part_rect[1], part_rect[2], element.bbox[1]))

                        elif element.bbox[0]<=part_rect[0] and element.bbox[2]>part_rect[0]:

                            new_part_rects.append((element.bbox[2], part_rect[1], part_rect[2], part_rect[3]))

                            if (part_rect[3]-element.bbox[3])>minimum_height:
                                new_part_rects.append((part_rect[0], element.bbox[3], part_rect[2], part_rect[3]))

                            if (element.bbox[1]-part_rect[1])>minimum_height:
                                new_part_rects.append((part_rect[0], part_rect[1], part_rect[2], element.bbox[1]))

                        elif element.bbox[0]<part_rect[2] and element.bbox[2]>=part_rect[2]:

                            new_part_rects.append((part_rect[0], part_rect[1], element.bbox[0], part_rect[3]))

                            if (part_rect[3]-element.bbox[3])>minimum_height:
                                new_part_rects.append((part_rect[0], element.bbox[3], part_rect[2], part_rect[3]))

                            if (element.bbox[1]-part_rect[1])>minimum_height:
                                new_part_rects.append((part_rect[0], part_rect[1], part_rect[2], element.bbox[1]))

                        elif element.bbox[0]>part_rect[0] and element.bbox[2]<part_rect[2]:

                            new_part_rects.append((part_rect[0], part_rect[1], element.bbox[0], part_rect[3]))

                            new_part_rects.append((element.bbox[2], part_rect[1], part_rect[2], part_rect[3]))

                            if (part_rect[3]-element.bbox[3])>minimum_height:
                                new_part_rects.append((part_rect[0], element.bbox[3], part_rect[2], part_rect[3]))

                            if (element.bbox[1]-part_rect[1])>minimum_height:
                                new_part_rects.append((part_rect[0], part_rect[1], part_rect[2], element.bbox[1]))

                        elif element.bbox[0]==part_rect[2] or element.bbox[2]==part_rect[0]:
                            new_part_rects.append(part_rect)
                        else:
                            print(part_rect)
                            print(element.bbox)
                            raise Exception("Unhandled case in overlaping rectangles")

                part_rects=new_part_rects

        largest_lower_rect_height=0
        largest_upper_rect_height = 0
        largest_lower_rect=None
        largest_upper_rect=None
        single_largest_rect_present=False
        single_largest_rect=None

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
            rect = patches.Rectangle((part_rect[0], part_rect[1]), part_rect[2] - part_rect[0],
                                     part_rect[3] - part_rect[1], linewidth=1, edgecolor='b', facecolor='none')
            ax.add_patch(rect)
            doc_part_rects.append(part_rect)

        else:
            if largest_lower_rect:
                part_rect=largest_lower_rect
                rect = patches.Rectangle((part_rect[0], part_rect[1]), part_rect[2] - part_rect[0],
                                                                      part_rect[3] - part_rect[1], linewidth=1, edgecolor='b', facecolor='none')
                ax.add_patch(rect)
                doc_part_rects.append(part_rect)

            if largest_upper_rect:
                part_rect=largest_upper_rect
                rect = patches.Rectangle((part_rect[0], part_rect[1]), part_rect[2] - part_rect[0],
                                         part_rect[3] - part_rect[1], linewidth=1, edgecolor='b', facecolor='none')
                ax.add_patch(rect)
                doc_part_rects.append(part_rect)
        page_num += 1
    tabula.convert_into(fname, ".temp.", output_format="csv", pages='all')

    plt.axis([0, 700, 0, 900*num_pages])
    plt.show()
    return doc_text_boxes, doc_part_rects


# def split_column(text_boxes, part_rect, side_first=None):


def get_text(fname):
    doc_text_boxes, doc_part_rects=get_columns(fname)

    doc_text_boxes.sort(key=lambda element: element.bbox[0])
    doc_text_boxes.sort(key=lambda element: element.bbox[1], reverse=True)
    # for element in doc_text_boxes:
    #     print(element.bbox,"  ->  ",element.get_text())


    doc_part_rects.sort(key=lambda rect: rect[1], reverse=True)
    # for element in doc_part_rects:
    #     print(element)

    # side_first=None
    # lower_y=None
    # text_box_num=0
    # ordered_text_boxes=[]
    # # for part_rect in doc_part_rects:
    # #     while(True):
    # #         if doc_text_boxes[text_box_num].bbox[1]>=part_rect[1] and doc_text_boxes[text_box_num].bbox[3]<=part_rect[3]:
    # #             if doc
    # #     if not lower_y:
    # #         side_first=None

    ordered_text_boxes = []
    part_rect_num=0
    num_part_rects=len(doc_part_rects)
    left_column=[]
    right_column=[]

    for element in doc_text_boxes:
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

        if element.bbox[1]<doc_part_rects[part_rect_num][1] and num_part_rects>(part_rect_num+1):
            part_rect_num+=1
            right_column=[]
            left_column=[]

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

    new_ordered_text_boxes=[item for sublist in ordered_text_boxes for item in sublist]
    # new_ordered_text_boxes.sort(key=lambda element : element[])
    for element in new_ordered_text_boxes:
        print(element.get_text())

    print("----------------------------------------------------")








    # side_first=None
    # for key in doc_part_rects:
    #     doc_text_boxes[key].sort(key=lambda element : element.bbox[1], reverse=True)
    #     if len(doc_part_rects[key])==1:
    #         split_column(doc_text_boxes[key], doc_part_rects[key][0], side_first)
    #     doc_part_rects[key].sort(key=lambda rect : rect[1], reverse=True)





if __name__ == "__main__":
    fname='/home/jatin/iitb/flexiele/parser/dataset/samplecv/5 Sourabh.pdf'
    text = get_text(fname)
    fname='/home/jatin/iitb/flexiele/parser/dataset/samplecv/3 Bhirgu Sharma.pdf'
    text=get_text(fname)
    fname = '/home/jatin/iitb/flexiele/parser/dataset/samplecv/6 Sujeet.pdf'
    text = get_text(fname)
    fname = '/home/jatin/iitb/flexiele/parser/dataset/samplecv/iimjobs_Gaurav_Suman.pdf'
    text = get_text(fname)
    fname = '/home/jatin/iitb/flexiele/parser/dataset/samplecv/iimjobs_Swostik_Rout.pdf'
    text = get_text(fname)
    fname = '/home/jatin/iitb/flexiele/dataset/more/Copy of IIITN_AMAN_SONI_CV.pdf'
    text = get_text(fname)
    fname = '/home/jatin/iitb/flexiele/parser/dataset/samplecv/sdarunkataria@gmail.com.pdf'
    text = get_text(fname)


