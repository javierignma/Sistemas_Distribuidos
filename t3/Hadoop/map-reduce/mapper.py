#!/usr/bin/env python
# -*-coding:utf-8 -*
import sys


for line in sys.stdin:
    docs = line.lower()
    arr = []

    for char in [",", ".", '"', "'", "(", ")", "\\", ";", ":", "$1", "$", "&"]:
        docs = docs.replace(char, '')

    name, docs = docs.split('<splittername>')
    
    for word in docs.split():
        arr.append('{}\t{}\t{}'.format(word, name, 1))

    for i in sorted(arr):
        print(i)