#!/usr/bin/python
# -*- coding: UTF-8 -*-

import re
import io
import os
import sys
import math
import time
from re import sub

import jieba
from lxml import html
from bs4 import BeautifulSoup
from HTMLParser import HTMLParser

reload(sys)
sys.setdefaultencoding('utf-8')

class Stack(object):
    def __init__(self):
        self.stack = []
        
    def push(self, data):
        self.stack.append(data)
        
    def pop(self):
        return self.stack.pop()
    
    def size(self):
    	return len(self.stack)
    	
def class_sign(x):
	if x == 'essay_body':
		return 1
	elif x == 'nd_essay_body':
		return 1
	elif x == 'rightContent':
		return 1
	elif x == 'nd_rightContent':
		return 1
	elif x == 'news_content':
		return 1
	elif ('essay' in x) or ('Essay' in x):
		return 2
	elif ('namelist' in x) or ('Namelist' in x):
		return 3
	elif ('content' in x) or ('Content' in x):
		return 4
	elif ('para' in x) or ('Para' in x):
		return 4
	elif x == 'desp':
		return 4
	elif x == 'name':
		return 4
	elif ('intro' in x) or ('Intro' in x):
		return 4 
	elif ('title' in x) or ('Title' in x):
		return 6
	return 5

class _MyHTMLParser(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self._text = []
	
	def handle_data(self, data):
		text = data.strip()
		if len(text) > 0:
			text = sub('[ \t\r\n]+', ' ', text)
			self._text.append(text + ' ')

	def handle_starttag(self, tag, attrs):
		if tag == 'p':
			self._text.append('\n\n')
		elif tag == 'br':
			self._text.append('\n')
		elif tag == 'div':
			if len(attrs) < 1 or len(attrs[0]) < 2:
				self._text.append('5BLOCK[')
			else:
				class_id = attrs[0][1]
				x = class_sign(class_id)
				self._text.append(str(x)+'BLOCK[')
		elif tag == 'title':
			self._text.append('1TITLE[')
		elif tag == 'h1':
			self._text.append('2TITLE[')
		elif tag == 'h2':
			self._text.append('3TITLE[')
		elif tag == 'h3':
			self._text.append('4TITLE[')
		elif tag == 'h4':
			self._text.append('5TITLE[')
		elif tag == 'h5':
			self._text.append('6TITLE[')
		elif tag == 'h6':
			self._text.append('7TITLE[')
			
	def handle_endtag(self, tag):
		if tag == 'div':
			self._text.append(']BLOCK')
		elif tag == 'title':
			self._text.append(']TITLE1')
		elif tag == 'h1':
			self._text.append(']TITLE2')
		elif tag == 'h2':
			self._text.append(']TITLE3')
		elif tag == 'h3':
			self._text.append(']TITLE4')
		elif tag == 'h4':
			self._text.append(']TITLE5')
		elif tag == 'h5':
			self._text.append(']TITLE6')
		elif tag == 'h6':
			self._text.append(']TITLE7')
	
	def handle_startendtag(self, tag, attrs):
		if tag == 'br':
			self._text.append('\n\n')

	def text(self):
		return self._text
		#return ''.join(self._text).strip()

def HTML_to_text(text):
	parser = _MyHTMLParser()
	parser.feed(str(text))
	parser.close()
	return parser.text()
	
def check_sign(tmp):
	if tmp == '1TITLE[': 
		return 0
	if tmp == '2TITLE[': 
		return 1
	if tmp == '3TITLE[': 
		return 2
	if tmp == '4TITLE[': 
		return 3
	if tmp == '5TITLE[': 
		return 4
	if tmp == '6TITLE[': 
		return 5
	if tmp == '7TITLE[': 
		return 6
	if tmp == '1BLOCK[': 
		return 7
	if tmp == '2BLOCK[': 
		return 8
	if tmp == '3BLOCK[': 
		return 9
	if tmp == '4BLOCK[': 
		return 10
	if tmp == '5BLOCK[': 
		return 11
	if tmp == '6BLOCK[': 
		return 12
	if tmp == ']TITLE1': 
		return 13
	if tmp == ']TITLE2': 
		return 14
	if tmp == ']TITLE3': 
		return 15
	if tmp == ']TITLE4': 
		return 16
	if tmp == ']TITLE5': 
		return 17
	if tmp == ']TITLE6': 
		return 18
	if tmp == ']TITLE7': 
		return 19	
	if tmp == ']BLOCK': 
		return 20
	return -1 

def sol(id, g, text):
	q = Stack()
	flag = False
	for i in text:
		x = check_sign(i)
		if x < 13: 
			q.push(i)
		else:
			if q.size() > 0:
				tmp = []
				j = q.pop()
				while (x != 20 and check_sign(j) + 13 != x) or (x == 20 and check_sign(j) < 7):
					tmp.append(j)
					j = q.pop()
				if len(tmp) == 0:
					continue
				tmp.reverse()
				
				if check_sign(j) == 0 or check_sign(j) == 11:
					continue
				words = ''.join(tmp).strip().lower()
				g.write(words + '\n')
	
	return
		
def get_space(tmp):
	for i in range(len(tmp) - 1, -1, -1):
		if tmp[i] == ' ':
			return i
	return -1

def main():
	Total = open("URL.txt", "r")
	
	tmp = Total.readline()
	n = int(tmp[get_space(tmp) + 1: len(tmp)])
	
	
	for i in range(n):
		
		tmp = Total.readline()
		s = tmp[0: get_space(tmp)]
		hash = int(tmp[get_space(tmp) + 1: len(tmp)])
		print hash
		
		f = open(str(hash) + '.html', "r")
		g = open('text/' + str(i) + '.txt', "w")
		
		soup = BeautifulSoup(f.read(), 'lxml')
		o_text = HTML_to_text(soup)
		sol(i, g, o_text)
		
		g.close()
		f.close()
		
	Total.close()
	
	
if __name__ == '__main__':
	main()
