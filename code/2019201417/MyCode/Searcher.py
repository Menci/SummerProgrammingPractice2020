#!/usr/bin/python
# -*- coding: UTF-8 -*-

import re
import io
import sys
import math
import time 
import heapq
import linecache

import jieba
from lxml import html
from bs4 import BeautifulSoup
from HTMLParser import HTMLParser

reload(sys)
sys.setdefaultencoding('utf-8')


MINIDF0 = 3.1 #5
MINIDF1 = 2.8 #10
MINIDF2 = 2.5 #20
MINIDF3 = 2.2 #50
MINIDF4 = 1.8 #100

tf = {}
url = {}
Len = []
index = {}
wordid = {}

def ttf(term, id):
	if tf.has_key(term) and tf[term].has_key(id):
		return 1 + math.log10(0.0 + tf[term][id])
	else:
		return 0
		
def idf(term):
	if index.has_key(term):
		ans = math.log10(7495.0 / (len(index[term]) + 1))
		return ans
	else:
		return 0
		
def W(term, id):
	return ttf(term, id) * idf(term)

def is_number_term(term):
	if '年' in term or '级' in term or '月' in term or '日' in term or '岁' in term:
		return True
	if '高龄' in term or '名' in term or '个' in term or '周年' in term or '人' in term:
		return True
	return False

def get_score(ID, words):
	num = {}
	val = []
	for j in range(len(words)):
		add = 1.0
		i = words[j]
		IDF = idf(i)
		if IDF >= MINIDF0:
			add = 20000.0
		elif IDF >= MINIDF1:
			add = 2000.0
		elif IDF >= MINIDF2:
			add = 200.0
		elif IDF >= MINIDF3:
			add = 20.0
		elif IDF >= MINIDF4:
			add = 2.0	
		if i.isalnum() == True:
			if len(i) == 4 or (len(i) <= 3 and j != len(words) - 1 and is_number_term(words[j + 1]) == True):
				add += 200.0
		
		if num.has_key(i):
			num[i] += add
		else:
			num[i] = add
	for i in num:
		num[i] = (1 + math.log10(num[i]) )
	for id in ID:
		ans = 0.0
		for i in num:
			if wordid.has_key(i):
				tmp = W(i, id)
				ans += (num[i]) * tmp
		if Len[id] > 0.000001:
			ans /= Len[id]
		val.append((ans, id))
		
	return val

def get_index(s):
	if wordid.has_key(s):
		pass
	else:
		return []
		
	if index.has_key(s):
		return index[s] 	
		
	tmp = linecache.getline('index.txt', wordid[s] + 1)
	
	index[s] = []
	tf[s] = {}
	
	k = -1
	j = 0
	l = 0 
	while j < len(tmp):
	
		if tmp[j] != ' ':
			j += 1 
			continue
		id = int(tmp[k + 1: j])
		index[s].append(id)
		k = j
		l = j + 1
		
		while l <= len(tmp):
		
			if tmp[l] != ' ':
				l += 1
				continue
			tf[s][id] = int(tmp[k + 1: l])
			k = l
			break
			
		j = l + 1
	
	return index[s]
	
def get_url(id):
	if url.has_key(id):
		return url[id]
	
	tmp = linecache.getline('URL.txt', id + 2)
	i = len(tmp) - 1
	for i in range(len(tmp) - 1, -1, -1):
		if tmp[i] == ' ':
			break
	 
	url[id] = tmp[0: i - 1]
	return url[id]

def get_title(docid): 
	Title = linecache.getline('title.txt', docid + 1)
	return Title

def get_Kth(ID, K, words):
	val = get_score(ID, words)
	heapq.heapify(val)
	KK = min(K + 60, len(val))
	ans = heapq.nlargest(KK, val)
	tmp = []
	for i in range(len(ans)):
		URL = get_url(ans[i][1])
		#清除一些已知的重复的网站 
		
		#if 'news_detail.php' in URL or 'notice_detail.php' in URL:
		#	continue
		
		if '#' in URL:
			continue 
			
		TITLE = get_title(ans[i][1])
		tmp.append((URL, TITLE, ans[i][1]))
	return tmp[0: min(K, len(val))]

def merge(a, b):
	j = 0
	k = 0
	ans = []
	while j != len(a) and k != len(b):
		if a[j] == b[k]:
			ans.append(a[j])
			j += 1
			k += 1
		elif a[j] < b[k]:
			ans.append(a[j])
			j += 1
		else:
			ans.append(b[k])
			k += 1
	while j != len(a):
		ans.append(a[j])
		j += 1
	while k != len(b):
		ans.append(b[k])
		k += 1		
	return ans

global stopWords
def get_stopwords_list():
	stopwords = [line.strip() for line in io.open('stopwords.txt',encoding='UTF-8').readlines()]
	return stopwords

def get_merged_index(words):
	ans = []
	if len(words) == 1:
		if wordid.has_key(words[0]):
			ans = get_index(words[0])
	else:
		i = 0
		for i in range(len(words)):
			if wordid.has_key(words[i]):
				ans = get_index(words[i])
				break
		for j in range(i + 1, len(words)):
			if wordid.has_key(words[j]):
				ttmp = get_index(words[j])
				if len(words) > 15 and idf(words[j]) < 1.17: #500
					continue
				ans = merge(ans, ttmp)
	return ans

def init():

	time_start = time.time()
	
	global stopWords
	stopWords = get_stopwords_list()
	
	WORD = open("wordlist.txt", "r")
	tmp = WORD.readline()
	n = int(tmp)
	for i in range(n):
		tmp = WORD.readline()
		tmp = tmp[0: len(tmp) - 1]
		wordid[tmp] = i
	
	DOC = open("doclen.txt", "r")
	tmp = DOC.readline()
	n = int(tmp)
	for i in range(n):
		tmp = DOC.readline()
		Len.append(float(tmp[0: len(tmp) - 1]))
	DOC.close()
	
	time_end = time.time()
	print 'init use time: ', time_end - time_start, 's'

def Search(user_qry, K): 
	init()
		
	time_start = time.time()
		
	global stopWords
	words = jieba.cut(user_qry.strip())
	words = [w for w in words if w != ' ' and w != '\n']
	words = [w for w in words if w not in stopWords]
	
	for i in range(len(words)):
		words[i] = str(words[i]).lower() 
		
	ans = get_merged_index(words)
	
	ans = get_Kth(ans, K, words)
		
	time_end = time.time()
	print 'total use time: ', time_end - time_start, 's. finish, please continue'
	
	return ans

