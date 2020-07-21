##Download and unzip
     $unzip 2019202122.zip
##Crawling.cpp
* used to crawl all the urls from the root url you have set.
* First , you should open the file Code .  Then input the cmd below
```javascript
$ cd code
$ g++ -std=c++14 Crawing.cpp
$ ./a.out
```
* Then you will get all the Url`s html in this file . 


##Content.cpp
* Just execute the following command.
```javascript
$ g++ -std=c++14 Content.cpp
$ ./a.out
```
* Then yuo can get the tile and the body. They will be saved in the file Content.

##CWS.cpp
* to use this cpp, you should download the THULAC of tsinghua
    *  the link is here * http://thulac.thunlp.org/*
* Then (make sure you have set the model):
* ```javascript
$ g++ -std=c++14 CWS.cpp
$ ./a.out
```

##Show_res.cpp
* remember to down load the **httplib.h** to you Linux to make sure compile successfully.
*  make_termlist.cpp
    * it`s uesd to set the dictionary by searching the title and the content
* Score.cpp
   * this cpp is to figure out the Score and rank the urls which are relevant.
* ```javascript
$ g++ -std=c++14 Show_res.cpp -lpthread
$ ./a.out
```
* Then open the chrome and go into _http://127.0.0.1::1234_ , you can search for the infomation.
