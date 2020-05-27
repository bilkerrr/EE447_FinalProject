import importlib, sys
importlib.reload(sys)
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTFigure, LTImage
from pdfminer.converter import PDFPageAggregator
import re


# Open a PDF file.
def information_extract(filepath):
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
    text_content = []
    for page in PDFPage.create_pages(document):
        interpreter.process_page(page)
        layout = device.get_result()
        flag = 0
        for lt_obj in layout:
            if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
                text = lt_obj.get_text()
                text = text.replace('-\n', '')
                text = text.replace('ﬁ', 'fi')
                text = text.replace('“', '\'')
                text = text.replace('”', '\'')
                text = text.replace('–', '-')
                text = text.replace('\xb4', '')
                text_content.append(text)
                if flag == 1:
                    print(text.replace('\n', ' '))
                flag = 0
                if text.strip().lower() == "abstract":
                    flag = 1
            else:
                pass
    fp.close()

    total_text = ''.join(text_content).replace("\n", "")
    # 从字符串中解析出参考文献
    p = re.compile('\[\d+\][^\[\]]*\d\.')
    m = p.findall(total_text)
    for i in m:
        if i.startswith("[") and i[i.index(']') + 1] == ' ' and i[i.index(']') + 2].isupper():
            # print(i)
            # print(str(i))
            line = str(str(i).encode(encoding='UTF-8', errors='replace'))
            print(line[2:-1])
            idx = line[1:line.find(']')]
            arxiv_id = re.findall(r'\d{4}\.\d{5}', line)
            if len(arxiv_id) == 0:
                print("null")
            else:
                print("<a href=https://arxiv.org/pdf/"+arxiv_id[0]+".pdf download=./source/"+idx+".pdf><button class='download-btn'>Fetch Paper</button></a>")

if __name__ == '__main__':
    params = sys.argv[1]
    # information_extract(r'source/DARTS+.pdf')
    information_extract(params)
