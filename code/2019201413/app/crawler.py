import re
import os
import sys
import time
import urllib.request
import urllib.parse
from collections import deque

fprintpt = re.compile('.*\/')

def fprint(info, filename, wtype = 'w'):
    global pathfile
    if filename[0] == '/':
        filename = filename[1:]
    filename = 'source/pages/' + filename
    filepath = fprintpt.match(filename)
    if filepath != None and not os.path.exists(filepath.group()):
        os.makedirs(filepath.group())
    if os.path.exists(filename):
        filename = filename + "_index_page"
    f = open(filename, wtype)
    print(info, file = f)
    print(filename[12:], file = pathfile)
    f.close()

def getpages(url):
    global pathfile
    pathfile = open('source/file.txt', 'w')
    queue = deque()
    vis = set()

    cnt = 1
    vis |= {url}
    queue.append(url)
    
    while queue:
        curl = queue.popleft()
        print("GET : " + curl + " , total " + str(cnt))
        cnt += 1
        try:
            response = urllib.request.urlopen(curl, timeout = 2)
        except:
            print("An error occurr when opening url : " + curl)
            fprint(curl + " : open error", "log.txt", 'a')
            continue

        if 'html' not in response.getheader('Content-Type'):
            continue
        try:
            data = response.read().decode('utf-8')
        except:
            print("An error occur when decoding.")
            fprint(curl + " : decode error", "log.txt", 'a')
            continue
        if len(curl) > len(url):
            fprint(data, curl[len(url):])

        link = re.compile('href="((.(?!png)(?!css)(?!jpg)(?!@))+?)"')
        for result in link.findall(data):
            if 'http' in result[0]:
                if url not in result[0]:
                    continue
                turl = result[0]
            else:
                turl = url + '/' + result[0]
            if turl not in vis:
                queue.append(turl)
                vis |= {turl}
    pathfile.close()
