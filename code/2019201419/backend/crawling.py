from bs4 import BeautifulSoup
from hashlib import md5
from queue import Queue
from redis import StrictRedis
from string import punctuation as punc_en
from time import sleep
from urllib.error import HTTPError
from urllib.parse import urljoin, urlparse, quote
from urllib.request import urlopen

import os
import re
import threading


cnt = 0
MAX_PAGE_CNT = 10000
MAX_TRY_PER_PAGE = 3


def page_parser(html_code, url: str):
    soup = BeautifulSoup(html_code, 'html.parser')
    urls = []

    if not os.path.exists('local_test_data'):
        os.mkdir('local_test_data')

    if not os.path.exists('local_test_data/web_content'):
        os.mkdir('local_test_data/web_content')
    file_name = md5(url.encode('utf-8')).hexdigest()
    with open(F'local_test_data/web_content/{file_name}.txt', 'w') as f:
        print('URL:', url, file=f)
        print('TITLE:', soup.title.string if soup.title else '', file=f)
        print('', file=f)
        print('========== CONTENT ==========', file=f)
        
        if soup:
            for s in soup.find_all(['script', 'img', 'embed', 'link', 'style']):
                s.decompose()
            for s in soup.find_all():
                if s.has_attr('href'):
                    if s['href'] != '' and s['href'][0] != '#':
                        urls.append(s['href'])

            text = re.sub('\n+', '\n', soup.text).strip()
            text = re.sub(r'\s{2,}', ' ', text)
            print(text, file=f)

    # if not os.path.exists('local_test_data/web_data'):
    #     os.mkdir('local_test_data/web_data')
    # with open(F'local_test_data/web_data/{file_name}.html', 'w') as f:
    #     print(soup.prettify(), file=f)

    return urls


def should_be_accessed(url):
    res = urlparse(url)
    return res.netloc == 'info.ruc.edu.cn' and res.scheme == 'http'


def BFS(q, visited, fail_sites):
    global cnt, MAX_TRY_PER_PAGE, MAX_PAGE_CNT
    fail_cnt = 0
    while not q.empty() and cnt <= MAX_PAGE_CNT:
        cur = quote(q.get(), safe=punc_en, encoding=None, errors=None)
        if visited.exists(cur) and visited[cur] != 'Failed':
            continue
        visited.set(cur, 'In try.')

        cnt += 1
        print(F'#{cnt} Fetching {cur}')

        while fail_cnt < MAX_TRY_PER_PAGE:
            try:
                req = urlopen(cur, timeout=2)
                if not req.headers['Content-Type'].startswith('text/html'):
                    url_list = []
                else:
                    html_code = req.read().decode('utf-8')
                    url_list = page_parser(html_code, cur)
            except HTTPError as e:
                if e.code == 404:
                    visited.set(cur, 'Done')
                    url_list = []
                    break
                else:
                    fail_cnt += 1
            except Exception as e:
                fail_cnt += 1
            else:
                visited.set(cur, 'Done')
                break

        if fail_cnt >= MAX_TRY_PER_PAGE:
            if cur not in fail_sites:
                fail_sites[cur] = 0
            if fail_sites[cur] < MAX_TRY_PER_PAGE:
                fail_sites[cur] += 1
                print(F'\nFetching {cur} failed. Try again later.')
                q.put(cur)
            else:
                print(F'\nFetching {cur} failed.')
            visited.set(cur, 'Failed')
            fail_cnt = 0
            continue
        else:
            fail_sites.pop(cur) if cur in fail_sites else None

        for url in url_list:
            abs_url = urljoin(cur, url)
            if not should_be_accessed(abs_url) or abs_url in visited:
                continue
            q.put(abs_url)

        sleep(2)


def crawling(root_url, thread_num, reset):
    q = Queue()
    fail_sites = {}

    try:
        f = open('local_test_data/todo_list.txt', 'r')
    except IOError:
        q.put(root_url)
    else:
        while True:
            ss = f.readline()
            if not ss:
                break
            if ss[-1] == '\n':
                ss = ss[:-1]
            ss = quote(ss, safe=punc_en, encoding=None, errors=None)
            q.put(ss)
        f.close()

    visited = StrictRedis(host='localhost', port=6379, decode_responses=True)
    if reset:
        visited.flushall()
    else:
        for key in visited.keys():
            if visited[key] != 'Done' and visited[key] != 'Failed':
                visited.set(key, 'Failed', xx=True)

    if thread_num == 1:
        BFS(q, visited, fail_sites)
    else:
        threads = [threading.Thread(target=BFS, args=(q, visited, fail_sites, ))
                   for i in range(thread_num)]

        threads[0].setDaemon(True)
        threads[0].start()
        sleep(4)
        for td in threads[1:]:
            td.setDaemon(True)
            td.start()
        for td in threads:
            td.join()

    fail_arr = []
    if not q.empty() or len(fail_sites.keys()) > 0:
        while not q.empty():
            fail_arr.append(q.get())
        for cur in fail_sites.keys():
            fail_arr.append(cur)

    return fail_arr


if __name__ == "__main__":
    flag = input('Clear all data in the database? (Y/N, N by default)') == 'Y'
    fail_sites = crawling('http://info.ruc.edu.cn/', 32, flag)

    if len(fail_sites) > 0:
        if not os.path.exists('local_test_data'):
            os.mkdir('local_test_data')
        with open('local_test_data/todo_list.txt', 'w') as f:
            for cur in fail_sites:
                print(cur, file=f)
        print(F'Please try to get pages listed in local_test_data/todo_list.txt again.')
        exit(1)
    else:
        if os.path.exists('local_test_data/todo_list.txt'):
            os.remove('local_test_data/todo_list.txt')
        print('Done.')
