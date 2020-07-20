# Search-Engine
A simple **offline web-search program** implemented with web-crawler tech., inverted index, and TF-IDF.

Homework of Summer Programming Practice 2020.

# Requirements
* Python3 (>=3.5.2)

# Installation
```bash
sudo pip3 install -r requirements.txt
```

# Initialization

Go to *arguments.py*, and change argument *root* to your target website.
For example ```root = "http://info.ruc.edu.cn/"```

Then start *run.sh*:

```bash
./run.sh
```

Or you can use ```python 3 [filename]``` to initialize data step by step:
* crawler_mt.py     *# getting html data from website*
* parser.py         *# parsing html data for pure text*
* cutter.py         *# split documents for terms*
* index.py          *# building inverted index*

# Searching
Start search using:

```bash
python3 search.py [query_text]
```

This will display result in console.

Or use Flask to get user interface:

```bash
flask run
```

Then use your browser to access your web server.

# Configuration

Set arguments in *arguments.py*.
* root              *# web-crawler target*
* resultDisplay     *# maximum results on display*
* abstractDisplay   *# maximun length of abstract (UI only)*
* *# modify file path* (not recommended)

Set stop word list in *stopwords.txt*, word per line.
Set user dictionary in *userdict.txt*, word per line.


