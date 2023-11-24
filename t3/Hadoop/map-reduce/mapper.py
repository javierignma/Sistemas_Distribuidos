#!/usr/bin/env python
# -*-coding:utf-8 -*
import sys
import re

for line in sys.stdin:
    docs = line.lower()
    arr = []

    for char in [",", ".", '"', "'", "(", ")", "\\", ";", ":", "$1", "$", "&"]:
        docs = docs.replace(char, '')
    tildes = {'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u', 'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U'}
    docs = ''.join(tildes.get(caracter, caracter) for caracter in docs)

    name, docs = docs.split('<splittername>')
    docs = re.sub(r'[^a-zA-ZñÑ0-9 ]', '', docs)

    for word in docs.split():
        arr.append('{}\t{}\t{}'.format(word, name, 1))

    for i in sorted(arr):
        print(i)