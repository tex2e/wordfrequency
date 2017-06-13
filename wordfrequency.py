#!/usr/bin/env python3
#
# wordfrequency
#
# subcommands
#   - create       : Create word frequency table.
#   - info <word>  : Show frequency of given word.
#   - read <file>
#

import sys
import argparse
import signal
import os
import re
import pickle
from pprint import pprint

# ------------------------------------------------------------------------------
# Arguments

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest='subcommand')
create_parser = subparsers.add_parser('create')
append_parser = subparsers.add_parser('append')
append_parser.add_argument('src_dir')
info_parser = subparsers.add_parser('info')
info_parser.add_argument('word')
read_parser = subparsers.add_parser('read')
read_parser.add_argument('file')
args = parser.parse_args()

if not args.subcommand:
    parser.print_usage()
    sys.exit()

# ------------------------------------------------------------------------------
# Signal

def signal_handler(signal, frame):
    print('exit.')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# ------------------------------------------------------------------------------
# Main

pickle_file = "wordfrequency.pkl"

if args.subcommand in ('create', 'append'):
    from collections import defaultdict
    from nltk.corpus import wordnet
    import glob

    subcommand = args.subcommand

    if subcommand == 'create':
        os.remove(pickle_file)
        src_dir = '*'
    else:
        src_dir = args.src_dir

    filepath = "extracted/{}/*_??.token".format(src_dir)

    if os.path.isfile(pickle_file):
        frequency = defaultdict(int, pickle.load(open(pickle_file, 'rb')))
    else:
        frequency = defaultdict(int)

    def count_word(frequency, filename):
        with open(filename) as f:
            for word in f.readlines():
                word = word.strip()
                word = wordnet.morphy(word) or word
                frequency[word] += 1

    for wiki_article_file in glob.iglob(filepath):
        print("INFO: {}".format(wiki_article_file))
        count_word(frequency, wiki_article_file)

    pickle.dump(dict(frequency), open(pickle_file, 'wb'))

if args.subcommand == 'info':
    from nltk.corpus import wordnet

    word = args.word.lower()
    word = wordnet.morphy(word) or word
    wordfrequency = pickle.load(open(pickle_file, 'rb'))
    print("{}: {}".format(word, wordfrequency.get(word, 0)))

if args.subcommand == 'read':
    from nltk import word_tokenize
    from nltk.corpus import wordnet

    filepath = args.file
    wordfrequency = pickle.load(open(pickle_file, 'rb'))

    with open(filepath) as f:
        for line in f.readlines():
            for word in word_tokenize(line):
                if re.match(r'^[a-zA-Z]+$', word):
                    pass
                elif word == '.':
                    sys.stdout.write(".\n")
                    continue
                else:
                    sys.stdout.write(" {}".format(word))
                    continue

                word = word.lower()
                word = wordnet.morphy(word) or word
                this_word_frequency = wordfrequency.get(word, 0)
                if this_word_frequency < 10000:
                    sys.stdout.write(" <\033[31m{}\033[0m:{}>".format(word, this_word_frequency))
                else:
                    sys.stdout.write(" {}".format(word))
