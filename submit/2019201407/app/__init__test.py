from flask import Flask, render_template, request
import jieba
from search import search

app = Flask(__name__)

jieba.load_userdict("./userdict.txt")

@app.route("/", methods = ["GET"])
def mainpage():
    return ""

@app.route("/s", methods = ["GET"]) #s
def resultpage():
    key = request.args.get("query", "")
    return search(key, False)

