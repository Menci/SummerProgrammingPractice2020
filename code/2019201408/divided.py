# encoding=utf-8
import jieba
import os

def makedir(path) :
    folder = os.path.exists(path)
    if not folder :
        os.makedirs(path)

def div(pathi, patho) :
    for id in range (1, 6976) :
        print(id)
        
        namin = pathi + str(id)
        namout = patho + str(id)
        if not os.path.exists(namin) :
            continue
        fin = open(namin, 'r', encoding = 'utf-8')
        fout = open(namout, 'w', encoding = 'utf-8')

        data = fin.read()
        seg_list = jieba.cut_for_search(data)
        for detial in seg_list : 
            print(detial, file = fout)

        fin.close()
        fout.close()


makedir('./divided_title')
div('./normalized_title/', './divided_title/')
makedir('./divided_time')
div('./normalized_time/', './divided_time/')
makedir('./divided_source')
div('./normalized_source/', './divided_source/')
makedir('./divided_body')
div('./normalized_body/', './divided_body/')