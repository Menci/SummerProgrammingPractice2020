# -*- coding: UTF-8 -*-

import io
import os
import re
import sys
import jieba
from re import sub

from flask import Flask, render_template, redirect, url_for, request

import Searcher

reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def main():
	if request.method == 'GET' and request.args.get('query'):
		query = request.args['query']
		
		#以下内容需要在人工评测的时候删去 
		'''
		urls = Searcher.Search(query, 100)
		f = open('/home/cpp/Desktop/SEO/templates/autosearch.html', 'w')
		for i in urls:
			f.write(i[0] + '\n')	
		f.close()  
		return render_template('autosearch.html', docs = urls, value = query, length = len(urls))
		'''
		
		urls = Searcher.Search(query, 20)
		terms = jieba.cut(query.strip())
		stopWords = get_stopwords_list()
		# clean stop_words
		terms = [w for w in terms if w != ' ' and w != '\n']
		terms = [w for w in terms if w not in stopWords]
		
		text = highlight(urls, terms, 60)
		return render_template('search.html', docs = text, value = query, length = len(urls))

	return render_template('index.html')

def get_stopwords_list():
	stopwords = [line.strip() for line in io.open('stopwords.txt',encoding='UTF-8').readlines()]
	return stopwords

def highlight(urls, terms, K):
	result = []
	K *= 4
	for doc in urls:
		title = doc[1]
		for term in terms:
			title = title.replace(term, '<font color="#EA0000">{}</font>'.format(term))
			
		txtpath = 'text/' + str(doc[2]) + '.txt'
		
		if os.path.exists(txtpath):
			f = open(txtpath, 'r')
			content = sub('[ \t\r\n]+', ' ', f.read())
			content = list(jieba.cut(content))
			
			st = 999999999
			for term in terms:
				for i in range(len(content)):
					if content[i] == term:
						st = min(st, i - 2)
			if st == 999999999 or st < 0:
				st = 0
			ed = min(len(content), st + K)
			if ed == len(content):
				st = max(0, ed - K)	
			
			cont = ''.join(content[st:ed])
			
			for term in terms:		
				cont = cont.replace(term, '<font color="#EA0000">{}</font>'.format(term))
			
			last = '...' + cont + '...'
			if len(cont) == 0:
				last = ''
				
			result.append((doc[0], title, last))
			
		else:
			result.append((doc[0], title, ''))
		
	return result

if __name__ == '__main__':
	app.run(debug = True)
