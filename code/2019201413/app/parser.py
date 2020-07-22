import re
import os
import time
import jieba
from html.parser import HTMLParser
from math import log, sqrt

debug_flag = 0 # 1 == debugging

printpath = re.compile('.*\/')
def path_check(filename):
    filepath = printpath.match(filename)
    if filepath != None and not os.path.exists(filepath.group()):
        os.makedirs(filepath.group())

idtodoc = []
doctoid = {}
tf = {}
df = {}
idf = {}
docval = {}
Ndf = 0

try:
    file_path = 'app/source/'
    stopword_file = open(file_path + "stopwords.txt", "r")
except:
    file_path = 'source/'
    stopword_file = open(file_path + "stopwords.txt", "r")

banlist = stopword_file.read().split()
banlist.append("")

class MyHtmlParser(HTMLParser):
    target_file = 'None'
    stacks = []
    vis = set()
    flag = 0
    ind = 0
    f = None

    def initparser(self, target, doc_id):
        self.vis.clear()
        self.ind = doc_id
        self.target_file = target
        path_check(self.target_file)
        self.f = open(self.target_file, 'w')
        ind = doc_id

    def handle_starttag(self, tag, attrs):
        if ('class', 'essay') in attrs:
            self.flag = 1
            self.stacks.append('essay')
        elif tag == 'h1' and self.flag == 1:
            self.stacks.append('title')
            self.flag = 2
        elif tag == 'title':
            self.stacks.append('html_title')
        elif ('class', 'share') in attrs:
            self.flag = 0
            self.stacks.append('share')
        else:
            self.stacks.append('normal')

    def handle_endtag(self, tag):
        attr = self.stacks.pop()
        if attr == 'essay':
            self.flag = 0
        elif attr == 'title' and self.flag == 2:
            self.flag = 1
        elif attr == 'share':
            self.flag = 1

    def handle_data(self, data):
        data = data.strip()
        if len(self.stacks) >= 1 and self.stacks[-1] == 'html_title':
            print(data, file = self.f)
        if self.flag == 0 or len(data) == 0:
            return
        ind = data.find("")

        for word in jieba.cut_for_search(data):
            word = word.strip()
            if len(word) == 0 or word == '\n':
                continue
            if word not in self.vis:
                self.vis.add(word)
                df[word] = df.setdefault(word, 0) + 1
            if word not in tf:
                tf[word] = {}
            if self.flag == 2:
                tf[word][self.ind] = tf[word].setdefault(self.ind, 0) + 10
            else:
                tf[word][self.ind] = tf[word].setdefault(self.ind, 0) + 1
        print(data, file = self.f)


def read_file(file_path):
    if not os.path.isfile(file_path):
        raise TypeError(file_path + " does not exist")
    all_the_text = open(file_path).read()
    return all_the_text

def parse_file(src, dest, ind):
    parser = MyHtmlParser()
    parser.initparser(dest, ind)
    parser.feed(read_file(src))

def parse_all():
    if not os.path.exists('source/parse_data'):
        os.makedirs('source/parse_data')
    filelist = open('source/file.txt', mode = 'r')
    
    global Ndf
    max_id = 0
    for filename in filelist.readlines():
        filename = filename[:-1]
        print("parse page:" + filename)
        parse_file('source/pages' + filename, 'source/parse_data' + filename, max_id)
        idtodoc.append(filename)
        doctoid[filename] = max_id
        max_id += 1

    Ndf = max_id + 1
    filelist.close()


def calculate():
    for word, dfv in df.items():
        idf[word] = log(Ndf / dfv) / log(10)
    for word, doclist in tf.items():
        idfv = idf[word]
        for doc, tfv in doclist.items():
            if doc not in docval:
                docval[doc] = {}
            docval[doc][word] = (1 + log(tfv) / log(10)) * idfv

    #normalize
    for doc, wordlist in docval.items():
        sums = 0
        for val in wordlist.values():
            sums += val * val
        sums = sqrt(sums)

        if sums != 0:
            for word in wordlist:
                docval[doc][word] /= sums

def save_data():
    idff = open(file_path + "idf.txt", "w")
    for word, idfv in idf.items():
        print(word + " " + str(idfv), end = " ", file = idff)
    idff.close()

    docf = open(file_path + "docw.txt", "w")
    print(len(docval), file = docf)
    for doc, wordlist in docval.items():
        print(str(doc), end = " ", file = docf)
        for word, val in wordlist.items():
            print(word + " " + str(val), end = " ", file = docf)
        print("", file = docf)
    docf.close()

def load_data():
    filelist = open(file_path + 'file.txt', 'r')
    max_id = 0
    for filename in filelist.readlines():
        filename = filename[:-1]
        idtodoc.append(filename)
        doctoid[filename] = max_id
        max_id += 1
    filelist.close()
    
    idff = open(file_path + "idf.txt", "r")
    tmplist = idff.readline()[:-1].split()
    for i in range(0, len(tmplist), 2):
        idf[tmplist[i]] = float(tmplist[i + 1])
    idff.close()

    docf = open(file_path + "docw.txt", "r")
    dictsiz = int(docf.readline()[:-1])
    for i in range(dictsiz):
        tmplist = docf.readline()[:-1].split()
        cdoc = int(tmplist[0])
        for j in range(1, len(tmplist), 2):
            if cdoc not in docval:
                docval[cdoc] = {}
            docval[cdoc][tmplist[j]] = float(tmplist[j + 1])
    docf.close()

    for openjieba in jieba.cut_for_search("open"):
        print("initialize jieba")
    print("jieba initilize complete")


def cmp(x):
    return x[1]

def sqr(x):
    return x * x

def query(qstring):
    tfq = {}
    qval = {}
    cutlist = jieba.lcut_for_search(qstring)
    for word in cutlist:
        if word not in banlist:
            tfq[word] = tf.setdefault(word, 0) + 1
    for word, tfv in tfq.items():
        tmp = idf.setdefault(word, 0)
        if tmp > 0:
            qval[word] = (1 + log(tfv) / log(10)) * idf.setdefault(word, 0)

    if len(qval) > 0:
        sums = 0
        for val in qval.values():
            sums += val * val
        sums = sqrt(sums)
        if sums > 0:
            for word in qval:
                qval[word] /= sums

    doclist = []
    for doc, wordlist in docval.items():
        cvalue = 0
        for word, val in qval.items():
            cvalue += wordlist.setdefault(word, 0) * val
        if cvalue > 0:
            doclist.append((doc, cvalue))

    doclist.sort(key = cmp, reverse = True)
    return (doclist, cutlist)

