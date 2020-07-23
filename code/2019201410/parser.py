#!/usr/bin/env python3
# coding = utf-8
from html.parser import HTMLParser
import os
import os.path
import re
import sys
import codecs

outfile = open('corpus.txt', 'w')
namelistFile = open('namelist.txt', 'w')

class MyHTMLParser(HTMLParser):
	def handle_data(self, data):
		if self.lasttag == 'title':
			namelist.write(data + '\n')
			for i in range(0, 5)
				outfile.write(data)
		else:
			outfile.write(data)

parser = MyHTMLParser()

path = 'web/'
data = ''
count = 0
files = os.listdir(path)
for file in files :
	url = file.replace('__', '/')
	namelistFile.write(url + '\n')

for file in files :
	count += 1
	txt_path = path + file
	if 'download.php' or '.swp' in txt_path: continue
	filename = 'info/' + file
	url = 'info.ruc.edu.cn/' + file
	url.replace('__', '/')
	contents = codecs.open(txt_path, 'r')
	data = ''
	for content in contents:
		data += content
	outfile = open(str(count) + '.txt', 'w')
	parser.feed(data)

	if count == 1: break
print(count)
