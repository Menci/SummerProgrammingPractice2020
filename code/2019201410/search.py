#!/usr/bin/env python3
import json
import os
import os.path
import hashlib
import re
import jieba
import zlib
import tqdm
from tqdm import tqdm
import math

N = 6897
titleSet = []
with open('namelist.out', 'r') as f:
	titleSet = f.readlines()
	for i in range(0, len(titleSet)):
		titleSet[i] = titleSet[i].rstrip('\n')

def check_useful_word(i):
	code = ord(i)
	#if i is a Chinese word
	if code >= 0x4e00 and code <= 0x9fa5:
		return True
	#if i is a Capital letter
	if code >= 0x41 and code <= 0x5a:
		return True
	#if i is a lowercase letter
	if code >= 0x61 and code <= 0x7a:
		return True
	#if i is a number
	if code >= 0x30 and code <=0x39:
		return True
	if i == ' ':
		return True
	return False

alltitle = set()
docId = 0
doctitle = []
docurl = []
class Page:
	def __init__(self, filename, content, json_body = None):
		if json_body is not None:
			body = json_body
			self.url = body['url']
			self.title = body['title']
			self.words = body['words']
			self.content = None #store the unmodified text
			self.useful_content = None
			self.times = None
			alltitle.add(self.url)
		#not from json
		else:
			self.url = titleSet[filename - 1]
			self.title = titleSet[filename - 1 + N]
			self.content = content
			self.useful_content = ''.join(i if check_useful_word(i) else '' for i in content);
			self.words = jieba.lcut(self.useful_content)

		#create tf
			for word in self.words:
				if len(word) >= 10:
					self.words.remove(word)
			for word in self.words:
				if ' ' in self.words:
					self.words.remove(' ')

		self.times = {}
		for word in self.words:
			if word not in self.times:
				self.times[word] = 0
			self.times[word] += 1

		self.tf = {}
		for word in self.words:
			self.tf[word] = self.times[word];

		self.tfidf = {}
		del self.content
		del self.useful_content
		del self.times
		
	def encode_to_json(self):
		body = {
			'url' : self.url,
			'title' : self.title,
			'words' : self.words
		}
		return json.dumps(body, indent = 4)
		
	def clean(self):
		del self.words

	def display(self):
		print(self.title + '\n' + self.url + '\n')
		print(self.words)

	pass

class pageLibrary:
	def __init__(self):
		self.page = set()
		self.invertedIndex = {}

	def addPage(self, page):
		self.page.add(page)
		self.invertedIndex[page.url] = page

	def build_idf(self):
		self.word_times = {}
		for page in self.page:
			for word in page.tf:
				if word not in self.word_times:
					self.word_times[word] = 0
				self.word_times[word] += 1

		self.df = {}
		for word in self.word_times:
			self.df[word] = self.word_times[word]

		#build tf-idf
		for page in self.page:
			for word in page.tf:
				page.tfidf[word] = (1 + math.log10(page.tf[word])) * math.log10(N / self.df[word])
			del page.tf
		del self.word_times

	def query(self, qs, number = 10):
		words = jieba.lcut(qs)
		query_words = set(words)
		lengthq = 0
		tq = {}
		for word in query_words:
			if word not in self.df: continue
			cnt = words.count(word)
			tq[word] = (1 + math.log10(cnt)) * math.log10(len(self.page) / self.df[word])
			lengthq += tq[word] ** 2

		Score = []
		for page in self.page:
			score = 0
			length = 0
			extra = 0
			for word in query_words:
				if word in page.tfidf:
					val = page.tfidf[word]
					score += val * tq[word]
					length += val ** 2
					extra += val
			if length == 0: continue
			length = math.sqrt(length)
			score /= length * math.sqrt(lengthq) #sqrt
			if qs in page.title : score = 1
			Score.append((score, extra, page.url))
		Score = sorted(Score, reverse = True, key = lambda tup:(tup[0], tup[1]))
		return [ {'url' : i[2], 'relevance' : i[0]} for i in Score[ : number ] ]
	
	def get_files(path):
	files = []
	allfiles = os.listdir(path)
	for file in allfiles:
		filename = file.replace('__', '/')
		files.append(filename)
	return files
	
def del_database():
	path = 'database/'
	files = os.listdir(path)
	for file in files:
		os.remove(path + file)

def set_database():
	del_database()
	path = 'DATA/'
	files = os.listdir(path)
	files = range(1, N + 1)
	for file in tqdm(files):
		i = file
		file_name = file
		file_path = path + str(i) + '.txt'
		file_url = titleSet[i - 1]
		file = str(file)
		file_hashValue = hashlib.sha256(file.encode('utf-8')).hexdigest()[:16]
		file_compress = 'database/' + file + '.json.gz'
		if os.path.exists(file_compress): continue
		#read files
		fin = open(file_path, 'rb')
		content = fin.read()
		fin.close()
		content = content.decode('utf-8')
		#create page
		page = Page(i, content)
		page_json = page.encode_to_json()
		page_compress = zlib.compress(page_json.encode('utf-8'), level = 9)
		page.clean()
		#write page_compress
		fout = open(file_compress, 'wb')
		fout.write(page_compress)
		fout.close()
	return
	

def load_data(Library):
	path = 'database/'
	files = os.listdir(path)
	for file in tqdm(files):
		fin = open(path + file, 'rb')
		page_compress = fin.read()
		fin.close()
		page_json = zlib.decompress(page_compress).decode('utf-8')
		page_body = json.loads(page_json)
		page = Page('', '', json_body = page_body)
		page.clean()
		Library.addPage(page)

def query(qs, Library, number = 10):
	query_words = list(jieba.cut(qs))
	results = Library.query(qs, number)
	result_url = []
	result_title = []
	result_content = []
	keyword = query_words[0]
	for result in results:
		url = result['url']
		relevance = result['relevance']
		page = Library.invertedIndex[url]
		title = page.title
		filename = 'info/' + filename
		fin = open(filename, 'r')
		content = fin.read()
		fin.close()
		content = content[1300:]
		str = content.find(keyword)
		abstract = content[0:50]
		if str != -1:
			abstract = content[str:][0:50]
			for key in query_words[0] :
				abstract = abstract.replace(key, '<span class="highlight">' + key + '</span>')
		result_content.append(abstract)
		result_url.append(url)
		result_title.append(title)
	return { 'url' : result_url, 'title' : result_title, 'content' : result_content}



Library = pageLibrary()
set_data = input('Load database ?(y/n)')
if set_data == 'y' :
	set_database()
load_data(Library)
Library.build_idf()

from flask import Flask
from flask import request
from flask import render_template

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def submit():
	return render_template('Lookao.html')

@app.route('/search', methods = ['GET'])
def search():
	qs = request.args['query']
	result = query(qs, Library)
	return render_template('1-Lookao.html', url = result['url'], title = result['title'], content = result['content'], 
			query = qs)

if __name__ == '__main__':
	app.run()
