# !/usr/bin/python3
# _*_ coding: utf-8 _*_

import threading
import requests
import time
import re
from queue import Queue
from urllib import parse

# ---------- Arguments ----------
DATA_DIR = "./data/"

THREAD_LIMIT = 32
# Maximum thread limit

DEPTH_LIMIT = 1000
# Maximum depth limit

FAILED_REQUESTS_COUNTER = 0
# Number of failed requests

SUCCESSFUL_REQUESTS_COUNTER = 0

TIMEOUT_RETRY_LIMIT = 1.5
# Maximum times of retrying

TIMEOUT_LIMIT = 5
# Maximum time of each retry

SLEEP_TIME = 0
# Sleep time after each request

BLACKLISTED_FILES = [
    ".rar", ".zip", ".7z", ".tar"
    ".mp3", ".mp4", ".avi", ".flv", ".wav",
    ".css", ".js", ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".ico",
    ".doc", ".docx", ".ppt", ".pptx", ".xls", ".xlsx", ".pdf",
    "download", "upload"
]
# Ignoring any URL containing any of these words

# ---------- End of Arguments ----------


startTime = time.time()
seedURL = "http://info.ruc.edu.cn"
URLList = []
URLDict = {}
URLInQueue = set()
URLDone = set()
URLCount = 0
failedRequests = []
requestHeaders = {
    "User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36 ORZBot"
}

def isURLAllowed(url):
    s = str(url).lower()
    if (s.find("info.ruc.edu.cn") != -1) and (url not in URLInQueue) and (url not in URLDone):
        return True
    else:
        return False

class crawlerThread(threading.Thread):
    def __init__(self, queue, threadID, lock):
        threading.Thread.__init__(self)
        self.urlqueue = queue
        self.threadID = threadID
        self.lock = lock

    def getURL(self, url):
        s = str(url).lower()
        for word in BLACKLISTED_FILES:
            if word in s:
                print("Blacklisted File, Skipping...")
                return None
        
        global TIMEOUT_LIMIT
        global FAILED_REQUESTS_COUNTER
        try:
            req = requests.get(url = url, headers = requestHeaders, timeout = TIMEOUT_LIMIT)
            return req
        except requests.exceptions.Timeout:
            global TIMEOUT_RETRY_LIMIT
            for i in range(TIMEOUT_RETRY_LIMIT):
                print("Retry #", i, url)
                req = requests.get(url = url, headers = requestHeaders, timeout = TIMEOUT_LIMIT)
                if req.status_code == 200 or req.status_code == 404:
                    return req
            
            FAILED_REQUESTS_COUNTER = FAILED_REQUESTS_COUNTER + 1
            failedRequests.append(url)
            print("Error Retrying", url)
            return None
        except:
            FAILED_REQUESTS_COUNTER = FAILED_REQUESTS_COUNTER + 1
            failedRequests.append(url)
            print("Error Getting", url)
            return None

    def workURL(self, url):
        
        req = self.getURL(url)

        if url in URLDone:
            return []
        if req == None:
            return []
        if req.status_code != 200 and req.status_code != 201:
            return []
        cont = req.text
        urls = re.findall(r'href=[\'"]?([^\'" >]+)', cont)
        cid = URLDict[url]
        with open(DATA_DIR + str(cid), "w") as f:
            global SUCCESSFUL_REQUESTS_COUNTER
            SUCCESSFUL_REQUESTS_COUNTER = SUCCESSFUL_REQUESTS_COUNTER + 1
            f.write(str(req.text))
        ret = []
        for link in urls:
            urlstr = link
            if(urlstr == None):
                continue
            combinedURL = parse.urljoin(url, urlstr)
            if isURLAllowed(combinedURL):
                ret.append(combinedURL)
        return ret


    def run(self):
        global SLEEP_TIME
        while True:
            elem = self.urlqueue.get()
            time.sleep(SLEEP_TIME)
            cdepth = elem[0]
            curl = elem[1]
            with self.lock:
                URLList.append(curl)
                global URLCount
                URLDict[curl] = URLCount
                global SUCCESSFUL_REQUESTS_COUNTER
                print("#", URLCount, ", ", curl, SUCCESSFUL_REQUESTS_COUNTER)
                URLCount = URLCount + 1

            newURLs = self.workURL(curl)

            URLDone.add(curl)
            
            if cdepth < DEPTH_LIMIT:
                # print(newURLs)
                with self.lock:
                    for newURL in newURLs:
                        if newURL not in URLInQueue:
                            URLInQueue.add(newURL)
                            self.urlqueue.put([cdepth + 1,newURL])
                        
            self.urlqueue.task_done();


def main():
    URLQueue = Queue()
    URLQueue.put([0, seedURL])
    URLInQueue.add(seedURL)

    lock = threading.Lock()
    for i in range(THREAD_LIMIT):
        th = crawlerThread(URLQueue, i, lock)
        th.setDaemon(True)
        th.start()

    URLQueue.join()

    print("Failed Counter", FAILED_REQUESTS_COUNTER)
    for i in range(FAILED_REQUESTS_COUNTER):
        print(failedRequests[i])
    with open("filemap", "w") as f:
        for URL in URLList:
            f.write(str(URL) + "\n")
main()
