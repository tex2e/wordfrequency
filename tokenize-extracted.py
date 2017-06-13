#!/usr/bin/env python3

import signal
import sys
import re
from collections import defaultdict, deque
from nltk import word_tokenize, pos_tag
import glob
import pickle
from pprint import pprint
import argparse
from itertools import zip_longest
from multiprocessing import Process
import time

parser = argparse.ArgumentParser()
parser.add_argument('directory')
args = parser.parse_args()

def grouper(n, iterable, fillvalue=None):
    "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(fillvalue=fillvalue, *args)

# NN: noun, common, singular or mass
# JJ: adjective or numeral, ordinal
# RB: adverb
# VB: verb, base form
# RP: particle
# WDT: WH-determiner
# WP: WH-pronoun
# WRB: Wh-adverb

def analyze(filename_src, filename_dest):
    with open(filename_src) as f_src, open(filename_dest, "w") as f_dest:
        for line in f_src.readlines():
            if re.match(r'^</?doc', line):
                continue
            for word in word_tokenize(line):
                if re.match(r'^[-a-zA-Z]+$', word):
                    f_dest.write(word.lower() + "\n")
    print("INFO: {} -> {}".format(filename_src, filename_dest))

filepath = "extracted/*/*_??"
if args.directory:
    directory = args.directory
    filepath = "extracted/{}/*_??".format(directory)

for i, (f1, f2, f3, f4) in enumerate(grouper(4, glob.iglob(filepath)), start=1):
    f1_dest = f1 + ".token"
    t1 = Process(target=analyze, args=(f1, f1_dest), daemon=True)
    t1.start()
    if f2:
        f2_dest = f2 + ".token"
        t2 = Process(target=analyze, args=(f2, f2_dest), daemon=True)
        t2.start()
    if f3:
        f3_dest = f3 + ".token"
        t3 = Process(target=analyze, args=(f3, f3_dest), daemon=True)
        t3.start()
    if f4:
        f4_dest = f4 + ".token"
        t4 = Process(target=analyze, args=(f4, f4_dest), daemon=True)
        t4.start()

    t1.join()
    t2.join()
    t3.join()
    t4.join()
    if i % 30 == 0:
        time.sleep(15)
