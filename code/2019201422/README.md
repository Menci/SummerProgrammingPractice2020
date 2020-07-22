# Nanako Search Engine
A program which can  build a small database for searching.

The program supports the search for pdf files.

Homework of Summer Programming Practice 2020.


# Requirements
* Python3 (3.8.4)

# Installation
```bash
pip install flask
pip install jieba
pip install BeautifulSoup
pip install pdfminer
```

# Initialization
(The initialization method is for Windows OS, but you can do the same thing on Linux or mac.)

```bash
cd NanakoSearch
crawler.py
(input the domain name you want to crawl)
parser.py
index.py
```

On Linux OS you can still run these 3 files in the order mentioned above to initialize.

(To avoid being banned, the crawler.py runs slowly, the rate of progress will be shown on the terminal)

# Searching
Now the program doesn't support the query in terminal

You can use Flask to get user interface:

run routes.py
```bash
routes.py
```

Then use your browser to access http://127.0.0.1:5000 and input your queries in the search bar.

# Warning
**Never input a domain name which contains plenty of websites**

There is no self-protection mechanism in the program, your PC may crash if you input such domain name in crawler.py.




