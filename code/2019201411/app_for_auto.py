#coding=utf-8
from flask import Flask
from flask import request
from flask import render_template
import jieba
import jieba.posseg as pseg
import sys 
import logging
import math
from operator import itemgetter, attrgetter

app = Flask(__name__)

@app.route('/', methods=['GET'])
def submit_form():
    return '''<form action='/submit' method='get'>
              <p><input name='query'></p>
              <p><button type="submit">Submit</button></p>
              </form>'''

#encode porb
reload(sys)
sys.setdefaultencoding('utf8') 
#-quiet when seg word
jieba.setLogLevel(logging.INFO)

Index = {}
df = {}
tf = {}#{<(term, docID)>:times}

N = 6897

#index & score pretreat
for i in range(1, N + 1):
    filename = str(i) + '.txt~'
    occurTimes = {}
    with open(filename, 'r') as f:
        words = jieba.lcut(f.read())
        uniqueWords = set(words)
        for word in uniqueWords :
            if word == ' ' or word == '\n' or word == 'TITLE' or word == 'content': continue
            tf[(word, i)] = words.count(word)

            if word not in Index : Index[word] = []
            Index[word].append(i)

            if word not in df : df[word] = 0
            df[word] += 1

#calc doc score
for word in tf.keys() :
    tf[word] = (1 + math.log10(tf[word])) * math.log10(N / df[word[0]])

with open("u_t.out", "r") as f:
    urlList = f.readlines()
for i in range(0, len(urlList)):
    urlList[i] = urlList[i].rstrip('\n')

print("pretreat finished!")

urls = ["http://www.baidu.com", "http://info.ruc.edu.cn/"]

@app.route('/submit', methods=['GET'])
def submit():
    queryStr = request.args['query']
    words = jieba.lcut(queryStr)
    finalDocList = []
    fq = {}
    uniqueWords = set(words)

    lengthq = 0
    for word in uniqueWords :
        if word not in Index : continue
        finalDocList = list(set(finalDocList) | set(Index[word]))
        cnt = words.count(word)
        fq[word] = (1 + math.log10(cnt)) * math.log10(N / df[word]);
        lengthq += fq[word] ** 2

    scoreList = []
    for doc in finalDocList :
        length = 0
        score = 0
        extra = 0
        for word in uniqueWords :
            if (word, doc) in tf :
                val = tf[(word, doc)]
                score += val * fq[word]
                length += val**2
                extra += val
        if length == 0 : continue
        length = math.sqrt(length)
        if queryStr in urlList[doc+N-1] : score = length * lengthq

        score /= length * lengthq
        scoreList.append((score, extra, doc))

    sortedList = sorted(scoreList, key=lambda tup:(-tup[0], -tup[1]))
    K = min(100, len(sortedList))

    info = ""
    for i in range(0, K):
        docID = sortedList[i][2]
        info = info + urlList[docID-1] + "\n"

    return info

if __name__ == '__main__':
    app.run()
