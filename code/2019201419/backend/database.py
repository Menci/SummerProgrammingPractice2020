from math import log10


class Database:
    def __init__(self, documents, keywords):
        self.documents = documents
        self.keywords = keywords


class Document:
    def __init__(self, url, title, length):
        self.url = url
        self.title = title
        self.length = length

        def calc(url):
            DELTA = 0.2
            white_list = ['academic_professor.php', 'overview_structure_dept.php', 'summerschool']
            black_list = ['list']

            ans = len(list(filter(lambda mode: url.find(mode) != -1, white_list))) - \
                len(list(filter(lambda mode: url.find(mode) != -1, black_list)))

            return ans * DELTA

        self.weight = calc(url.lower())


class Keyword:
    def __init__(self, word):
        self.word = word
        self.occurs = []
        self.idf = 0


class KeywordInDoc:
    def __init__(self, doc_id, frequency_t, frequency_c):
        self.doc_id = doc_id
        calc = lambda f : 0 if f == 0 else 1 + log10(f)
        self.tf = 0.8 * calc(frequency_t) + 0.2 * calc(frequency_c)
        self.suffix_max = self.tf
