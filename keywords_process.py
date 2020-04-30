from rake_nltk import Rake
import re
from nltk.corpus import stopwords
english_stopwords = stopwords.words("english")
english_stopwords.append("including")
english_stopwords.append("(")
english_stopwords.append(")")
# Uses stopwords for english from NLTK, and all puntuation characters by
# default
r = Rake()
file_path = r"example1.txt"
file = open(file_path, "r", encoding="utf-8")
texts = file.readlines()
offset = 100
file.close()
for text in texts:
    if 'ﬁ' in text:
        text = text.replace('ﬁ', 'fi')
    # Extraction given the text.
    r.extract_keywords_from_text(text)
    ref_dict = {}
    # Extraction given the list of strings where each string is a sentence.pip
    # r.extract_keywords_from_sentences(<list of sentences>)

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
            if ',' in tmp or '.' in tmp:
                for index in range(len(tmp)):
                    if tmp[index] == '[':
                        flag = 0
                    if tmp[index] == ']':
                        flag = 1
                    if flag and tmp[index] == ',' or tmp[index] == '.':
                        if index < pivot:
                            start = index
                        if index > pivot:
                            end = index
                            break
                tmp = tmp[start+1: end]
                numbers = tmp[tmp.index('[')+1: tmp.index(']')].split(', ')
                n = ' '.join(numbers)
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
                        n = ' '.join(numbers)
                        if n not in ref_dict:
                            ref_dict[n] = []
                        if tmp[i - 1] not in ref_dict[n]:
                            ref_dict[n].append(tmp[i - 1])

        except Exception:
            pass
    if len(ref_dict) >= 1:
        print(ref_dict)

    # print(new_ranked_phrases)

