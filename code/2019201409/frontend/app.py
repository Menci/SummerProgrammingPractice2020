import os

from flask import (
    Flask, Blueprint, flash, g, redirect, render_template, request, session, url_for, Markup, jsonify
)
from flask_bootstrap import Bootstrap

import pkuseg
from search import SrcEng


app = Flask(__name__, instance_relative_config=True)
bootstrap = Bootstrap(app)
app.config['BOOTSTRAP_BTN_STYLE'] = 'primary'
app.config['BOOTSTRAP_BTN_SIZE'] = 'lg'


@app.route('/', methods=["POST", "GET"])
def query():
    if request.method == 'POST':
        keyword = request.form['queryKeyword']
        output = SrcEng.query(keyword, 20)
        if len(output) > 0:
            return render_template('result.html', keyword=keyword, results=output)
        else:
            return render_template('query_failed.html', keyword=keyword)
    return render_template('query.html')


@app.route('/query', methods=['GET'])
def rawquery():
    word = request.args.get('word')
    if word != None:
        results = SrcEng.query_raw(word, 100)
        return render_template('raw_query.html', results=results)
    else:
        return "Bad Arguments"


@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


@app.route('/api', methods=['GET'])
def apiquery():
    word = request.args.get('query')
    results = SrcEng.query_raw(word, 100)
    res = ""
    for result in results:
        res += result[1].strip() + '\n'
    return res


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=2333)
