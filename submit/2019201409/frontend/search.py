
from LAC import LAC
import json
import os
import math
from collections import defaultdict
import time
import re

SrcEng = None
# ----------Begin of Arguments----------
# Location for dictionary file
USER_DICT = "../my_dict_upper.txt"

# Location for dumped index file
INDEX_DIR = "search_index.json"

# Location for parsed pages
PAGE_DATA_DIRECTORY = "../data/"

# A constant affecting accuracy
LENGTH_ALPHA = 0.25

# Length of snippet generated for user
SNIPPET_LENGTH = 150

# Location for stopwords
STOP_WORDS_DIR = "../crawler/cn_stopwords.txt"
# ----------End of Arguments----------

time_before_run = time.time()

# LAC
print("[INFO] Loading LAC")
lac = LAC(mode='seg')
lac.load_customization(USER_DICT, sep='\n')
print("[INFO] LAC Loaded")

STOP_WORDS = set()


def getStopwordsList():
    global STOP_WORDS
    with open(STOP_WORDS_DIR, "r") as f:
        for line in f.readlines():
            STOP_WORDS.add(line.strip('\n'))


def containNumber(word):
    if re.search("(19|20)\d{2}$", word) != None:
        return True
    elif re.search("\d{2}(年|届|次|等|轮|位|个|位|条|位|本|册)$", word) != None:
        return True
    else:
        return False


class SearchIndex:
    def __init__(self, data_directory):
        self.index = defaultdict(list)
        self.pageStorage = []
        self.data_dir = data_directory
        self.pageMap = []
        self.pageNum = 0

    def dumpjson(self):
        print("[INFO] Dumping data to ", INDEX_DIR)
        out = {}
        out["index"] = self.index
        out["pageStorage"] = self.pageStorage
        out["pageNum"] = self.pageNum
        with open(INDEX_DIR, "w") as f:
            strout = json.dumps(out)
            f.write(strout)
        print("[INFO] Data dumped to json.")

    def loadjson(self):
        print("[INFO] Loading data from ", INDEX_DIR)
        with open(INDEX_DIR, "r") as f:
            data = json.loads(f.read())
            self.index = data["index"]
            self.pageStorage = data["pageStorage"]
            self.pageNum = data["pageNum"]
            print("[INFO] Data loaded from json.")

    def processFile(self, data_file, fileid):
        data = {}
        with open(data_file, "r") as f:
            data_str = f.read()
            data = json.loads(data_str)
        self.pageStorage.append({
            'url': data['url'],
            'title': data['title'].strip(),
            'time': data['time'],
            'text': data['text']
        })
        factor = 1.0
        if ("academic_professor.php" in data['url']) or ("academic_research_lab.php" in data['url']) or ("overview_structure_dept.php" in data['url']):
            factor = 15
        if data['url'].strip().endswith("/"):
            factor = 100
        curdict = defaultdict(int)
        for word in data['words']:
            curdict[word] += 1
        self.pageMap.append(curdict)
        for key in curdict:
            if (key in data['title']) and (len(key) > 1):
                if factor > 1.0:
                    # id, tf(key, curdoc)
                    self.index[key].append(
                        [fileid, 1 + math.log(curdict[key] * factor * len(key))])
                elif containNumber(key):
                    self.index[key].append(
                        [fileid, 1 + math.log(curdict[key] * 10)])
                else:
                    self.index[key].append(
                        [fileid, 1 + math.log(curdict[key])])
            else:
                self.index[key].append([fileid, 1 + math.log(curdict[key])])

    def build(self):
        cidf = {}
        filenum = len([lists for lists in os.listdir(self.data_dir)])
        print("[INFO] ", filenum, "file(s) found in data directory")
        self.pageNum = filenum
        for fileid in range(filenum):
            self.processFile(self.data_dir + str(fileid) + ".json", fileid)
        # Calculate IDF for each term
        for key in self.index:
            cidf[key] = math.log(filenum / len(self.index[key]))
        # Calculate TF-IDF for each (term, doc)
        for fileid in range(filenum):
            # curtfidf = {}
            length = 0.0
            for term in self.pageMap[fileid]:
                val = cidf[term] * (1 + math.log(self.pageMap[fileid][term]))
                length += val * val
            self.pageStorage[fileid]['wlength'] = math.sqrt(length)

    def search(self, keywords, res_length):
        sco = {}
        sco = defaultdict(lambda: 0, sco)
        for keyword in keywords:
            if keyword not in self.index:
                continue
            cnt = 0
            for k2 in keywords:
                if k2 == keyword:
                    cnt += 1
            wtq = 1 + math.log(cnt)
            for pair in self.index[keyword]:
                sco[pair[0]] += pair[1] * wtq

        result_unsorted = [
            [sco[key] / (self.pageStorage[key]['wlength'] ** LENGTH_ALPHA), key] for key in sco]

        result_sorted = sorted(
            result_unsorted, key=lambda s: s[0], reverse=True)

        search_result = []
        for i in range(min(len(result_sorted), res_length)):
            search_result.append([
                self.pageStorage[result_sorted[i][1]]['title'],
                self.pageStorage[result_sorted[i][1]]['url'],
                self.pageStorage[result_sorted[i][1]]['time'],
                result_sorted[i][1],
                result_sorted[i][0],
            ])
        return search_result

    def query(self, keyword, res_length):
        keywords_raw = lac.run(keyword.upper())
        keywords = []
        for keyword in keywords_raw:
            if keyword not in STOP_WORDS:
                keywords.append(keyword)
        rawSearch = self.search(keywords, res_length)
        searchResult = []
        for res in rawSearch:
            cont = self.pageStorage[res[3]]['text']
            cont_str = ""
            min_res = 1000000000
            for sentence in cont:
                cont_str += sentence.strip()
            for word in keywords:
                pos = cont_str.find(word)
                if min_res > pos and pos >= 0:
                    min_res = pos
            if min_res == 1000000000:
                min_res = 0
            min_res -= 10
            if min_res < 0:
                min_res = 0
            if min_res == 0:
                summary = cont_str[min_res: min_res + SNIPPET_LENGTH]
            else:
                summary = '<small class=\"text-muted\">……</small>' + \
                    cont_str[min_res: min_res + SNIPPET_LENGTH]

            for word in keywords:
                summary = summary.replace(word, "<mark>" + word + "</mark>")

            if len(summary) == 0:
                summary = "<p><small class=\"text-muted\">Summary Not Available.</small></p>"
            elif len(cont_str) > min_res + SNIPPET_LENGTH:
                summary += '<small class=\"text-muted\">……</small>'

            if len(res[2]) == 0:
                res[2] = "Time not available."
            searchResult.append([res[0], res[1], res[2], summary])
        return searchResult

    def query_raw(self, keyword, res_length):
        keywords_raw = lac.run(keyword.upper())
        keywords = []
        for keyword in keywords_raw:
            if keyword not in STOP_WORDS:
                keywords.append(keyword)
        result = self.search(keywords, res_length)
        return result


def main():
    global SrcEng
    print("[INFO] Building Index for TF-IDF.")
    SrcEng = SearchIndex(PAGE_DATA_DIRECTORY)
    SrcEng.build()
    print("[INFO] Initialization of TF-IDF completed.")
    getStopwordsList()
    print("[INFO] Time elapsed:", time.time() - time_before_run)


def build_dump():
    global SrcEng
    print("[INFO] Building Index for TF-IDF.")
    SrcEng = SearchIndex(PAGE_DATA_DIRECTORY)
    SrcEng.build()
    print("[INFO] Initialization of TF-IDF completed.")
    SrcEng.dumpjson()
    getStopwordsList()
    print("[INFO] Time elapsed:", time.time() - time_before_run)


def build_load():
    global SrcEng
    SrcEng = SearchIndex(PAGE_DATA_DIRECTORY)
    SrcEng.loadjson()
    getStopwordsList()
    print("[INFO] Time elapsed:", time.time() - time_before_run)


# Use build_dump() on first run or after changing arguments, use build_load() later instead
# build_load()
build_dump()
