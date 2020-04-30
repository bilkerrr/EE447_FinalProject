import re
import requests

ref_file = open(r"DART+.txt", "r", encoding="utf-8")
dic = {}
for line in ref_file.readlines():
    idx = line[1:line.find(']')]
    arXiv_id = re.findall(r'\d{4}\.\d{5}', line)
    if len(arXiv_id) == 0:
        continue
    arXiv_id = arXiv_id[0]
    dic[arXiv_id] = idx

ref_file.close()

print(dic)

for arXiv_id, idx in dic.items():
    path = arXiv_id + ".pdf"
    foo = idx+".pdf"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36"
    }
    response = requests.get("https://arxiv.org/pdf/" + path, headers=headers)
    print(response.text)
    with open(foo, "wb") as f:
        f.write(response.content)
    f.close()

