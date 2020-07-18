#!/usr/bin/env python3

import sys
import json
import os
import time
import urllib.error
from urllib import request, parse
from typing import List, Tuple

server = os.environ.get("SUBMIT_SERVER") or "http://aliyun-sh.menci.moe:54321"

def parse_arguments() -> Tuple[str, str]:
    url_list = [s for s in sys.argv if s.startswith("http://")]
    url = url_list[0] if len(url_list) else None
    student_id_list = [s for s in sys.argv if s.startswith("201") and len(s) == len("2019114514") and str(int(s) == s)]
    student_id = student_id_list[0] if len(student_id_list) else None

    if url is None or student_id is None:
        print("  Usage: ./client.py student_id your_url\nExample: ./client.py 2019114514 http://127.0.0.1:1234/abc")
        sys.exit(1)
    print("Your student ID is: %s\nYour search engine API URL is: %s" % (student_id, url))
    return url, student_id

def get_query_list() -> List[str]:
    try:
        data = request.urlopen(request.Request(server + "/query_list")).read()
        query_list = json.loads(data)
        print("Retrieved %d queries from server" % len(query_list))
        return query_list
    except urllib.error.URLError:
        print("Error communicating with the submit server!")
        exit(1)

def do_query(url: str, query: str) -> Tuple[List[str], float]:
    try:
        data = {"query": query}
        req = request.Request(url + "?" + parse.urlencode(data))

        start_time = time.monotonic()
        res = request.urlopen(req)
        end_time = time.monotonic()

        res_data: str = res.read().decode("utf-8").strip()

        return [url.strip() for url in res_data.strip().splitlines()], end_time - start_time
    except urllib.error.URLError:
        print("Error communicating with your web server, do you have a server running on %s?" % repr(url))
        exit(1)

def submit(student_id: str, cases: List[List[str]], average_time: float):
    print("Submitting your result to server")
    data = {"student_id": student_id, "cases": cases, "average_time": average_time}
    req = request.Request(server + "/submit", data=json.dumps(data).encode("utf-8"))
    result = json.loads(request.urlopen(req).read())
    if not result["success"]:
        print("Error submitting your result: " + result["error"])
        sys.exit(1)
    print("Your score is: " + str(result["score"]))

def main():
    url, student_id = parse_arguments()
    query_list = get_query_list()
    
    cases: List[List[str]] = []
    time_sum: float = 0
    for i in range(len(query_list)):
        results, time_used = do_query(url, query_list[i])
        print("Finished query %d/%d: time used = %f" % (i + 1, len(query_list), time_used), end="\r")
        cases.append(results)
        time_sum += time_used
    print("")
    
    average_time = time_sum / len(query_list)
    print("Your average time is: %f" % average_time)
    submit(student_id, cases, average_time)

main()
