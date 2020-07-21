import os
from ess import *
from arguments import *
import cutter
from math import log, exp

P1 = 998244353
P2 = 1000000007
D = 19260817

def stopword(term):
    return term in term_filter      

#output
def outputarr(File, arr):
    f = open(dataDir + File, mode = "w")
    for each in arr:
        f.write(str(each))
        f.write("\n")
    f.close()

def outputarr2(File, arr2):
    f = open(dataDir + File, mode = "w")
    for arr in arr2:
        for each in arr:
            f.write(str(each[0]))
            f.write(" ")
            f.write(str(each[1]))
            f.write("|")
        f.write("\n")
    f.close()

def bkdr(s, d, p):
    res = 0
    for i in range(len(s)):
        res *= d
        res += 1 + ord(s[i])
        res %= p
    return res

def myhash(term):
    return bkdr(term, D, P1) * P2 + bkdr(term, D, P2)

def getkey(elem):
    return myhash(elem[0])

if __name__ == "__main__":
    
    print("Now start index.py")
    
    chkDir(dataDir)
    
    INs = [dicttextDir, dicttitleDir]
    docs = os.listdir(INs[0])   #
    docMlen = [0] * len(docs)   #
    terms = []                  #
    termID = {}
    termCnt = 0
    termArr = []                #
    postLists = []              #

    f = open("stopwords.txt", mode = "r")
    term_filter = set(f.read().split("\n"))
    f.close()  
    
    n = len(docs)
    
    i = 0
    for doc in docs:
        count = {}
        
        if abs(os.path.getsize(rawtextDir + doc) - os.path.getsize(rawtitleDir + doc)) <= 4:
            docMlen[i] = 2147483648
        
        # totsize = os.path.getsize(INs[0] + doc) + os.path.getsize(INs[1] + doc)
        
        for IN in INs:
            f = open(IN + doc, mode = "r")
            temp = f.read().split("\n")
            
            for term in temp:
                if stopword(term):
                    # print(doc)
                    continue
                if term not in termID:
                    termID[term] = termCnt
                    termCnt += 1
                    postLists.append([])
                    terms.append(term)
                if term not in count:
                    count[term] = 0
                
                # weight = 1048576 * (totsize - os.path.getsize(IN + doc)) / totsize
                
                weight = 1
                
                if(IN == INs[1]):
                    weight = 2048 / max(1, os.path.getsize(rawtitleDir + doc) - 45)
                    # weight = 64
                    
                count[term] += weight
                 
            f.close()
            
        for term in count:
            postLists[termID[term]].append((i, int(count[term]))) #(docID, cnt)
        
        # docMlen[i] += os.path.getsize(INs[0][0] + doc) ** 0.75
            
        i += 1
        if(i % 100 == 0):
            print("%s%d"%("." * (40 - len(str(i))), i))
    
    print("Total docs: %d" % i)
    print("Total terms: %d" % len(terms))
    
    
    for term in terms:
        df = len(postLists[termID[term]])
        for d, cnt in postLists[termID[term]]:
            docMlen[d] += (tf(cnt) * idf(df, n)) ** 2
        
    for i in range(n):
        docMlen[i] **= 0.5
        # docMlen[i] *= os.path.getsize(INs[0][0] + docs[i])
        # docMlen[i] **= 0.5
        docMlen[i] += 64 #
     
    
    termArr = [(term, termID[term]) for term in terms]
    termArr.sort(key = getkey)
    termArr = [(each[1], myhash(each[0])) for each in termArr]
    
    # output
    outputarr(docsFile, docs)
    outputarr(docMlenFile, docMlen)
    outputarr(termsFile, terms)
    outputarr(termArrFile, termArr)
    outputarr2(postListsFile, postLists)

