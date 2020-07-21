from flask import Flask,Response
from flask import request
from flask import render_template
import threading

app = Flask(__name__)


@app.route("/", methods=["GET"])
def form():
    fo = open(".\\templates\\my_first_page.html","r",encoding = "utf-8")
    return fo.read()

def get_single(url,title,essay_body):
    fo = open(".\\templates\\single_res.html","r",encoding = "utf-8")
    single = fo.read()
    fo.close()
    single = single.replace("{{url}}",url)
    single = single.replace("{{title}}",title)
    single = single.replace("{{essay_body}}",essay_body)
    return single

def get_results(search_sentence,title,result_body,result_num):
    fo = open(".\\templates\\res_head.html","r",encoding = "utf-8")
    result = fo.read()
    fo.close()
    result = result.replace("{{search_sentence}}",search_sentence)
    result = result.replace("{{title}}",title)
    result = result.replace("{{result_body}}",result_body)
    result = result.replace("{{result_num}}",result_num)
    return result

@app.route("/submit", methods=["GET"])
def query():
    result_body = ""
    result_num = str(100)
    search_sentence = request.args["query"]
    list_now = query_sentence(search_sentence)
    word_list = jieba.lcut(search_sentence)
    for i in list_now:
        fo = open("E:\\htmls\\"+str(i)+"\\"+"title.txt","r",encoding="utf-8")
        title = fo.read()
        fo.close()
        fo = open("E:\\htmls\\"+str(i)+"\\"+"content.txt","r",encoding="utf-8")
        essay_body = fo.read()
        fo.close()
        fo = open("E:\\htmls\\"+str(i)+"\\"+"url.txt","r",encoding="utf-8")
        url = fo.read()
        fo.close()
        if(len(essay_body)>100):
            essay_body = essay_body[0:100]
        for k in word_list:
            title = title.replace(k,"<strong>"+k+"</strong>")
            essay_body = essay_body.replace(k,"<em>"+k+"</em>")
        result_body += get_single(url,title,essay_body)+"\n"
    title ="Nanako Search"
    return get_results(search_sentence,title,result_body,result_num)

import requests
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin

import jieba
import jieba.posseg
import jieba.analyse

import math

Docnum = 6826

tf_list = list()
idf_list = list()
norm_list = list()
dic = dict()
root = "E:\\htmls\\"
def change_to_array(now_list):
    ans_list = list()
    for i in range(0,Docnum+1):
        ans_list.append(0)
    for k,v in now_list:
        ans_list[k] = v
    return ans_list

def init():
    global idf_list
    fo = open(root+"idf.txt","r",encoding="utf-8")
    idf_list = eval(fo.read())
    fo.close()
    global tf_list
    fo = open(root+"tf.txt","r",encoding="utf-8")
    lines = fo.readlines()
    for line in lines:
        tf_list.append(eval(line))
    fo = open(root+"diction.txt","r",encoding="utf-8")
    global dic
    dic = eval(fo.read())
    fo.close()
    
    global norm_list
    fo = open(root+"norm.txt","r",encoding="utf-8")
    norm_list = eval(fo.read())
    fo.close()

def query_keyword(word_id):
    print (len(tf_list))
    weight = idf_list[word_id]
    now_list = change_to_array(tf_list[word_id])
    len_ = len(now_list)
    for i in range(0,len_):
        now_list[i] *=weight
    return now_list

class MyThread(threading.Thread):
    def __init__(self, key,tmp_list):
        super(MyThread, self).__init__() 
        self.key = key
        self.temp_list = tmp_list

    def run(self):
        print("Now running "+ self.key)
        self.tmp_list = query_keyword(dic[self.key])
        print("Finish "+ self.key)

def query_sentence(query_string):
    len_ = Docnum
    ans_list = res_list = list()
    for i in range(0,len_+1):
        ans_list.append(0)
        res_list.append(0)
    thread_list = list()
    for i in range(0,4):
        thread_list.append(MyThread(0,list()))
    count = 0
    for k,v in jieba.analyse.extract_tags(query_string,topK=10000,withWeight=True):
        try:
            dic[k]
            thread_list[count%4] = MyThread(k,list())
            thread_list[count%4].start()
        except:
            continue
        print(k)
        print(v)
        if count % 4==3:
            for j in range(0,4):
                thread_list[j].join()
                for i in range(0,len_+1):
                    ans_list[i]+=thread_list[j].tmp_list[i]
                    res_list[i]+=thread_list[j].tmp_list[i]*thread_list[j].tmp_list[i]
        count+=1
    if count % 4!=0:
        for j in range(0,count):
            thread_list[j].join()
            for i in range(0,len_+1):
                ans_list[i]+=thread_list[j].tmp_list[i]
                res_list[i]+=thread_list[j].tmp_list[i]*thread_list[j].tmp_list[i]
    
    now_list = list()
    for i in range(1,len_+1):
        if res_list[i]!=0:
            now_list.append((i,ans_list[i]*norm_list[i]/math.sqrt(res_list[i])))
    return get_result(now_list,100)

def get_result(word_list,len_):
    word_list.sort(key=lambda x:x[1],reverse = True)
    Ans = list()
    max_len = len(word_list)
    for i in range(0,min(max_len,len_)):
        Ans.append(word_list[i][0])
    return Ans
                        

if("__main__"==__name__):
    init()
    jieba.load_userdict("E:\\htmls\\dict.txt")
    app.run()
