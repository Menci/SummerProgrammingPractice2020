from os.path import dirname, join
from string import punctuation as punc_en
from zhon.hanzi import punctuation as punc_zh

import jieba
import re

jieba.load_userdict(join(dirname(__file__), 'user_dict.txt'))
stopwords = open(join(dirname(__file__), 'stopwords.txt'), 'r').read().split('\n')

def cut_words(line):
    words = []
    line = ''.join(c for c in line if c not in punc_en and c not in punc_zh)
    line = re.sub(r'\s+', ' ', line).strip()

    for tmp in line.split():
        for word in jieba.cut(tmp):
            if word not in stopwords:
                words.append(word)
    return words
