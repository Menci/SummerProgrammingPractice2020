# crawler with multi_thread and parser

from bs4 import BeautifulSoup
import threading
import requests
import queue
import time
from parser import myHtmlParser
from parser import myUrlParser
from ess import *
from arguments import *

maxDepth = 128
maxThread = 64
sleepTime = 0

depth = {}
texthasher = set()
Q = queue.Queue(0)

# multi_thread
class myThread (threading.Thread):
    def __init__(self, url):
        threading.Thread.__init__(self)
        self.url = url
        
    def run(self):
    # get request
        flag = 1
        while flag > 0:
            try:
                req = requests.get(self.url)
                flag = 0
            except:
                if(flag % 3 == 1):
                    print("An error occured on %s. Now retrying..."%self.name)
                flag += 1
        
    # parser
        if "html" not in req.text:    #http://info.ruc.edu.cn/download.php?id=10
            return
        if req.text in texthasher:
            return
        else:
            texthasher.add(req.text)
        
        soup = BeautifulSoup(req.text, "html.parser")
        fileName = encrypt(self.url)
        
        f1 = open(rawhtmlDir + fileName, mode = "w")
        f1.write(req.text)
        f1.close()
        
    # bfs framework
        if depth[self.url] < maxDepth:
            urls = soup.find_all("a", href = True)
            for each in urls:
                url = myUrlParser(base = self.url, url = each.get("href"))
                
                if url != None and url not in depth:
                    Q.put(url)
                    depth[url] = depth[self.url] + 1
        
        time.sleep(sleepTime)


def bfs():
    Q.put(root)
    depth[root] = 1
    total = 0

    basicThreadCount = threading.active_count()
    while Q.empty() == False or threading.active_count() > basicThreadCount:

        while threading.active_count() == maxThread:
            continue
        while Q.empty() == True and threading.active_count() > basicThreadCount:
            continue
        if Q.empty() == True:
            break
        
        t = myThread(Q.get())
        t.start()
        total += 1
        if(total % 100 == 0):
            print("%s%d"%("." * (40 - len(str(total))), total))
        
    print("Total: %d"%total)

    
if __name__ == "__main__":
    print("Now start crawler.py")
    chkDir(rawhtmlDir)
    bfs()

