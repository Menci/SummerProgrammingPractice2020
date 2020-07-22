import requests
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin

import jieba
import jieba.posseg
import jieba.analyse

import math

Docnum = 0
Wordnum = 0
root = ".\\htmls\\"
count = 0
dic = dict()
tf_list = list()
idf_list = list()
def is_Chinese(check_str):
    for ch in check_str:
        if ((u'\u4e00' > ch) | (ch > u'\u9fff'))&(ch!='\n'):
            return False
    return True


def get_single_dic(path):
    filename = ["content","subtitle","title"]
    for name in filename:
        f = open(path+name+"_wordlist.txt","r",encoding="utf-8")
        while 1: 
            lines = f.readlines() 
            if not lines: 
                break
            for line in lines:
                line = line.replace("\n","")
                if((is_Chinese(line)|line.isalnum())&(line!="")):
                    try:
                        dic[line]
                    except:
                        global count
                        count =count+1
                        dic[line] = count

def get_dic(path):
    global Docnum
    Docnum = 1
    while(1):
        try:
            get_single_dic(path+"\\"+str(Docnum)+"\\")
        except:
            Docnum -= 1
            break
        print("now processing :"+str(Docnum))
        Docnum=Docnum+1
    global Wordnum
    Wordnum = len(dic)
    fo = open(root+"diction.txt","w",encoding='utf-8')
    fo.write(str(dic))
    fo.close()

def load_dic():
    root = ".\\htmls\\"
    fo = open(root+"diction.txt","r",encoding='utf-8')
    global dic
    dic =eval(fo.read())
    fo.close()

def get_single_sy(path):
    filename = [("content",1),("subtitle",2),("title",10)]
    now_dic=dict()
    for pr in filename:
        name = pr[0]
        weight = pr[1]
        f = open(path+name+"_wordlist.txt","r",encoding="utf-8")
        while 1: 
            lines = f.readlines()
            if not lines: 
                break
            for line in lines:
                line = line.replace("\n","")
                try:
                    dic[line]
                    try:
                        now_dic[dic[line]]+=weight
                    except:
                        now_dic[dic[line]]=weight
                except:
                    123
    f= open(path+"diction.txt","w",encoding="utf-8")
    f.write(str(now_dic))
    f.close()

    
def init():
    load_dic()
    root = ".\\htmls\\"
    get_norm(root)
    for i in range(1,Docnum+1):
        print(i)
        get_single_sy(".\\htmls\\"+str(i)+"\\")
    i=1
    lenth = len(dic)+1
    global dic_list
    dic_list = []
    for i in range(0,lenth):
        dic_list.append(dict())
    for i in range(1,Docnum+1):
        print("Now proecssing "+str(i)+"\n")
        fo = open(root+str(i)+"\\diction.txt","r",encoding="utf-8")
        now_dic = dict()
        now_dic = eval(fo.read())
        for k,v in now_dic.items():
            try:
                dic_list[k][i]=v
            except:
                print(k)
                print(i)
    fo = open(root+"suoyin.txt","w",encoding="utf-8")
    for i in range(1,lenth):
        dic_list[i] = sorted(dic_list[i].items(),key=lambda x:x[0],reverse = False)
        fo.write(str(dic_list[i])+"\n")
    fo.close()
    global idf_list
    idf_list.append(0)
    max_idf = 0
    for i in range(1,Wordnum+1):
        ans = 0
        for k,v in dic_list[i]:
            ans+=v
        max_idf = max(max_idf,ans)
    max_idf = 2*max_idf
    for i in range(1,Wordnum+1):
        ans = 0
        for k,v in dic_list[i]:
            ans+=v
        idf_list.append(math.log10(max_idf/ans))
    fo = open(root+"idf.txt","w",encoding="utf-8")
    fo.write(str(idf_list))
    fo.close()
    global tf_list
    tf_list.append(list())
    
    for i in range(1,Wordnum+1):
        now_list = list()
        now_list.append((0,0))
        for tmp in dic_list[i]:
            tmp = list(tmp)
            tmp[1] = 1+math.log10(tmp[1])
            now_list.append(tmp)
        tf_list.append(now_list)
    fo = open(root+"tf.txt","w",encoding="utf-8")
    for i in range(0,Wordnum+1):
        fo.write(str(tf_list[i])+"\n")
    fo.close()
    
def get_norm(path):
    now_list = list()
    now_list.append(0)
    for i in range(1,Docnum+1):
        ans =1
        fo = open(path+str(i)+"\\url.txt","r",encoding="utf-8")
        url = fo.read()
        fo.close()
        if(url.find("namelist")!=-1):
            ans*=0.8
        if(url.find("overview")!=-1):
            ans*=1.1
        if(url.find("professor")!=-1):
            ans*=1.1
        now_list.append(ans)
    fo = open(path+"norm.txt","w",encoding="utf-8")
    fo.write(str(now_list))
    fo.close()
    
get_dic(".\\htmls\\")
init()

