#!/usr/bin/env python
# -*-coding:utf-8 -*

import sys

current_word = None
current_count = 0
word = None

doc_count = {}
for line in sys.stdin:
    # print(line.replace("\n","").replace("\t",","))
    result = line.replace("\n","").split('\t')

    if result[0] in doc_count.keys():
        if result[1] in doc_count[result[0]].keys():
            doc_count[result[0]][result[1]] += 1
        else:
            doc_count[result[0]][result[1]] = 1
    else:
        doc_count[result[0]] = {result[1]: 1}

print('Word\t[ (Document1, Count1), ... ]')
for key,counts in doc_count.items():
    value = ""
    for doc,count in counts.items():
        value += "({}, {}) ".format(doc, count)
    print("{}\t{}".format(key, value))