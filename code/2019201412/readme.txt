crawl.cpp was used to crawl all the websites from info.ruc.edu.cn into "'docid'.txt"
extract.cpp extract contents of every website from "'docid'.txt" into "'docid'ext.txt"
cut.py use jieba and cut content from "'docid'ext.txt" into "'docid'cut.txt"
calc_idf.cpp generate the Inverse retrieval from "*cut.txt" into one file "overall.txt"
Init.cpp read "overall.txt" and deal with the query, calc scores according to tf-idf, then find topK relative docid and write the answer into "result.txt"
I wrote Select.txt providing some CSS to create a better-looked UI
app.py get the url, abstract content displays in own website