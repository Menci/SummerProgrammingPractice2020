from hashlib import md5
from math import sqrt
from pickle import load
from time import time

import imp
import heapq

print('Loading Database Files.....')
st = time()

db = imp.load_source('database', 'backend/database.py')
database = load(open('local_test_data/index.db', 'rb'))

Documents = database.documents
Keywords = database.keywords

N = len(Documents)

cut_words = imp.load_source('ultility', 'backend/ultility.py').cut_words

print(F'Done. Time used: {time() - st} s.')


class SearchResult:
    def __init__(self, doc: db.Document, score, snipped):
        self.title = doc.title
        self.url = doc.url
        self.snipped = snipped
        self.score = score


def process(words):
    prod = [0 for i in range(N)]
    norm = [0 for i in range(N)]
    norm_q = 0
    for word in words:
        norm_q += Keywords[word].idf ** 2
        for occur in Keywords[word].occurs:
            prod[occur.doc_id] += Keywords[word].idf * occur.tf
            norm[occur.doc_id] += occur.tf ** 2
    dist = [(prod[i] / sqrt(norm[i] * norm_q) + Documents[i].weight, i)
            for i in range(N) if norm[i] != 0]
    dist.sort(reverse=True)
    return dist[:100]


def get_snipped(file_name, words):
    with open(F'local_test_data/web_content/{file_name}.txt', 'r') as f:
        content = ' '.join(f.readlines()[4:])
        f.close()
    min_pos = 2147483647
    for word in words:
        cur = content.find(word)
        if cur != -1:
            min_pos = min(min_pos, cur)
    content = content[max(0, min_pos - 6):min_pos + 256]
    for word in words:
        content = content.replace(word, '<em>' + word + '</em>')
    return content


def do_search(input_str: str, auto=False):
    input_str = input_str.strip()
    input_words = list(filter(lambda x: x in Keywords, cut_words(input_str)))
    tmp = process(input_words)

    result = []
    if not auto:
        for (score, doc_id) in tmp:
            file_name = md5(Documents[doc_id].url.encode('utf-8')).hexdigest()
            result.append(SearchResult(
                Documents[doc_id],
                score,
                get_snipped(file_name, input_words)
            ))
    else:
        for (score, doc_id) in tmp:
            result.append(Documents[doc_id].url)
    return result
