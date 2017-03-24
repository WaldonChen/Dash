#!/usr/bin/env python

import sys
import os
import re
import sqlite3
from bs4 import BeautifulSoup

if len(sys.argv) < 2:
    print "Usage: %s <docset_dir>" % (sys.argv[0])
    sys.exit(1)

resdir = os.path.join(sys.argv[1], 'Contents/Resources')
docpath = os.path.join(resdir, 'Documents')
if not os.path.exists(docpath):
    os.makedirs(docpath)

conn = sqlite3.connect(os.path.join(resdir, 'docSet.dsidx'))
cur = conn.cursor()

try:
    cur.execute('DROP TABLE searchIndex;')
except:
    pass

cur.execute('CREATE TABLE searchIndex(id INTEGER PRIMARY KEY, name TEXT, '
            'type TEXT, path TEXT);')
cur.execute('CREATE UNIQUE INDEX anchor ON searchIndex (name, type, path);')

page = open(os.path.join(docpath, 'Name-Index.html')).read()
soup = BeautifulSoup(page, 'lxml')
links = soup.find('table', class_='index-fn').find_all('a')

contains_var = re.compile(r'variable', re.IGNORECASE)
contains_func = re.compile(r'function', re.IGNORECASE)
contains_macro = re.compile(r'if|else|def', re.IGNORECASE)
contains_dire = re.compile(r'directive|search', re.IGNORECASE)
contains_target = re.compile(r'target', re.IGNORECASE)

for tag in links:
    if tag.code:
        name = tag.code.text.strip()
        path = tag.attrs['href'].strip()
        type = 'Entry'
        if contains_var.search(path):
            type = 'Variable'
        elif contains_func.search(path):
            type = 'Function'
        elif contains_dire.search(path):
            type = 'Directive'
        elif contains_target.search(path):
            type = 'Global'
        if contains_macro.search(name):
            type = 'Macro'
        cur.execute('INSERT OR IGNORE INTO searchIndex(name, type, path)'
                    ' VALUES (?,?,?)', (name, type, path))
        # print 'name: %s, path: %s' % (name, path)

page = open(os.path.join(docpath, 'index.html')).read()
soup = BeautifulSoup(page, 'lxml')
links = soup.find('table', class_='menu').find_all('a')

for tag in links:
    name = tag.text.strip()
    path = tag.attrs['href'].strip()
    cur.execute('INSERT OR IGNORE INTO searchIndex(name, type, path)'
                ' VALUES (?,?,?)', (name, 'Guide', path))
    # print 'name: %s, path: %s' % (name, path)

conn.commit()
conn.close()
