from flask import request, render_template
from app import app
import time
import re
from . import parser
from . import info_mark

flag = 0
if flag == 0:
    parser.load_data()
    flag = 1

@app.route('/', methods=['GET'])
def form():
    global flag
    if flag == 0:
        parser.load_data()
        flag = 1
    return render_template("index.html")
    #return "<form method='get' action='/submit'><input name='name'><button>submit</button></form>"

cstring = ""
cresult = []
ccut = []
base_url = "http://info.ruc.edu.cn"

@app.route('/query', methods=['GET'])
def form_submit():
    global flag
    if flag == 0:
        parser.load_data()
        flag = 1
   
    t0 = time.clock()
    global cstring, cresult, ccut
    if request.args["word"] != cstring:
        cstring = request.args["word"]
        tmp = parser.query(request.args["word"])
        cresult = tmp[0]
        while len(cresult) > 0 and cresult[-1][1] == 0:
            cresult.pop()
        ccut = tmp[1]
    t1 = time.clock()

    page_count = (len(cresult) + 10) // 10
    #determine by calculated
    current_page = int(request.args["page"].encode('utf-8')) - 1
    cdata = cresult[current_page * 10 : min(len(cresult), current_page * 10 + 10)]

    load_data = []
    for i in range(len(cdata)):
        load_data.append((base_url + parser.idtodoc[cdata[i][0]], info_mark.mark_info(parser.idtodoc[cdata[i][0]], ccut, parser.idf)))
   
    for i in range(len(load_data)):
        re.sub("_index_page", load_data[i][0], "") 


    range_l = current_page - 4
    if range_l < 1:
        range_l = 1
    range_r = range_l + 10
    if range_r > page_count + 1:
        range_r = page_count + 1

    url_l = request.url.replace("page=" + str(current_page + 1), "page=")
    return render_template("result.html", word=request.args["word"], lists = range(range_l, range_r), urls = url_l, cpage = current_page + 1, result = load_data, result_len = len(load_data), main_page = request.url[:request.url.find("/query")], result_count = len(cresult), time_used = t1 - t0)


