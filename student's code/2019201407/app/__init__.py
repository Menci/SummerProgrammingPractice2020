from flask import Flask, render_template, request
import jieba
from search import search

app = Flask(__name__)

jieba.load_userdict("./userdict.txt")

@app.route("/", methods = ["GET"])
def mainpage():
    return render_template("homepage.html")

@app.route("/s", methods = ["GET"]) #s
def resultpage():
    key = request.args.get("query", "")
    if(len(key) == 0):
        return mainpage()
    else:
        return render_template("result.html", info = search(key, True), key = key)
    
'''
result:
    title
    abstract(...)
    link(...)
    
web template:
    title / input: orin
    for each res in arr

'''
