# Easy Search

A very simple web search engine, Homework of SummerProgrammingPractice2020

## Requirements

* Python3
* Flask( https://palletsprojects.com/p/flask/ )
* Jieba( https://github.com/fxsjy/jieba )

## Initialization

Open *app/target_website.txt*, and change the website link to your target website.

Then run *app/initialize.py* using the command below:

```bash
python3 initialize.py
```

## Usage

First, run a Flask server with the command below:

```bash
python3 -m flask run
```

Then use a browser to access the server provided by Flask.

Can customize stop word list by editing *app/source/stopwords.txt*, words are divided by line.
