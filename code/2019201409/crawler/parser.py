# !/usr/bin/python3
# _*_ coding: utf-8 _*_

from bs4 import BeautifulSoup, Comment
# import hanlp
import pkuseg
import json
import time

USER_DICT = '../my_dict_upper.txt'
# Dictionary of entities for LAC, generated with HanLP, jieba and pkuseg.


print("[INFO] Loading LAC")
from LAC import LAC
lac = LAC(mode = 'seg')
lac.load_customization(USER_DICT, sep = '\n')

print("[INFO] LAC Loaded")

# Location for raw data
DATA_DIR = "./data/"

# Location for filemap
FILEMAP_DIR = "./filemap"

# Location for output Files
OUTPUT_DIR = "../data/"

# Ignore strings containing:
BLACKLISTED_STRINGS = [
    "您所在的位置", "分享到：", "公众微信二维码", "Copyright ©", "版权所有", "北京市海淀区中关村大街59号", "邮编：100872", 
    "技术支持：", "传真：", "浏览量", "新闻类型",
    "color:" , "text-decoration:",
    "\n", "upload", "   ", "\t"
]

# Filter pages with url containing:
BLACKLISTED_PAGES = [
    "_list.php", "academic_faculty", "internation_info.php", "education_notice.php"
]

STOP_WORDS = set()

titleSet = set()

def getStopwordsList():
    global STOP_WORDS
    with open("cn_stopwords.txt", "r") as f:
        # STOP_WORDS = [line.strip() for line in f.readlines()]
        for line in f.readlines():
            STOP_WORDS.add(line.strip('\n').upper())

class RawHTMLParser:
    def __init__(self, content, fileid, validfileid, fileurl):
        self.content = content
        self.fileid = fileid
        self.title = ""
        self.time = ""
        self.url = fileurl
        self.oldID = fileid
        self.newID = validfileid
        self.plainText = []
        self.processed = []
    
    def stringAllowed(self, st):
        for blk in BLACKLISTED_STRINGS:
            if blk in st:
                return False
        return True



    def parseHTML(self):
        soup = BeautifulSoup(self.content, 'html.parser')

        # Binary files, Non-html files
        if soup.body == None:
            return
        
        # Skip blacklisted pages
        for item in BLACKLISTED_PAGES:
            if item in self.url:
                return

        # Remove all scripts
        for sc in soup.select('script'):
            sc.extract()

        # Remove all links
        for sc in soup.select('a'):
            sc.extract()
        
        # Remove all comments
        for sc in soup(text=lambda text: isinstance(text, Comment)):
            sc.extract()
        findres = soup.find("div", {"id": "main"})

        # Binary files, Non-html files
        if soup.body == None:
            return

        # Find text & output
        text = soup.body.find_all(text = True)
        self.title = soup.head.title.text.replace(' - 中国人民大学信息学院', '')
        resultStrings = []

        title_processed = lac.run(self.title.upper().strip())
        for word in title_processed:
            if word not in STOP_WORDS:
                self.processed.append(word)
        for i in text:
            istr = i.strip()
            if "发布时间：" in istr:
                self.time = istr
            elif len(istr) > 1 and self.stringAllowed(istr):
                resultStrings.append(istr.upper())
        self.plainText = resultStrings
        self.time = self.time.replace('发布时间：', '')

        if len(resultStrings) == 0:
            return
        cutall = lac.run(resultStrings)
        for cutres in cutall:
            for curword in cutres:
                cs = curword.strip()
                if cs not in STOP_WORDS:
                    self.processed.append(cs)


    def dump(self):
        with open(OUTPUT_DIR + str(self.newID) + ".json", "w") as f:
            djson = json.dumps({
                "url": self.url,
                "id": self.newID,
                "title":self.title,
                "time": self.time, 
                "text": self.plainText, 
                "words":self.processed
                })
            f.write(djson)



def main():
    with open(FILEMAP_DIR, "r") as fmp:
        filemap = fmp.readlines()
        fileid = 0
        validfileid = 0
        time2 = time.time()
        for i in filemap:
            try:
                with open(DATA_DIR + str(fileid), "r") as fpage:
                    cont = fpage.read()
                    rp = RawHTMLParser(cont, fileid, validfileid, i.strip())
                    rp.parseHTML()
                    cur_text = ""
                    for word in rp.plainText:
                        wst = word.strip()
                        ignoreWord = False
                        for badword in BLACKLISTED_STRINGS:
                            if badword in wst:
                                ignoreWord = True
                                break
                        if ignoreWord == False:
                            cur_text += wst
                    # Filter duplicated pages
                    rp.token = hash(cur_text)
                    if rp.token in titleSet:
                        print("[BAD] File", fileid, "is duplicated.")
                    if len(rp.plainText) > 0 and rp.token not in titleSet:
                        rp.dump()
                        titleSet.add(rp.token)
                        validfileid = validfileid + 1
            except FileNotFoundError:
                pass
                print("[BAD] File", fileid, "doesn't exist.")
            else:
                pass
                print("[OK] #{id}  Time={tim:.2f}s, {pgs:.2f}Page/Sec".format(id = fileid, tim = time.time() - time2, pgs = (fileid + 1) / (time.time() - time2)))
            fileid += 1
    
main()