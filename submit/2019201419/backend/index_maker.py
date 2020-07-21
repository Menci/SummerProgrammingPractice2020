from math import log10, ceil
from sys import stdout

from database import Document, Keyword, KeywordInDoc, Database
from ultility import cut_words

import os
import pickle

Documents = []
Keywords = {}


def process(input_file):
    words = []
    with open(input_file, 'r', encoding='utf-8') as inf:
        url = inf.readline()[5:].strip()
        title = inf.readline()[7:].strip()
        lines = inf.readlines()[3:]
        if len(lines) > 0:
            for line in lines:
                words += cut_words(line)
    return (url, title, cut_words(title), words)


def report(portion, total):
    part = total / 50
    count = ceil(portion / part)
    stdout.write('\r')
    stdout.write(F"[{'>' * count}{'-' * (50 - count)}] ({portion}/{total})")
    stdout.flush()

    if portion >= total:
        stdout.write('\n')
        stdout.flush()


if __name__ == "__main__":
    doc_dir = 'local_test_data/web_content'
    total = len(os.listdir(doc_dir))
    doc_cnt = 0
    doc_tmp = []

    stdout.write('Loading Files:\n')
    stdout.flush()
    for file_name in os.listdir(doc_dir):
        if not file_name.endswith('.txt'):
            continue
        (url, title, title_words, content_words) = process(F'{doc_dir}/{file_name}')
        if len(content_words) != 0:
            doc_tmp.append((url, title, title_words, content_words))
        doc_cnt += 1
        report(doc_cnt, total)

    stdout.write('Analysing Files:\n')
    stdout.flush()
    for doc_id in range(len(doc_tmp)):
        (url, title, title_words, content_words) = doc_tmp[doc_id]
        Documents.append(Document(url, title, len(title_words) + len(content_words)))

        words = title_words + content_words

        for word in words:
            if word not in Keywords:
                Keywords[word] = Keyword(word)

            if len(Keywords[word].occurs) > 0 and Keywords[word].occurs[-1].doc_id == doc_id:
                continue

            Keywords[word].occurs.append(
                KeywordInDoc(
                    doc_id, 
                    title_words.count(word) / len(title_words) * 500, 
                    content_words.count(word) / len(content_words) * 500
                )
            )

        report(doc_id + 1, len(doc_tmp))

    for word in Keywords:
        Keywords[word].idf = log10(len(Documents) / len(Keywords[word].occurs))
        for i in range(len(Keywords[word].occurs) - 2, -1, -1):
            if Keywords[word].occurs[i + 1].suffix_max >= Keywords[word].occurs[i].tf:
                Keywords[word].occurs[i].suffix_max = Keywords[word].occurs[i + 1].suffix_max

    db_file = open('local_test_data/index.db', 'wb')
    pickle.dump(Database(Documents, Keywords), db_file)
