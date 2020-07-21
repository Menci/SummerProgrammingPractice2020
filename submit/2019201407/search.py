from index import *
from ess import *
from arguments import *
from math import *
import cutter
import jieba
import sys
import os
import re

def readarr(filename):
    f = open(dataDir + filename, mode = "r")
    arr = f.read().strip("\n").split("\n")
    f.close()
    return arr
    
docs = readarr(docsFile)
mlen = readarr(docMlenFile)
terms = readarr(termsFile)
a = readarr(termArrFile)
plist = readarr(postListsFile)

mlen = [float(each) for each in mlen]
n = len(docs)
m = len(terms)

def getid(term):
    l, r = 0, m - 1
    val = myhash(term)
    
    while l < r:
        mid = (l + r) // 2
        x = int(a[mid][1:-1].split(",")[1])
        if(val <= x):
            r = mid
        else:
            l = mid + 1
    
    
    if(int(a[l][1:-1].split(",")[1]) == val):
        return int(a[l][1:-1].split(",")[0])
    return -1

def normstr(s):
    v = '()[]{}^$?+*.\\'
    l = list(s)
    for i in range(len(l)):
        if l[i] in v:
            l[i] = '\\' + l[i]
    return ''.join(l)

# search for a sentence
# detail = True: add UI info
def search(sentence, detail):
    sentence = sentence.lower() # lower_case
    qterms = list(jieba.cut_for_search(sentence))
    
    score = [0] * n
    for term in qterms:
        t = getid(term)
        # print("word:", term, t)
        
        if t == -1:
            continue
        l = plist[t].strip("|").split("|")
        df = len(l)
        for each in l:
            d, cnt = each.split(" ", 1)      
            d = int(d)
            cnt = int(cnt)
            score[d] += tf(cnt) * idf(df, n) / mlen[d]
                         
    for i in range(n):
        score[i] = (i, score[i])
    score.sort(key = lambda x: x[1], reverse = True) # nth_element
    
    if detail == False:
        res = []
        for i in range(min(n, 100)):
            res.append(decrypt(docs[score[i][0]]))
        return "\n".join(res)
    
    # else: detail == True
    results = []
    for i in range(resultDisplay):
        d = score[i][0]
        url = docs[d]
        
        f = open(rawtitleDir + url, mode = "r")
        title = f.read()
        flagT = [0] * len(title)
        for term in list(qterms):
            if(getid(term) == -1):
                continue
            for it in re.finditer(normstr(term), title, re.I):
                i = int(it.start())
                for j in range(i, i + len(term)):
                    flagT[j] = 1
        f.close()
        
        f = open(rawtextDir + url, mode = "r")
        text = f.read()
        flagS = [0] * len(text)
        for term in qterms:
            if(getid(term) == -1):
                continue
            for it in re.finditer(normstr(term), text, re.I):
                i = int(it.start()) # iter, not int
                for j in range(i, i + len(term)):
                    flagS[j] = 1
        sf = [0] * (len(text) + 1)
        sf[0] = flagS[0]
        for i in range(1, len(text)):
            sf[i] = sf[i - 1] + flagS[i]
        w = min(len(text), abstractDisplay)
        sf = [sf[i + w - 1] - sf[i - 1] for i in range(0, len(text) - w + 1)]
        l = sf.index(max(sf))
        snippet = text[l : l + w]
        flagS = flagS[l : l + w]
        f.close()
        
        res1 = []
        for i in range(len(title)):
            if(flagT[i]): 
                res1.append("<font color=\"red\">" + title[i] + "</font>")
            else:
                res1.append(title[i])
                
        res2 = []
        for i in range(len(snippet)):
            if(flagS[i]):
                res2.append("<font color=\"red\">" + snippet[i] + "</font>")
            else:
                res2.append(snippet[i])
        res2.append("...")
        
        if(max(flagS) > 0 or max(flagT) > 0):
            results.append([decrypt(url), "".join(res1), "".join(res2)] )
    
    # test_mode
    if(len(os.sys.argv) > -1):
        for i in range(min(resultDisplay, len(results))):
            url = results[i][0]
            f = open(rawtitleDir + encrypt(url), mode = "r")
            print("%d:" % (i + 1), f.read())
            print(url)
            print("")
            f.close()
        print("")
    
    return results

if __name__ == "__main__":
            
    print("Now start search.py")
    jieba.load_userdict("./userdict.txt")
    
    query = os.sys.argv
    del query[0]
    
    sentence = ""
    for each in query:
        sentence += each + " "
    
    print("\nsearching:", sentence)
    print("")
    search(sentence, True)

