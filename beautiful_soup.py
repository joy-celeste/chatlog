#!/usr/bin/python
# -*- coding: latin-1 -*-
import functools, operator, re, json, emoji, codecs
from pprint import pprint
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil import parser

print("opening the file...")
f = codecs.open("andrews-log-original.html", 'r', 'utf-8')

print("feeding into soup...")
soup = BeautifulSoup(f.read(), "html.parser")

print("finding all messages...")
messages = soup.find_all('div', {'class':"pam _3-95 _2pi0 _2lej uiBoxWhite noborder"})

def parse_reactions(reaction):
    result = []
    for r in reaction:
        split = emoji.get_emoji_regexp().split(r.get_text(strip=True))[1:]
        dict = {'reaction': split[0], 'actor': split[1]}
        result.append(dict)
        r.decompose()
    return result

def parse_content(r):
    for line in r:
        if line.find('ul'):
            line.find('ul').decompose()

    result = ''
    for line in r:
        temp = line.get_text(strip=True)
        if temp:
            result += temp

    return result

def parse_timestamp(s):
#    dt = datetime.strptime(s, '%b %d, %Y %I:%M%p')
    return s

def parse_html(messages):
    result = []
    count = 0
    total = len(messages)

    for m in messages:
        sender_name = m.find_all('div', {'class':"_3-96 _2pio _2lek _2lel"})[0].get_text()
        reactions = parse_reactions(m.find_all('li'))
        content = parse_content(m.find_all('div', {'class':"_3-96 _2let"}))
        timestamp = parse_timestamp(m.find_all('div', {'class':"_3-94 _2lem"})[0].get_text())

        dict = {"sender_name": sender_name,
                "timestamp": timestamp,
                "reactions": reactions,
                "content": content}
        result.append(dict)
        if count % 1000 == 0:
            print("processed {}%...".format(100*(count/float(total))))
        count += 1

    return result

with open('andrews_original_formatted.json', 'w') as outfile:
    print("saving to .json...")
    json.dump(parse_html(messages), outfile, \
        sort_keys=True, indent=2, separators=(',', ': '))

    print("successfully saved!")
