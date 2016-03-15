#!/usr/bin/env python3.4
import os
import json
from bs4 import BeautifulSoup

def read_file(fn):
    with open(fn, "r") as f:
        return f.read()

pages = []
assets = {}
alph = []
for fn in sorted(os.listdir(".")):
    if not os.path.isdir(fn):
        continue
    body = os.path.join(fn, "body.html")
    head = os.path.join(fn, "head.html")
    style = os.path.join(fn, "style.css")

    p = {"num": int(fn.replace("page-", ""))}
    for k, name in (('body',body), ('head',head), ('style',style)):
        if os.path.isfile(name):
            p[k] = read_file(name)
    pages.append(p)
pages.sort(key=lambda x: x['num'])
for p in pages:
    del p['num']
# print(json.dumps(pages, indent=2))
removed = set()
for i,p in enumerate(pages):
    if 'body' in p and 'h2' in p['body']:
        soup = BeautifulSoup(p['body'], 'html.parser')
        name = soup.find('h2').get_text().strip()
        soup.find('p').string.replace_with('{}')
        soup.find('h2').string.replace_with('{}')
        soup.find('h1').string.replace_with('{}')
        p['body'] = soup.prettify()
        tpl_name = 'tpl_{}'.format(name.lower())
        fig_name = 'fig_{}'.format(name.lower())
        print(i, name)
        removed.add(i)
        removed.add(i-1)
        assets[tpl_name] = p
        assets[fig_name] = pages[i-1]
        alph.append((name, fig_name, tpl_name))

for i,p in enumerate(pages):
    if i not in removed:
        assets['page_{}'.format(i+1)] = p
        print(i, json.dumps(p, indent=2))

with open("assets.json", "w") as f:
    json.dump(assets, f, indent=2, sort_keys=True)
with open("alph_en.json", "w") as f:
    json.dump(alph, f, indent=2, sort_keys=True)
