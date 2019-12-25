from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LTTextBoxHorizontal, LTCurve, LTLine,LTRect
import numpy as np

document = open('/home/jatin/iitb/flexiele/parser/dataset/samplecv/5 Sourabh.pdf', 'rb')

#Create resource manager
rsrcmgr = PDFResourceManager()

# Set parameters for analysis.
laparams = LAParams()

# Create a PDF page aggregator object.
device = PDFPageAggregator(rsrcmgr, laparams=laparams)

interpreter = PDFPageInterpreter(rsrcmgr, device)
for page in PDFPage.get_pages(document):
    interpreter.process_page(page)
# receive the LTPage object for the page.
    data=[]
    data_x=[]
    data_y=[]
    layout = device.get_result()
    min_x=10000
    max_x=0

    import matplotlib.pyplot as plt
    import matplotlib.patches as patches

    # Create figure and axes
    fig, ax = plt.subplots(1)
    plt.axis([0, 700, 0, 1000])





    for element in layout:
        if isinstance(element, LTTextBoxHorizontal):
            # print(element.bbox[0], element.bbox[1], element.get_text().replace('\n', '----------').replace('\t', '****'))
            min_x=min(element.bbox[0], min_x)
            max_x=max(element.bbox[0], max_x)

            data.append({'x0': element.bbox[0], 'y0':element.bbox[1], 'text':element.get_text()})
            # print(element.bbox)
            # print(element.get_text())
            # print("------------------------------------------------")
            data_x.append(element.bbox[0])
            data_y.append(element.bbox[1])
            width=max_x-min_x

            # Create a Rectangle patch
            # rect = patches.Rectangle((element.bbox[0], element.bbox[1]), element.bbox[2]-element.bbox[0], element.bbox[3]-element.bbox[1], linewidth=1, edgecolor='r', facecolor='none')
            rect = patches.Rectangle((element.bbox[0], element.bbox[1]), element.bbox[2]-element.bbox[0], element.bbox[3]-element.bbox[1], linewidth=1, edgecolor='r', facecolor='none')

            # Add the patch to the Axes
            ax.add_patch(rect)

        # for element in data:
        #     print(element)

    # sorted_x=sorted(data, key=lambda dic: dic['x0'])
    # print(sorted_x)
    # for element in sorted_x:
    #     print(element)

    plt.show()

print("----------------------------------------")
print("----------------------------------------")
print("----------------------------------------")
print("----------------------------------------")

document = open('/home/jatin/iitb/flexiele/parser/dataset/samplecv/iimjobs_Gaurav_Suman.pdf', 'rb')
#
#Create resource manager
rsrcmgr = PDFResourceManager()

# Set parameters for analysis.
laparams = LAParams()

# Create a PDF page aggregator object.
device = PDFPageAggregator(rsrcmgr, laparams=laparams)

interpreter = PDFPageInterpreter(rsrcmgr, device)
for page in PDFPage.get_pages(document):
    interpreter.process_page(page)
# receive the LTPage object for the page.
    data=[]
    data_x=[]
    data_y=[]
    layout = device.get_result()
    min_x=10000
    max_x=0

    import matplotlib.pyplot as plt
    import matplotlib.patches as patches

    # Create figure and axes
    fig, ax = plt.subplots(1)
    plt.axis([0, 700, 0, 1000])





    for element in layout:
        if isinstance(element, LTTextBoxHorizontal):
            # print(element.bbox[0], element.bbox[1], element.get_text().replace('\n', '----------').replace('\t', '****'))
            min_x=min(element.bbox[0], min_x)
            max_x=max(element.bbox[0], max_x)

            data.append({'x0': element.bbox[0], 'y0':element.bbox[1], 'text':element.get_text()})
            # print(element.bbox)
            # print(element.get_text())
            # print("------------------------------------------------")
            data_x.append(element.bbox[0])
            data_y.append(element.bbox[1])
            width=max_x-min_x

            # Create a Rectangle patch
            # rect = patches.Rectangle((element.bbox[0], element.bbox[1]), element.bbox[2]-element.bbox[0], element.bbox[3]-element.bbox[1], linewidth=1, edgecolor='r', facecolor='none')
            rect = patches.Rectangle((element.bbox[0], element.bbox[1]), element.bbox[2]-element.bbox[0], element.bbox[3]-element.bbox[1], linewidth=1, edgecolor='r', facecolor='none')

            # Add the patch to the Axes
            ax.add_patch(rect)

        # for element in data:
        #     print(element)

    # sorted_x=sorted(data, key=lambda dic: dic['x0'])
    # print(sorted_x)
    # for element in sorted_x:
    #     print(element)

    plt.show()
#
#
# print("----------------------------------------")
# print("----------------------------------------")
# print("----------------------------------------")
# print("----------------------------------------")


document = open('/home/jatin/iitb/flexiele/parser/dataset/samplecv/iimjobs_Swostik_Rout.pdf', 'rb')
#
#Create resource manager
rsrcmgr = PDFResourceManager()

# Set parameters for analysis.
laparams = LAParams()

# Create a PDF page aggregator object.
device = PDFPageAggregator(rsrcmgr, laparams=laparams)

interpreter = PDFPageInterpreter(rsrcmgr, device)
for page in PDFPage.get_pages(document):
    interpreter.process_page(page)
# receive the LTPage object for the page.
    data=[]
    data_x=[]
    data_y=[]
    layout = device.get_result()
    min_x=10000
    max_x=0

    import matplotlib.pyplot as plt
    import matplotlib.patches as patches

    # Create figure and axes
    fig, ax = plt.subplots(1)
    plt.axis([0, 700, 0, 1000])





    for element in layout:
        if isinstance(element, LTTextBoxHorizontal):
            # print(element.bbox[0], element.bbox[1], element.get_text().replace('\n', '----------').replace('\t', '****'))
            min_x=min(element.bbox[0], min_x)
            max_x=max(element.bbox[0], max_x)

            data.append({'x0': element.bbox[0], 'y0':element.bbox[1], 'text':element.get_text()})
            # print(element.bbox)
            # print(element.get_text())
            # print("------------------------------------------------")
            data_x.append(element.bbox[0])
            data_y.append(element.bbox[1])
            width=max_x-min_x

            # Create a Rectangle patch
            # rect = patches.Rectangle((element.bbox[0], element.bbox[1]), element.bbox[2]-element.bbox[0], element.bbox[3]-element.bbox[1], linewidth=1, edgecolor='r', facecolor='none')
            rect = patches.Rectangle((element.bbox[0], element.bbox[1]), element.bbox[2]-element.bbox[0], element.bbox[3]-element.bbox[1], linewidth=1, edgecolor='r', facecolor='none')

            # Add the patch to the Axes
            ax.add_patch(rect)

        # for element in data:
        #     print(element)

    # sorted_x=sorted(data, key=lambda dic: dic['x0'])
    # print(sorted_x)
    # for element in sorted_x:
    #     print(element)

    plt.show()



# print("----------------------------------------")
# print("----------------------------------------")
# print("----------------------------------------")
# print("----------------------------------------")
#
#
document = open('/home/jatin/iitb/flexiele/parser/dataset/samplecv/3 Bhirgu Sharma.pdf', 'rb')
#
#Create resource manager
rsrcmgr = PDFResourceManager()

# Set parameters for analysis.
laparams = LAParams()

# Create a PDF page aggregator object.
device = PDFPageAggregator(rsrcmgr, laparams=laparams)

interpreter = PDFPageInterpreter(rsrcmgr, device)
for page in PDFPage.get_pages(document):
    interpreter.process_page(page)
# receive the LTPage object for the page.
    data=[]
    data_x=[]
    data_y=[]
    layout = device.get_result()
    min_x=10000
    max_x=0

    import matplotlib.pyplot as plt
    import matplotlib.patches as patches

    # Create figure and axes
    fig, ax = plt.subplots(1)
    plt.axis([0, 700, 0, 1000])





    for element in layout:
        if isinstance(element, LTTextBoxHorizontal):
            # print(element.bbox[0], element.bbox[1], element.get_text().replace('\n', '----------').replace('\t', '****'))
            min_x=min(element.bbox[0], min_x)
            max_x=max(element.bbox[0], max_x)

            data.append({'x0': element.bbox[0], 'y0':element.bbox[1], 'text':element.get_text()})
            # print(element.bbox)
            # print(element.get_text())
            # print("------------------------------------------------")
            data_x.append(element.bbox[0])
            data_y.append(element.bbox[1])
            width=max_x-min_x

            # Create a Rectangle patch
            # rect = patches.Rectangle((element.bbox[0], element.bbox[1]), element.bbox[2]-element.bbox[0], element.bbox[3]-element.bbox[1], linewidth=1, edgecolor='r', facecolor='none')
            rect = patches.Rectangle((element.bbox[0], element.bbox[1]), element.bbox[2]-element.bbox[0], element.bbox[3]-element.bbox[1], linewidth=1, edgecolor='r', facecolor='none')

            # Add the patch to the Axes
            ax.add_patch(rect)

        # for element in data:
        #     print(element)

    # sorted_x=sorted(data, key=lambda dic: dic['x0'])
    # print(sorted_x)
    # for element in sorted_x:
    #     print(element)

    plt.show()
#
#
print("----------------------------------------")
print("----------------------------------------")
print("----------------------------------------")
print("----------------------------------------")


document = open('/home/jatin/iitb/flexiele/parser/dataset/samplecv/6 Sujeet.pdf', 'rb')
#
#Create resource manager
rsrcmgr = PDFResourceManager()

# Set parameters for analysis.
laparams = LAParams()

# Create a PDF page aggregator object.
device = PDFPageAggregator(rsrcmgr, laparams=laparams)

interpreter = PDFPageInterpreter(rsrcmgr, device)
for page in PDFPage.get_pages(document):
    interpreter.process_page(page)
# receive the LTPage object for the page.
    data=[]
    data_x=[]
    data_y=[]
    layout = device.get_result()
    min_x=10000
    max_x=0

    import matplotlib.pyplot as plt
    import matplotlib.patches as patches

    # Create figure and axes
    fig, ax = plt.subplots(1)
    plt.axis([0, 700, 0, 1000])





    for element in layout:
        if isinstance(element, LTTextBoxHorizontal):
            # print(element.bbox[0], element.bbox[1], element.get_text().replace('\n', '----------').replace('\t', '****'))
            min_x=min(element.bbox[0], min_x)
            max_x=max(element.bbox[0], max_x)

            data.append({'x0': element.bbox[0], 'y0':element.bbox[1], 'text':element.get_text()})
            # print(element.bbox)
            # print(element.get_text())
            # print("------------------------------------------------")
            data_x.append(element.bbox[0])
            data_y.append(element.bbox[1])
            width=max_x-min_x

            # Create a Rectangle patch
            # rect = patches.Rectangle((element.bbox[0], element.bbox[1]), element.bbox[2]-element.bbox[0], element.bbox[3]-element.bbox[1], linewidth=1, edgecolor='r', facecolor='none')
            rect = patches.Rectangle((element.bbox[0], element.bbox[1]), element.bbox[2]-element.bbox[0], element.bbox[3]-element.bbox[1], linewidth=1, edgecolor='r', facecolor='none')

            # Add the patch to the Axes
            ax.add_patch(rect)

        # for element in data:
        #     print(element)

    # sorted_x=sorted(data, key=lambda dic: dic['x0'])
    # print(sorted_x)
    # for element in sorted_x:
    #     print(element)

    plt.show()


document = open('/home/jatin/iitb/flexiele/parser/dataset/samplecv/aksingh1493@gmail.com.pdf', 'rb')
#
#Create resource manager
rsrcmgr = PDFResourceManager()

# Set parameters for analysis.
laparams = LAParams()

# Create a PDF page aggregator object.
device = PDFPageAggregator(rsrcmgr, laparams=laparams)

interpreter = PDFPageInterpreter(rsrcmgr, device)
for page in PDFPage.get_pages(document):
    interpreter.process_page(page)
# receive the LTPage object for the page.
    data=[]
    data_x=[]
    data_y=[]
    layout = device.get_result()
    min_x=10000
    max_x=0

    import matplotlib.pyplot as plt
    import matplotlib.patches as patches

    # Create figure and axes
    fig, ax = plt.subplots(1)
    plt.axis([0, 700, 0, 1000])





    for element in layout:
        if isinstance(element, LTTextBoxHorizontal):
            # print(element.bbox[0], element.bbox[1], element.get_text().replace('\n', '----------').replace('\t', '****'))
            min_x=min(element.bbox[0], min_x)
            max_x=max(element.bbox[0], max_x)

            data.append({'x0': element.bbox[0], 'y0':element.bbox[1], 'text':element.get_text()})
            # print(element.bbox)
            # print(element.get_text())
            # print("------------------------------------------------")
            data_x.append(element.bbox[0])
            data_y.append(element.bbox[1])
            width=max_x-min_x

            # Create a Rectangle patch
            # rect = patches.Rectangle((element.bbox[0], element.bbox[1]), element.bbox[2]-element.bbox[0], element.bbox[3]-element.bbox[1], linewidth=1, edgecolor='r', facecolor='none')
            rect = patches.Rectangle((element.bbox[0], element.bbox[1]), element.bbox[2]-element.bbox[0], element.bbox[3]-element.bbox[1], linewidth=1, edgecolor='r', facecolor='none')

            # Add the patch to the Axes
            ax.add_patch(rect)

        # for element in data:
        #     print(element)

    # sorted_x=sorted(data, key=lambda dic: dic['x0'])
    # print(sorted_x)
    # for element in sorted_x:
    #     print(element)

    plt.show()
