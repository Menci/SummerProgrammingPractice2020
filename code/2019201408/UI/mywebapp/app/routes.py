from app import app 
from flask import request
import os
import jieba
import numpy as np
import math
import re

dic = {}
s = {}
ss = {}
lst = [{}for i in range(100000)]
lenght = {}
ans = {}
q = []
cnt = int(0)
sumfile = int(0)
NumToUrl = {}
flag = int(0)

def judge(word) :
    import re
    test_str = re.search(r"\W", word)
    if test_str == None and word != ' ' and word != '的' and word != '地' and word != '得' :
        return False;
    else:
        return True


def solveFile(id) :
    global dic
    global lst
    global cnt
    global sumfile

    dicp = {}
    dicp.clear()

    path = '../../divided_body/' + str(id)
    if not os.path.exists(path) :
        return
    fin = open(path, 'r', encoding = 'utf-8')
    data = fin.read()
    for word in data.split() :
        if judge(word) :
            continue
        if dic.get(word, -1) == -1 :
            cnt = cnt + 1
            dic[word] = cnt
            s[cnt] = 0;
            ss[cnt] = 0;
        p = dic[word]
        if dicp.get(word, -1) == -1 :
            dicp[word] = 1
            lst[p][id] = 0
            s[p] = s[p] + 1
        lst[p][id] += 1
        ss[p] = ss[p] + 1
    fin.close()
    
    path = '../../divided_title/' + str(id)
    if not os.path.exists(path) :
        return
    sumfile = sumfile + 1
    fin = open(path, 'r', encoding = 'utf-8')
    data = fin.read()
    for word in data.split() :
        if judge(word) :
            continue
        if dic.get(word, -1) == -1 :
            cnt = cnt + 1
            dic[word] = cnt
            s[cnt] = 0;
            ss[cnt] = 0;
        p = dic[word]
        if dicp.get(word, -1) == -1 :
            dicp[word] = 1
            lst[p][id] = 0
            s[p] = s[p] + 1
        lst[p][id] += 1
        ss[p] = ss[p] + 1
    fin.close()

    lenght[id] = 0
    for word in dicp :
        lenght[id] = lenght[id] + np.log10(lst[dic[word]][id]) * np.log10(lst[dic[word]][id])
    lenght[id] = lenght[id] ** 0.5
    lenght[id] = lenght[id] ** 0.495

def makeDictionary() :
    for i in range(1, 6796) :
        solveFile(i)

def makeUrl() :
    html = open("../../Reflect")
    data = html.readlines()
    for line in data : 
        list = []
        for word in line.split() :
            list.append(word)
        url = ''
        id = int(0)
        for i in range (0, list.__len__(), 1) :
            if i + 1 != list.__len__() :
                url = url + list[i]
            else :
                id = int(list[i])
        if url.find("http://") == -1 and url.find("https://") == -1 :
            url = "http://" + url
        NumToUrl[id] = url
    html.close

def presolveQuery() :
    query = 'ACM'
    ans.clear()
    seg_list = jieba.cut_for_search(query)
    q.clear()
    for word in seg_list :
        q.append(word)
    for i in range(1, 6796) :
        tmp = int(0)
        for j in range(0, len(q)) :
            word = q[j]
            if dic.get(word, -1) == -1 :
                continue
            id = dic[word]
            if lst[id].get(i, -1) == -1 :
                continue
            tmp += (1 + np.log10(lst[id][i])) * np.log10(sumfile / s[id])
        if tmp != 0 :
            ans[i] = tmp

def solveQuery(query) :
    global ans
    print(query)
    ans.clear()
    seg_list = jieba.cut_for_search(query)
    q.clear()
    for word in seg_list :
        q.append(word)
    for i in range(1, 6796) :
        tmp = int(0)
        for j in range(0, len(q)) :
            word = q[j]
            if judge(q[j]) :
                continue
            if dic.get(word, -1) == -1 :
                continue
            id = dic[word]
            if lst[id].get(i, -1) == -1 :
                continue
            # if lst[id][i] == 0 or ss[id] == 0 or len(word) == 0 :
                # print('qaqqaqaqa')
            ttmp = (1 + np.log10(lst[id][i])) * (np.log10(cnt / ss[id]) ** 1.75) * (np.log10(len(word) + 1))
            if word.isdigit() == True :
                ttmp = ttmp * (np.log10(len(word) + 1) + 1.6)
            tmp = tmp + ttmp
        if tmp != 0 and lenght[i] != 0:
            ans[i] = tmp / lenght[i]
            if NumToUrl[i].find("academic_") != -1 :
                if NumToUrl[i].find("professor") != -1:
                    ans[i] = ans[i] * 1.6
                else :
                    ans[i] = ans[i] * 1.2
            else :
                if NumToUrl[i].find("overview_") != -1 :
                    ans[i] = ans[i] * 1.2
                else :
                    if NumToUrl[i].find("notice_") != -1 or NumToUrl[i].find("news_") != -1 :
                        ans[i] = ans[i] / 1.2

def trans(data) :
    str = data
    for i in range(0, len(q)) :
        if judge(q[i]) :
            continue
        pos = 0
        while 1 :
            pos = str.find(q[i], pos, len(str))
            if pos != -1 :
                t1 = ''
                t2 = ''
                if pos != 0 :
                    t1 = str[0 : pos]
                if (pos + len(q[i])) < len(str) :
                    t2 = str[(pos + len(q[i])) : len(str)]
                str = t1 + '<span style=\'color:red\'>' + str[pos : (pos + len(q[i]))] + '</span>' + t2
                pos = pos + len(q[i]) + 27
            else :
                break
    return str

# @app.route("/querytest", methods = ["GET"])
# def test() :
#     global flag
#     if flag == 0 :
#         flag = 1
#         makeDictionary()
#         makeUrl()
#         for i in range (1, 10) :
#             presolveQuery()
#     solveQuery(request.args["word"])
#     # solveQuery(request.args["query"])
#     Command = '['
#     # Command = ''
#     sumfile = 0
#     lasans = -1
#     for detial in sorted(ans.items(), key = lambda kv:kv[1], reverse = True) :
#         sumfile = sumfile + 1
#         if sumfile != 0 :
#             if detial[1] == lasans :
#                 sumfile = sumfile - 1
#                 continue
#         if (sumfile > 100) :
#             break
#         Command= Command + '"' + NumToUrl[detial[0]] + '",'
#         # Command = Command + NumToUrl[detial[0]] + '\n'
#         lasans = detial[1]
#     Command = Command + '""]'
#     return Command

@app.route("/test", methods = ["GET"])
def test() :
    global flag
    if flag == 0 :
        flag = 1
        makeDictionary()
        makeUrl()
        for i in range (1, 10) :
            presolveQuery()
    # solveQuery(request.args["word"])
    solveQuery(request.args["query"])
    # Command = '['
    Command = ''
    sumfile = 0
    lasans = -1
    for detial in sorted(ans.items(), key = lambda kv:kv[1], reverse = True) :
        sumfile = sumfile + 1
        if sumfile != 0 :
            if detial[1] == lasans :
                sumfile = sumfile - 1
                continue
        if (sumfile > 100) :
            break
        # Command= Command + '"' + NumToUrl[detial[0]] + '",'
        Command = Command + NumToUrl[detial[0]] + '\n'
        lasans = detial[1]
    # Command = Command + '""]'
    return Command

@app.route("/", methods = ["GET"])
def search() :
    global flag
    if flag == 0 :
        flag = 1
        makeDictionary()
        makeUrl()
        for i in range (1, 10) :
            presolveQuery()
    web = open('./elgooG.html', 'r', encoding = 'utf-8');
    Command = web.read();
    return Command
    
@app.route("/result", methods = ["GET"])
def result():
    global flag
    if flag == 0 :
        flag = 1
        makeDictionary()
        makeUrl()
        for i in range (1, 10) :
            presolveQuery()
    solveQuery(request.args["name"])

    Command = '<head> \
    <meta http-equiv = "content-type" content = "text/html; charset = utf-8"/> \
    <style> \
        input{ \
            border: 1px solid #ccc; \
            padding: 7px 0px; \
            border-radius: 3px; \
            padding-left:5px; \
            -webkit-box-shadow: inset 0 1px 1px rgba(0,0,0,.075); \
            box-shadow: inset 0 1px 1px rgba(0,0,0,.075); \
            -webkit-transition: border-color ease-in-out .15s,-webkit-box-shadow ease-in-out .15s; \
            -o-transition: border-color ease-in-out .15s,box-shadow ease-in-out .15s; \
            transition: border-color ease-in-out .15s,box-shadow ease-in-out .15s \
        } \
        input:focus{ \
                border-color: #66afe9; \
                outline: 0; \
                -webkit-box-shadow: inset 0 1px 1px rgba(0,0,0,.075),0 0 8px rgba(102,175,233,.6); \
                box-shadow: inset 0 1px 1px rgba(0,0,0,.075),0 0 8px rgba(102,175,233,.6) \
        } \
        input{ \
            outline-style: none ; \
            border: 1px solid #ccc;  \
            border-radius: 10px; \
        } \
        input{ \
            text-indent:10px; \
        } \
        button{ \
            outline-style: none ; \
            border: 1px solid #ccc;  \
            border-radius: 10px; \
        } \
        .logo{ \
            position: fixed; \
            top:50%; \
            left: 50%; \
            margin-top: -450px; \
            margin-left:-500px ; \
        } \
        .search{ \
            position: fixed; \
            top:50%; \
            left: 50%; \
            margin-top: -450px; \
            margin-left:-320px ; \
        } \
        .result{ \
            position: fixed; \
            top:10%; \
            left: 30%; \
            margin-left:-320px ; \
        } \
    </style> \
    <title> Welcome to elgooG! </title> \
</head> \
<body> \
    <div class = "logo"> \
        <img src="./static/google.png", width="150", height="50"> \
    </div> \
    <form method = "get" action = "/result"> \
        <div class = "search"> \
            <input type = "text", name = "name",' +  ' value = "' + request.args["name"] +'",' + ' style = "height:40px; width:600px; font-size:16px"> \
            <button style = "height:40px; width:75px; font-size: 16px; align-items: center;"> Search </button> \
        </div> \
    </form> '

    Command = Command + '<div class = "result"><div  \
                style=\' \
                width: 1400px;  \
                height: 850px; \
                overflow: auto; \
                scrollbar-darkshadow-color: #85989C; \
                scrollbar-track-color: #95A6AA; \
                scrollbar-arrow-color: #FFD6DA; \
                \'>'
    sumurl = 0
    lasans = -1
    for detial in sorted(ans.items(), key = lambda kv:kv[1], reverse = True) :
        sumurl = sumurl + 1
        if sumurl > 1 :
            if detial[1] == lasans :
                sumurl = sumurl - 1
                continue
        lasans = detial[1]
        # print(sumurl, '  ', lasans)
        if (sumurl > 10) :
            break
        path = '../../normalized_title/' + str(detial[0])
        if os.path.exists(path) :
            file = open(path, 'r', encoding = 'utf-8')
            data = file.read()
            Command = Command + '<a href = "' + NumToUrl[detial[0]] + '"><p style = "font-size:20px; color:mediumblue" id = "show">' + trans(data) + '</p></a>'
        else :
            Command = Command + '<a href = "' + NumToUrl[detial[0]] + '"><p style = "font-size:20px; color:mediumblue" id = "show">' + NumToUrl[detial[0]] + '</p></a>'

        path = '../../normalized_time/' + str(detial[0])
        if os.path.exists(path) :
            file = open(path, 'r', encoding = 'utf-8')
            data = file.read()
            Command = Command + '<p style = "font-size:15px;color:grey" id = "show">' + data
            path = '../../normalized_source/' + str(detial[0])
            if os.path.exists(path) :
                file = open(path, 'r', encoding = 'utf-8')
                data = file.read()
                Command = Command + ';' + data
            Command = Command + '</p>'
        else :
            path = '../../normalized_source/' + str(detial[0])
            if os.path.exists(path) :
                file = open(path, 'r', encoding = 'utf-8')
                data = file.read()
                Command = Command + '<p style = "font-size:15px;color:grey" id = "show">' + data + '</p>'
        
        frspos = -1
        path = '../../normalized_body/' + str(detial[0])
        file = open(path, 'r', encoding = 'utf-8')
        data = file.read()
        for i in range(0, len(q)) :
            tmppos = data.find(q[i])
            if tmppos != -1 :
                if frspos == -1 :
                    frspos = tmppos
                else :
                    frspos = min(frspos, tmppos)
        if frspos == -1 :
            Command = Command + '<p style = "font-size:16px;color:black" id = "show">' + trans(data[0:min(150, len(data))]) + '</p>'
        else :
            Command = Command + '<p style = "font-size:16px;color:black"  id = "show">... ' + trans(data[max(0, frspos - 10):min(150 + frspos, len(data))]) + ' ...</p>'

    Command = Command + '</div>'

    # Command = Command + '<span style=\'color: red;\'></span> \
    #                     <script type="text/javascript">'
    # for i in range(0, len(q)) :
    #     if not judge(q[i]) :
    #         Command = Command + 'document.getElementById("show").innerHTML = document.getElementById("show").innerHTML.replace(eval(\'/'+ q[i] + '/ig\'),"<span style=\'color: red;\'>' + q[i] + '</span>");'
    # Command = Command + '</script>' 

    Command = Command + '</div>'
    Command = Command + '</body>'
    
    return Command
