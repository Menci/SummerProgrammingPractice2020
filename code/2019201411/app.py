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
import argparse

app = Flask(__name__)

@app.route('/submit', methods=['GET'])
def submit_form():
    return render_template('search.html')

reload(sys)
sys.setdefaultencoding('utf8') 
jieba.setLogLevel(logging.INFO)

Index = {}
df = {}
tf = {}#{<(term, docID)>:times}

parser=argparse.ArgumentParser(prog="app.py")
parser.add_argument('-num', type=int, default=0, help='the number of the websites, default=0')
args=parser.parse_args()
N = args.num

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

for word in tf.keys() :
    tf[word] = (1 + math.log10(tf[word])) * math.log10(N / df[word[0]])

with open("u_t.out", "r") as f:
    urlList = f.readlines()
for i in range(0, len(urlList)):
    urlList[i] = urlList[i].rstrip('\n')

print("pretreat finished!")

urls = ["http://www.baidu.com", "http://info.ruc.edu.cn/"]

@app.route('/submit', methods=['POST'])
def submit():
    queryStr = request.form['name']
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
    K = min(10, len(sortedList))

    info = []
    for i in range(0, K):
        docID = sortedList[i][2]
        content = ""
        with open(str(docID) + ".txt~", "r") as f:
            contentLines = f.readlines()
            for i in range(0, len(contentLines)):
                contentLines[i] = contentLines[i].rstrip('\n')

            # brief content displayed in the results
            if (len(contentLines) > 7) :
                i = 7
                totalLen = 0
                while totalLen < 25 and i < len(contentLines):
                    totalLen += len(contentLines[i])
                    content = content + contentLines[i] + " ";
                    i += 1
                if i < len(contentLines) : content = content + "..."
            
        #mark the key word
        content = unicode(content, 'utf-8')
        for word in uniqueWords :
            pos = content.rfind(word)
            while pos != -1 :
                content = content[:pos] + "<strong>" + content[pos:pos+len(word)] + "</strong>" + content[pos+len(word):]
                pos = content[:pos].rfind(word)

        info.append((urlList[docID-1], urlList[N+docID-1], content))

    return render_template('results.html', username=request.form['name'], info=info)

if __name__ == '__main__':
    app.run()

