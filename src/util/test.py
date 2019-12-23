from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LTTextBoxHorizontal

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
    for element in layout:
        if isinstance(element, LTTextBoxHorizontal):
            # print(element.bbox[0], element.bbox[1], element.get_text().replace('\n', '----------').replace('\t', '****'))
            min_x=min(element.bbox[0], min_x)
            max_x=max(element.bbox[0], max_x)

            data.append({'x': element.bbox[0], 'y':element.bbox[1], 'text':element.get_text()})
            data_x.append(element.bbox[0])
            data_y.append(element.bbox[1])
            width=max_x-min_x

        for element in data:
            print(element)

    sorted_x=sorted(data, key=lambda dic: dic['x'])
    # print(sorted_x)
    # for element in sorted_x:
    #     print(element)

    import numpy as np
    import matplotlib.pyplot as pp

    # pp.plot(data_x, np.zeros_like(data_x), 'x')
    pp.plot(data_x, data_y, 'x')
    pp.show()

print("----------------------------------------")
print("----------------------------------------")
print("----------------------------------------")
print("----------------------------------------")

document = open('/home/jatin/iitb/flexiele/parser/dataset/samplecv/iimjobs_Gaurav_Suman.pdf', 'rb')

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
    for element in layout:
        if isinstance(element, LTTextBoxHorizontal):
            # print(element.bbox[0], element.bbox[1], element.get_text().replace('\n', '----------').replace('\t', '****'))
            min_x=min(element.bbox[0], min_x)
            max_x=max(element.bbox[0], max_x)

            data.append({'x': element.bbox[0], 'y':element.bbox[1], 'text':element.get_text()})
            data_x.append(element.bbox[0])
            data_y.append(element.bbox[1])
            width=max_x-min_x

    for element in data:
        print(element)

    sorted_x=sorted(data, key=lambda dic: dic['x'])
    # print(sorted_x)
    # for element in sorted_x:
    #     print(element)

    import numpy as np
    import matplotlib.pyplot as pp

    # pp.plot(data_x, np.zeros_like(data_x), 'x')
    pp.plot(data_x, data_y, 'x')
    pp.show()


print("----------------------------------------")
print("----------------------------------------")
print("----------------------------------------")
print("----------------------------------------")


document = open('/home/jatin/iitb/flexiele/parser/dataset/samplecv/iimjobs_Swostik_Rout.pdf', 'rb')

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
    for element in layout:
        if isinstance(element, LTTextBoxHorizontal):
            # print(element.bbox[0], element.bbox[1], element.get_text().replace('\n', '----------').replace('\t', '****'))
            min_x=min(element.bbox[0], min_x)
            max_x=max(element.bbox[0], max_x)

            data.append({'x': element.bbox[0], 'y':element.bbox[1], 'text':element.get_text()})
            data_x.append(element.bbox[0])
            data_y.append(element.bbox[1])
            width=max_x-min_x

    for element in data:
        print(element)

    sorted_x=sorted(data, key=lambda dic: dic['x'])
    # print(sorted_x)
    # for element in sorted_x:
    #     print(element)

    import numpy as np
    import matplotlib.pyplot as pp

    # pp.plot(data_x, np.zeros_like(data_x), 'x')
    pp.plot(data_x, data_y, 'x')
    pp.show()