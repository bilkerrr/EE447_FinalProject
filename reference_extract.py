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
            text_content.append(lt_obj.get_text())
            with open("DARTS+_content.txt", "a", encoding='utf-8') as f:
                f.write(lt_obj.get_text()+'\n')
        else:
            pass

# text_content 中每一个元素存储了一行文字
total_text = ''.join(text_content).replace("\n", "")
#从字符串中解析出参考文献
file = open("DARTS+_ref.txt","w", encoding="utf-8")
p = re.compile('\[\d+\][^\[\]]*\d\.')
m = p.findall(total_text)
for i in m:
    if i.startswith("[") and i[i.index(']')+1] == ' ' and i[i.index(']')+2].isupper():
        # print(i)
        file.write(str(i))
        file.write("\n")
file.close()