from bs4 import BeautifulSoup, NavigableString, Tag, Comment
from urllib.parse import urlparse
from urllib.parse import urljoin
from urllib.parse import urlunparse
from posixpath import normpath

import os
from ess import *
from arguments import *

id_filter = {"top", "child_menu", "footer"}
name_filter = {"script", "None"}
suffix_filter = {".css", ".js", ".png", ".jpg", ".bmp", ".gif", ".jpeg", ".ico", ".avi", ".mp3", ".mp4", ".xls", ".flv", ".doc", ".ppt", ".xlsx", ".docx", ".pptx", ".pdf", ".rar", ".zip", ".7z"}
class_filter = {"side_bar"}

        
def tagchecker(tag):
    if "class" in tag.attrs:
        for each in tag["class"]: # tag["class"]: list
            if each in class_filter:
                return True
    if "id" in tag.attrs:
        if str(tag["id"]) in id_filter:
            return True
    if str(tag.name) in name_filter:
        return True
    return False

        
def myHtmlParser(soup, f):
    for child in soup.find_all(tagchecker):
        child.decompose()
        
    string = soup.get_text()
    if(type(string) != type(None)):
        if(str(string).strip() != ""):
            f.write(str(string).strip())
            f.write(" ") 


def myJoin(base, url):
    arr = urlparse(urljoin(base, url))
    return urlunparse((arr.scheme, arr.netloc, normpath(arr[2]), arr.params, arr.query, arr.fragment))

def myUrlParser(base, url):
    if(url == ""):
        return None 
    elif os.path.splitext(url)[-1] in suffix_filter:
        return None
        
    if url[0] == "/":
        url = root + url[1:]
    url = myJoin(base, url)
    if root not in url: # or "keyword.php?name=" in url:
        return None
    return url.split("#")[0]

    
if __name__ == "__main__":
    print("Now start parser.py")
    chkDir(rawtitleDir)
    chkDir(rawtextDir)
    
    total = 0
    for filename in os.listdir(rawhtmlDir):
        f1 = open(rawhtmlDir + filename, mode = "r")
        f2 = open(rawtextDir + filename, mode = "w")
        f3 = open(rawtitleDir + filename, mode = "w")
        
        soup = BeautifulSoup(f1.read(), "html.parser") # https://beautifulsoup.readthedocs.io/zh_CN/v4.4.0/index.html#id15 important details
        try:
            f3.write(str(soup.head.title.string).strip())   
            myHtmlParser(soup, f2)
        except:
            print("Error found in:", decrypt(filename))  
        
        f1.close()
        f2.close()
        f3.close()
        total += 1
        if(total % 100 == 0):
            print("%s%d"%("." * (40 - len(str(total))), total))
        
    print("Total: %d"%total)
    

'''
def writeStr(string, f):
    if(type(string) != type(None)):
        if(str(string).strip() != ""):
            f.write(str(string).strip())
            f.write(" ") 

def myHtmlParser_old(soup, Text):
    # Text = os.sys.stdout #
    try:
        for child in soup.body.contents:
            if type(child) == Comment:
                continue
            elif type(child) == NavigableString:
                writeStr(child.string, Text)
            else:
                if child.has_attr("id"):
                    if str(child["id"]) in id_filter:
                        continue
                for child2 in child.descendants:
                    # writeStr(str(type(child2.name)), Text) #
                    # writeStr(str(child2.name), Text) #
                    if str(child2.name) in name_filter:
                        continue
                    if type(child2) != Comment and type(child2) != NavigableString:
                        if child2.has_attr("class"):
                            if str(child2["class"]) in class_filter:
                                continue
                    writeStr(child2.string, Text)
    except Exception as e:
        print("Exception found on HtmlParser.")
        print(repr(e))
'''
