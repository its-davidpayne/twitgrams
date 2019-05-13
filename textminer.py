##! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
THIS IS VERY FAR FROM FINISHED. VERY FAR FROM WORKING, TOO.
IT'S BARELY STARTED, OK?
"""
import re
import string

import os
import sys
import time

with open('frankenstein.txt', encoding='utf-8') as textreader:
    raw_text = textreader.read()
    # raw_text = raw_text.replace('\n', ' ').replace('\t',' ')
    print('All chars: ', len(raw_text))

remove_unwanted_chars = re.compile('[^a-zA-Z0-9\.?! ]', re.UNICODE)
simplify_whitespace = re.compile('[\n\t\v\f\r]', re.UNICODE)
unify_whitespace = re.compile('[ ]{2,}', re.UNICODE)
splitter = re.compile('([\w ]+[\.\?\!])')

cleaned_of_linefeeds = simplify_whitespace.sub(' ', raw_text)
cleaned_text = remove_unwanted_chars.sub('', cleaned_of_linefeeds)
further_cleaned = unify_whitespace.sub(' ', cleaned_text)
print('Cleaned text: ', len(further_cleaned))

sentences = splitter.split(further_cleaned)
#sentences = further_cleaned.strip().split('.')

new_sents = []

for sent in sentences:
    if not sent:
        continue
    elif sent.startswith(" "):
        new_sents.append(sent[1:])
    else:
        new_sents.append(sent)

sentences = new_sents

print('Num sentences: ', len(sentences))

print(sentences[:10])

file_name = f'data{os.sep}frankenstein_cleaned.txt'
with open(file_name, 'w') as textwriter:
    for senten in sentences:
        if senten:
            textwriter.write("%s\n" % senten)