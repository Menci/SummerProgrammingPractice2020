import requests
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin

import jieba
import jieba.posseg
import jieba.analyse

from pdfminer.pdfparser import  PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfdevice import PDFDevice
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal,LAParams
from pdfminer.pdfpage import PDFTextExtractionNotAllowed


visited_urls=[]
queue_urls=[]
pre={'User-agent':'Mozilla/5.0'}
text_label = []
root = ".\\htmls\\"

def red_txt(filename):
    dirname = filename.replace(".txt","")
    return dirname

def is_empty(html):
    return (html.find("title")==-1)


def parse_html(path,content):

    if(is_empty(content)):
        fo=open(".\\htmls\\nouse.txt","a",encoding="utf-8")
        fo.write(path+"\n")
        fo.close()
        return

    fo=open(path+"content.txt","w",encoding="utf-8")
    print(fo.name)
    soup = BeautifulSoup(content, 'html.parser')

    list_para = soup.find_all(class_='para')
    for para in list_para:
        fo.write(para.get_text())
    
    list_body = soup.find_all(class_='essay_body')
    for body in list_body:
        fo.write(body.get_text())

    dic=open(".\\htmls\\dic_new.txt","a",encoding="utf-8")
    list_body = soup.find_all("li")
    tmp=""
    for body in list_body:
        tmp+="\n"+body.get_text()
    dic.write(tmp)
    dic.close()
    #print(tmp)
    tmp=tmp.replace(" ","")
    #print(tmp)
    fo.write(tmp)
    fo.close()
    
    fo=open(path+"subtitle.txt","w",encoding="utf-8")
    list_h1 = soup.find_all("h1")
    for h1 in list_body:
        fo.write(h1.get_text())
    list_h1 = soup.find_all("h2")
    for h1 in list_body:
        fo.write(h1.get_text())
    list_title = soup.find_all(class_="title")
    for title in list_title:
        fo.write(title.get_text())
    fo.close()

    fo=open(path+"title.txt","w",encoding="utf-8")
    fo.write(soup.find("title").get_text())
    fo.close()

def parse_pdf(Path,Save_name):
    
    parser = PDFParser(Path)
    document = PDFDocument(parser)
  
 
    if not document.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        rsrcmgr = PDFResourceManager()
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr,laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr,device)
 
        for page in PDFPage.create_pages(document):
            interpreter.process_page(page)
            layout = device.get_result()
            for x in layout:
                if(isinstance(x,LTTextBoxHorizontal)):
                    with open('%s'%(Save_name),'a',encoding="utf-8") as f:
                        results = x.get_text().encode('utf-8')
                        results = results.decode()
                        #print(results)
                        f.write(results)
                        f.close()

        fo = open(Save_name,'r',encoding='utf-8')
        content =fo.read()
        fo.close()

        content = content.replace("\n","")
        content = content.replace(" ","")
        fo = open(Save_name,'w',encoding="utf-8")
        fo.write(content)
        fo.close()
         

def find_wordlist(path):
    filename=["content","subtitle","title"]
    for file in filename:
        fo = open(path+file+".txt","r",encoding="utf-8")
        s=fo.read()
        fo.close()
        fo = open(path+file+"_wordlist.txt","w",encoding="utf-8")
        seg_list = jieba.cut_for_search(s)
        fo.write("\n".join(seg_list))
        #for x in jieba.analyse.extract_tags(s,topK=10000,withWeight=False):
        #   fo.write(x+"\n")
        fo.close()

def GetSource(path):

    filename=["content","subtitle","title"]
    for file in filename:
        fo = open(path+file+".txt","w",encoding="utf-8")
        fo.close()

    fo = open(path+"suf.txt","r",encoding="utf-8")
    suf = fo.read()
    fo.close()

    content_path = path+"content"+suf;
    print(suf)
    
    if (suf==".html")|(suf==".php")|(suf==".asp")|(suf==".aspx"):
        fo = open(content_path,"r",encoding="utf-8")
        content = fo.read()
        fo.close()
        parse_html(path,content)
        
    if (suf==".pdf"):
        Path = open(path+"content"+suf,'rb')
        parse_pdf(Path,path+"content.txt")
        Path.close()

        fo = open(path+"url.txt","r",encoding="utf-8")
        title = fo.read()
        fo.close()
        
        fo = open(path+"title.txt","w",encoding="utf-8")
        fo.write(title)
        fo.close()
    find_wordlist(path)
    
 
root = ".\\htmls\\"
i=1
ans=0

while (1):
    path = root+str(i)+"\\"
    try:
        GetSource(path)
    except:
       break
    print("Now processing:"+path)
    i+=1


