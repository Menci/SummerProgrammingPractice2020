#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys
import time
import Queue
import string
import requests

from lxml import html
from urlparse import urljoin
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf-8')

global cnt
hash = [0 for i in range(10000)]
s = [[0 for i in range(1000)] for i in range(10000)]

def delete_file(x):
	if os.path.exists(str(hash[x]) + '.html'):
		os.remove(str(hash[x]) + '.html')
	hash[x] = -1
	global cnt
	cnt = cnt - 1
	return

END = ['.doc:', '.docx:', '.pdf:', '.xls:', '.xlsx:', '.png:', '.gif:', '.rar:', '.flv:']
def check(tmp, end):
	if len(end) > len(tmp):
		return False
	j = len(tmp) - len(end) - 1
	for i in range(0, len(end)):
		j = j + 1
		if tmp[j] != end[i]: 
			return False
	return True
	
def get_space(tmp):
	for i in range(len(tmp) - 1, -1, -1):
		if tmp[i] == ' ':
			return i
	return -1

def correct_spider():
	f = open("URL.txt", "r")
	list = f.readline()
	n = int(list[get_space(list) + 1: len(list)])
	global cnt
	cnt = n
	for i in range(n):
		list = f.readline()
		s[i] = list[0: get_space(list)]
		hash[i] = int(list[get_space(list) + 1: len(list)])
		for j in END:
			if check(s[i], j):
				delete_file(i)
				break
		
		if string.find(s[i],'/download') != -1:
			delete_file(i)
		
	f.close()
	f = open("URL.txt", "w")
	f.write('Total: ' + str(cnt) + '\n')
	for i in range(n):
		if hash[i] >= 0:
			f.write(s[i] + ' ' + str(hash[i]) + '\n')
	f.close()
	
def main():
	correct_spider()
	
	
if __name__ == '__main__':
	main()
