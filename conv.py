import json

url_dict = {}
with open('url_dictionary.txt', 'r', encoding='utf-8') as f:
    while True:
        try:
            l, r = f.readline().split(', ')
        except:
            break
        url = f.readline()
        if not l or not r or not url:
            break
        r = r.replace('\n', '')
        if r not in url_dict.keys():
            url_dict[r] = {}
        url_dict[r][l] = url

with open('url_dictionary.json', 'w', encoding='utf-8') as f:
    json.dump(url_dict, f, ensure_ascii=False, indent=4)
