欢迎使用 LeavesSearch!
This is Leaves.

## 使用方法
	进入文档LeavesSearch
	* flask run
	* 于浏览器中进入 http://127.0.0.1:5000/ 即可搜索
## 数据更新&&编译方法
	进入 app/THULAC-master 
	* g++ -o urlget urlget.cpp
	* ./urlget
	* g++ -o CutforTF CutforTF.cpp -lpthread
	* ./CutforTF
	* g++ -o CutforIDF CutforIDF.cpp -lpthread
	* ./CutforIDF
	(It takes about 25min)
	进入 app
	* g++ -o pre pre.cpp -lpthread
	查看 app/THULAC-master/url URL的总数目 N
	修改 Search.cpp 中的 全局变量 int N
	* g++ -o Search Search.cpp

	Then you will have new data.
## CPP说明：
	urlget.cpp : get url
	Cut... .cpp: Cut words and calculate tf-idf
	pre.cpp : prepare
	Search.cpp : Search
	.. .py: for web  UI
