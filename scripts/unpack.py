#!/usr/bin/env python3.4
import argparse
import json
import os

def parse_arguments():
    parser = argparse.ArgumentParser(description='Unpack book')
    parser.add_argument('-o', '--output', dest='output',
        help='output directory', default='.')
    parser.add_argument('-l', '--language', dest='language',
        help='language (en, pl)', default='en')
    parser.add_argument('--upper', dest='upper', action='store_true')

    args = parser.parse_args()
    return args

def load_json(fn):
    with open(fn, "r") as f:
        return json.load(f)


def ensure_dir(f):
    # from http://stackoverflow.com/questions/273192/python-best-way-to-create-directory-if-it-doesnt-exist-for-file-write
    d = os.path.dirname(f)
    if d!='' and not os.path.exists(d):
        os.makedirs(d)


def write_file(fn, contents):
    ensure_dir(fn)
    with open(fn, "w") as f:
        f.write(contents)


class PageGenerator(object):

    def __init__(self, output_dir="."):
        self.counter = 0
        self.output_dir = output_dir
        ensure_dir(output_dir)

    def add_page(self, p):
        self.counter += 1
        dest_dir = os.path.join(self.output_dir, "page-{}".format(self.counter))
        for k, name in [('body', 'body.html'), ('head', 'head.html'), ('style','style.css')]:
            if k in p:
                fn = os.path.join(dest_dir, name)
                write_file(fn, p[k])

def main():
    args = parse_arguments()

    assets = load_json("assets.json")
    if args.language=='pl':
        alph = load_json("alph_pl.json")
        FOR_WORD = "jak"
    else:
        alph = load_json("alph_en.json")
        FOR_WORD = "for"

    g = PageGenerator(args.output)

    g.add_page(assets['page_1'])
    g.add_page(assets['page_2'])
    g.add_page(assets['page_3'])

    for word, fig, tpl in alph:
        g.add_page(assets[fig])
        p = assets[tpl]
        letter = word.upper()[0]
        if args.upper:
            word = word.upper()
        new_p = p.copy()
        new_p['body'] = p['body'].format(letter, FOR_WORD, word)
        g.add_page(new_p)

    g.add_page(assets['page_56'])
    g.add_page(assets['page_57'])
    g.add_page(assets['page_58'])



if __name__ == '__main__':
    main()

