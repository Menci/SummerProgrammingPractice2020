#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys
import time
import Queue
import requests

from lxml import html
from urlparse import urljoin
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf-8')

B = 257
MOD = 19260817
string_to_hash_table = {}
hash_to_string_table = {}

def probe(x):
	ans = ((x + 1) >> 1) * ((x + 1) >> 1)
	if x & 1:
		pass
	else:
		ans = -ans
	return ans
	
def string_to_hash(s):
	if string_to_hash_table.has_key(s) == False:
		hash = 0
		for i in range(len(s)):
			hash = (hash * B % MOD + ord(s[i])) % MOD
		
		for i in range(MOD):
			tmp = ((hash + probe(i)) % MOD + MOD) % MOD
			if hash_to_string_table.has_key(tmp):
				continue
			hash = tmp
			break
		
		string_to_hash_table[s] = hash
		hash_to_string_table[hash] = s
		
	return string_to_hash_table[s]
	
def print_hash_table():
	f = open("URL.txt", "w")
	f.write('Total: ' + str(len(string_to_hash_table)) + '\n')
	for i in string_to_hash_table:
		f.write(i + ': ' + str(string_to_hash_table[i]) + '\n')
	f.close()
	
def check(root_url, url):
	if len(root_url) > len(url):
		return False
	for i in range(len(root_url)):
		if root_url[i] != url[i]:
			return False
	for i in range(len(url)):
		if url[i] == '@':
			return False
	return True
	
def normalize_url(pre_url, url):
	tmp = urljoin(pre_url, url)
	end = 'index.php'
	if len(end) > len(tmp):
		return tmp
	j = len(tmp) - 10
	for i in range(0, 9):
		j = j + 1
		if tmp[j] != end[i]: 
			return tmp
	
	return tmp[0: len(tmp) - 9]
	
INF = 18000
def spider(root_url):
	q = Queue.Queue(0)
	vis = {}
	
	q.put(root_url)
	vis[root_url] = True
	
	cnt = 0
	while q.qsize() > 0:
		cnt += 1
		if cnt > INF: 
			print 'ERROR: Too Many Page'
			return
			
		url = q.get()
		response = requests.get(url, timeout=5).status_code
		if response == 200:
			pass
		else:
			continue
			 
		sys_string = 'wget -O ' + str(string_to_hash(url)) + '.html ' + '\'' + url + '\''
		os.system(sys_string)
		time.sleep(1.5)

		res = requests.get(url)
		soup = BeautifulSoup(res.text, 'lxml')
		for tmp in soup.find_all('a'):
			link = tmp.get('href')
			if link is None:
				continue
			link = normalize_url(url, link)
			if check(root_url, link) == False:
				continue
			if vis.has_key(link):
				continue	
			q.put(link)
			vis[link] = True
		
	return

def main():	
	spider('http://info.ruc.edu.cn/')
	print_hash_table()

	
if __name__ == '__main__' :
	main()
