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


def sentence_process(filepath):
    # Open a PDF file.
    fp = open(filepath, 'rb')
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
    para = []
    for page in PDFPage.create_pages(document):
        interpreter.process_page(page)
        layout = device.get_result()
        for lt_obj in layout:
            if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
                sentences = sent_tokenize(lt_obj.get_text())
                for sentence in sentences:
                    if "[" in sentence and "]" in sentence:
                        sentence = sentence.replace('-\n', '')
                        sentence = sentence.replace('ﬁ', 'fi')
                        sentence = sentence.replace('“', '\'')
                        sentence = sentence.replace('”', '\'')
                        sentence = sentence.replace('–', '-')
                        para.append(sentence)

            else:
                pass
    return para


