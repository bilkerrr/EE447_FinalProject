import fitz
from keywords_process import keyword_process
from nltk.stem import SnowballStemmer
import json
import sys


# filepath: original pdf path
# refpath: reference pdf path
# filenumber: reference number
def highlight_pdf(j_input, refpath, filenumber):
    snowball_stemmer = SnowballStemmer('english')
    f = open(j_input, encoding='utf-8') #打开‘product.json’的json文件
    res = f.read()
    ref_dict = json.loads(res)
    f.close()
    doc = fitz.open(refpath)
    filenumber = str(filenumber)
    text_list = ref_dict[filenumber]
    new_text_list = []
    for text in text_list:
        text = text.split(" ")
        for t in text:
            new_text_list.append(snowball_stemmer.stem(t))
    text_list = new_text_list
    print(text_list)
    for page in doc:
        for text in text_list:
            if 'fi' in text:
                text = text.replace('fi', 'ﬁ')
            text_instances = page.searchFor(text)
        ### HIGHLIGHT
            for inst in text_instances:
                highlight = page.addHighlightAnnot(inst)

    doc.save("source/highlight.pdf", garbage=4, deflate=True, clean=True)


if __name__ == '__main__':
    highlight_pdf("dictionary.json", sys.argv[1], sys.argv[2])
    # highlight_pdf(r"dictionary.json", r"source/1.pdf", '1')
