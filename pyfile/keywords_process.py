from rake_nltk import Rake
import re
from nltk.corpus import stopwords
import importlib, sys
importlib.reload(sys)
from sentence_process import sentence_process
import json


def keyword_process(filepath):
    english_stopwords = stopwords.words("english")
    english_stopwords.append("including")
    english_stopwords.append("(")
    english_stopwords.append(")")
    # Uses stopwords for english from NLTK, and all puntuation characters by
    # default
    r = Rake()
    texts = sentence_process(filepath)
    offset = 100
    ref_dict = {}
    for text in texts:
        if 'ﬁ' in text:
            text = text.replace('ﬁ', 'fi')
        # Extraction given the text.
        r.extract_keywords_from_text(text)

        # To get keyword phrases ranked highest to lowest.
        ranked_phrases = r.get_ranked_phrases()
        new_ranked_phrases = []

        for i in ranked_phrases:
            cop = re.compile('[^A-Z^a-z^-]')
            ii = cop.sub(' ', i).lstrip().split(' ')
            new_i = []
            lower_text = text.lower()
            for word in ii:
                if word not in english_stopwords:
                    new_i.append(word)
            i = ' '.join(new_i).strip()
            if len(i) > 1:
                new_ranked_phrases.append(i)
            try:
                pivot = lower_text.index(i)
                if (pivot - offset) < 0:
                    start = 0
                else:
                    start = pivot - offset
                if (pivot + offset) >= len(lower_text):
                    end = len(lower_text) - 1
                else:
                    end = pivot + offset
                tmp = lower_text[start: end]
                pivot = tmp.index(i)
                flag = 1
                flag2 = 0
                if ',' in tmp or '.' in tmp:
                    for index in range(len(tmp)):
                        if tmp[index] == '[':
                            flag = 0
                        if tmp[index] == ']':
                            flag = 1
                        if tmp[index] == i:
                            flag2 = 1
                        if flag and tmp[index] == ',' or tmp[index] == '.'and flag2:
                            if index < pivot:
                                start = index
                            if index > pivot:
                                end = index
                                break
                    tmp = tmp[start+1: end]
                    numbers = tmp[tmp.index('[')+1: tmp.index(']')].split(', ')
                    for n in numbers:
                        new_n = []
                        for nn in n:
                            if nn.isdigit():
                                new_n.append(nn)
                        n = int(''.join(new_n))
                        if n not in ref_dict:
                            ref_dict[n] = []
                        if i != '':
                            if i not in ref_dict[n]:
                                ref_dict[n].append(i)
                else:
                    tmp = text.split(' ')
                    for i in range(len(tmp)):
                        if tmp[i][0] == '[' and i > 1:
                            numbers = tmp[i][1:-1].strip(']').split(', ')
                            for n in numbers:
                                new_n = []
                                for nn in n:
                                    if nn.isdigit():
                                        new_n.append(nn)
                                n = int(''.join(new_n))
                                if n not in ref_dict:
                                    ref_dict[n] = []
                                if tmp[i - 1] not in ref_dict[n]:
                                    ref_dict[n].append(tmp[i - 1])
            except Exception:
                pass
    myfile = open('dictionary.json', 'w+')
    json.dump(ref_dict, myfile)
    myfile.close()
    print(ref_dict)
    return ref_dict
    # print(new_ranked_phrases)


if __name__ == '__main__':
    # params = sys.argv[1]
    # keyword_process(params)
    keyword_process("C:/xampp/htdocs/source/DARTS+.pdf")
