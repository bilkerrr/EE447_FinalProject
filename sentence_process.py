from nltk.tokenize import sent_tokenize

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
fp = open('DARTS+.pdf', 'rb')
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
    for lt_obj in layout:
        if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
            sentences = sent_tokenize(lt_obj.get_text())
            for sentence in sentences:
                if "[" in sentence and "]" in sentence:
                    print(sentence.replace('\n', ' '))
                    with open("example1.txt", "a", encoding="utf-8") as f:
                        if '-\n' in sentence:
                            sentence = sentence.replace('-\n', '')
                        f.write(sentence.replace('\n', ' '))
                        f.write("\n")

        else:
            pass


