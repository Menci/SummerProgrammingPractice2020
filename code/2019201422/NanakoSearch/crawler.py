import requests
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin

visited_urls=[]
queue_urls=[]
pre={'User-agent':'Mozilla/5.0'}

count=None

def mkdir(path):
    
    import os
    path=path.strip()
    path=path.rstrip("\\")
  
    isExists=os.path.exists(path)
  
    if not isExists:
        
        os.makedirs(path)
  
        print (path+'successfully make')
        return True
    else:
        print (path+'derectory already exist')

def get_filename(url):
    name = url
    name=name.replace("\\","");
    name=name.replace("/","");
    name=name.replace(":","");
    name=name.replace("*","");
    name=name.replace("?","");
    name=name.replace("\"","");
    name=name.replace("<","");
    name=name.replace(">","");
    name=name.replace("|","");
    #print(name)
    return name

def find_urls(init_url):
    print ('now dealing with '+init_url)
    time.sleep(3)
    
    global cnt
    name=str(cnt)
    name = ".\\htmls"+"\\"+name
    print(name)
    mkdir(name)
    #print(name)
    fo = open(name+"\\url.txt","w",encoding="utf-8")
    fo.write(init_url)
    fo.close()
    suf=".html"
    if init_url.find(".docx")!=-1:
        suf=".docx"
    else:
        if init_url.find(".doc")!=-1:
                suf=".doc"
        if init_url.find(".html")!=-1:
            suf=".html"
        if init_url.find(".php")!=-1:
            suf=".php"
        if init_url.find(".xlsx")!=-1:
            suf=".xlsx"
        if init_url.find(".pdf")!=-1:
            suf=".pdf"
        if init_url.find(".aspx")!=-1:
            suf=".aspx"
        else:
            if init_url.find(".asp")!=-1:
                suf=".asp"
    print(suf)
    
    if (suf==".docx")|(suf==".doc")|(suf==".pdf")|(suf==".xlsx"):
        i=1
        while i<=1000:
            try:
                res=requests.get(init_url,headers=pre,timeout=10)
                break
            except:
                i+=1
                time.sleep(10)
        res.encoding = res.apparent_encoding
        with open(name+"\\content"+suf, 'wb') as f:
            f.write(res.content)
        fo = open(name+"\\suf.txt","w",encoding="utf-8")
        fo.write(suf)
        fo.close()
        urls=[]
        return urls
    i=1
    while i<=1000:
        try:
            res=requests.get(init_url,headers=pre,timeout=10)
            break
        except:
            i+=1
            time.sleep(10)
    res.raise_for_status
    rep=res.text
    
    fo = open(name+"\\suf.txt","w",encoding="utf-8")
    fo.write(suf)
    fo.close()
        
    fo = open(name+"\\content"+suf,"w",encoding="utf-8")
    fo.write(rep)
    fo.close()


    try:
        soup=BeautifulSoup(rep,"html.parser")
        urls=[]
        for link in soup.find_all('a'):
            if link.get('href'):
                urls.append(link.get('href'))
        new_urls = list(set(urls))
        print ('done')
        return new_urls
    except:
        print("failed to get")

def BFS(init_url):
    visited_name = open(".\\visited_urls.txt","w",encoding='utf-8')
    global cnt
    cnt = 1
    visited_urls.append(init_url)
    queue_urls.append(init_url)
    while len(queue_urls)>0:
        print (cnt)
        init_url = queue_urls.pop(0)
        visited_name.write(init_url+"\n")
        urls = find_urls(init_url)
        cnt=cnt+1
        for url in urls:
            if (url.find('mailto')!=-1)|(url.find("download.php?")!=-1)|(url.find(".doc")!=-1)|(url.find(".xlsx")!=-1):
                continue
            else:
                new_url = urljoin(init_url,url)
                new_url = new_url.replace("https:","http:")
                new_url = new_url.replace("convert_detail.php?","detail.php?")
                if(new_url.find("info.ruc.edu.cn")==-1):
                    continue
                if new_url not in visited_urls:
                    queue_urls.append(new_url)
                    visited_urls.append(new_url)
    visited_name.close()

print("Please input the host name you want to crawl(with \"https\"):")

BFS(input())
#BFS("https://info.ruc.edu.cn/userfiles/upload/f20170517024143922.pdf")
                    
                
    
