import importlib, sys
importlib.reload(sys)
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTFigure, LTImage
from pdfminer.converter import PDFPageAggregator
import re

# Open a PDF file.
filename = "DARTS+"
fp = open(filename+'.pdf', 'rb')
# Create a PDF parser object associated with the file object.
parser = PDFParser(fp)
# Create a PDF document object that stores the document structure.
# Supply the password for initialization.
rsrcmgr = PDFResourceManager()
laparams = LAParams()
device = PDFPageAggregator(rsrcmgr, laparams=laparams)
interpreter = PDFPageInterpreter(rsrcmgr, device)
document = PDFDocument(parser)
# Process each page contained in the document.
text_content = []
for page in PDFPage.create_pages(document):
    interpreter.process_page(page)
    layout = device.get_result()
    flag = 0
    for lt_obj in layout:
        if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
            text = lt_obj.get_text()
            if flag == 1:
                with open(filename+"_abstract.txt", "a", encoding='utf-8') as f:
                    text.replace('-\n', '')
                    text = text.replace('ﬁ', 'fi')
                    f.write(text.replace('\n', ' ')+'\n')
            flag = 0
            if text.strip().lower() == "abstract":
                flag = 1

        else:
            pass
fp.close()