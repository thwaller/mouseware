#!/usr/bin/env python

import json
import fileinput
import glob
from os.path import splitext, basename

import markov


def build_wordlist():
    words = {}

    src = "txt/*"
    dest = "js/wordlist.js"

    for file in glob.glob(src):
        with open(file, 'r') as f:
            place = splitext(basename(file))[0]
            # using list(set( words )) unique-ifies the words
            words[place] = list(set([i.strip() for i in f]))

    with open(dest, 'w') as f:
        f.write("var words = ")
        json.dump(words, f)
        f.write(";")


def build_markovchain():
    src = "markov_corpus/*"
    dest = "js/markovchain.js"

    with fileinput.input(files=glob.glob(src)) as f:
        corpus = markov.get_ngrams(3, f)

    chain = markov.PassphraseMarkovChain(corpus)
    print(chain.to_json())


if __name__ == "__main__":
    build_wordlist()
    build_markovchain()
