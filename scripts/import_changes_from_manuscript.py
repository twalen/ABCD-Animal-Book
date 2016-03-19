#!/usr/bin/env python3.4
import os
import json
from bs4 import BeautifulSoup

with open("assets.json", "r") as f:
    assets = json.load(f)

def read_file(fn):
    with open(fn, "r") as f:
        return f.read()

for name,page,elem in [('page_1',1,'style'), ('page_57',41,'body'), ('page_57',41,'style')]:
    if elem=='style':
       fn = 'style.css'
    elif elem=='body':
       fn = 'body.html'
    else:
       raise Exception("aaa")
    full_fn = os.path.join("..", "manuscript", "page-{}".format(page), fn)
    assets[name][elem] = read_file(full_fn)

with open("assets.json", "w") as f:
    json.dump(assets, f, indent=2, sort_keys=True)
