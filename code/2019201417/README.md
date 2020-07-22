# Before you start, you need to prepare:

* this file
* python2.7
**And you need to download the following libraries:**
* bs4
* lxml
* jieba
* flask
* urlparse
* HTMLParser

# This document contains:

## MyCode:

All the Python files written for this assignment, along with a stopwords.

### Spider.py, Check.py:

The former is the crawler and the latter is the file that checks the crawler.The reason why the latter exists is that some urls need to be deleted after I complete the crawler, so urls that do not conform to the rules should be deleted on this basis.

#### When run, the following files are generated:
##### Lots of HTML files:
The web pages that the crawler gets.
##### URL.txt:
Store all the urls the crawler gets.
The first line shows how many urls there are.
Each subsequent line displays a URL and a hash value, where the url corresponds to an HTML file named after the hash value.

### Get_Text.py:

#### When run, the following files are generated:
##### wordlist.txt:
Store all the words we get from the web pages.
The first line shows how many terms there are.
The next line is one term.
##### title.txt:
Store the title of all web pages.
The ith line is the title of the web page which docid is i-1  (note that docid is not a hash value, but the order in which it appears in URl.txt).
##### doclen.txt:
Store the vector length of all web pages.
The first line shows how many urls there are.
The (i+1)th line isthe vector length of the web page which docid is i-1.
##### index.txt:
Stores inverted index for each term
The ith line has the inverted index and TF value of the i-th term (the order of words is numbered by wordlist.txt).
There are 2n Numbers in each line, the j *2-1 number is the docid, and the j \*2 number is the TF value of the term in the corresponding docid.

### Get_Abtract.py:

Generate abstract of all web pages.
#### When run, the following files are generated:
##### text:
It stores the TXT file named docid, which is the body of each doc.

### Searcher.py:

Searching answers by keyword.

### Main.py:

Generate web pages.

## SearchEngine.zip:

A search engine that does not contain abstracts.
Run it after unzipping:
>$ python Main.py

For the version which has abstracts, use the above file to generate a text folder and then place the text folder in the location of Main.py.
>\$ ./Spider.py
>\$ ./Check.py
>\$ ./Get_Abtract.py

If you need to update, do the following:
>\$ ./Spider.py
>\$ ./Check.py
>\$ ./Get_Text.py

And copy all the generated txt files to the location of Main.py.
