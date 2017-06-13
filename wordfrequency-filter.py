#!/usr/bin/env python3

import pickle

pickle_file = "wordfrequency.pkl"

wordfrequency = pickle.load(open(pickle_file, 'rb'))
delete_keys = []

for key, val in wordfrequency.items():
    if val <= 1:
        delete_keys.append(key)

for key in delete_keys:
    wordfrequency.pop(key, None)

pickle.dump(dict(wordfrequency), open(pickle_file, 'wb'))
