#!/usr/bin/env python3

from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Dict, List, Optional
import json
import sqlite3
import pickle
import datetime

allowed_result_count = 100

database = sqlite3.connect("server_data/database.db")
database.execute('''
    CREATE TABLE IF NOT EXISTS data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        submit_time TEXT,
        client_ip TEXT,
        student_id TEXT,
        avarage_time REAL,
        score REAL,
        indexes TEXT,
        raw_cases TEXT
    )
''')

student_id_list = open("server_data/student_id_list").read().splitlines()
testdata = [s.split(" ", 1) for s in open("server_data/testdata").read().splitlines()]
query_list = [x[1] for x in testdata]
query_count = len(testdata)

print("Loading data")
urls: List[str] = pickle.load(open("server_data/urls.bin", "rb"))
sim = pickle.load(open("server_data/sim.bin", "rb"))

def normalize_url(url: str) -> str:
    if url.endswith("/"):
        url = url[:-1]
    return url

url_id: Dict[str, int] = {normalize_url(urls[i]): i for i in range(len(urls))}

def url_to_id(url: str) -> Optional[int]:
    return url_id.get(normalize_url(url))

def check_sim(url1: str, url2: str) -> bool:
    id1 = url_to_id(url1)
    id2 = url_to_id(url2)
    if id1 is None or id2 is None:
        return False
    if id1 == id2:
        return True
    if id1 > id2:
        id1, id2 = id2, id1
    return sim[id1][id2] > 0.9

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/query_list":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(query_list).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/submit":
            try:
                request_body = self.rfile.read(int(self.headers.get("content-length")))
                data = json.loads(request_body)
                if type(data) != dict:
                    raise Exception("Invalid data type: %s, expected %s" % (repr(type(data)), repr(dict)))
                if data.get("student_id") not in student_id_list:
                    raise Exception("Invalid student id: " + repr(data.get("student_id")))
                if type(data.get("cases")) != list:
                    raise Exception("Invalid data.cases type: %s, expected %s" % (repr(type(data.get("cases"))), repr(list)))
                if len(data.get("cases")) != query_count:
                    raise Exception("Invalid testdata length: %d, expected %d" % (len(data.get("cases")), query_count))
                for i in range(query_count):
                    if type(data.get("cases")[i]) != list:
                        raise Exception("Invalid data.cases[%d] type: %s, expected %s" % (i, repr(type(data.get("cases")[i])), repr(list)))
                    if len(data.get("cases")[i]) > allowed_result_count:
                        raise Exception("Too many results for data.cases[%d], the maximum allowed is %d" % (i, allowed_result_count))
                    for s in data.get("cases")[i]:
                        if type(s) != str:
                            raise Exception("Invalid data.cases[%d][%d] type: %s, expected %s" % (repr(type(s)), repr(str)))
                        if len(s) > 1024:
                            raise Exception("Url too long: %s" % repr(s))
                if type(data.get("average_time")) not in [int, float]:
                    raise Exception("Invalid data.average_time type: %s, expected %s or %s" % (repr(type(data.get("avarage_time"))), repr(int), repr(float)))
                
                indexes: List[float] = []
                for i in range(query_count):
                    query_result: List[str] = data.get("cases")[i]
                    index = -1
                    for j in range(len(query_result)):
                        if check_sim(query_result[j], testdata[i][0]):
                            index = j + 1
                            break
                    indexes.append(index)

                score: float = 0
                for index in indexes:
                    if index != -1:
                        score += 1 / index

                database.execute("INSERT INTO data (student_id, submit_time, client_ip, avarage_time, score, indexes, raw_cases) VALUES (?, ?, ?, ?, ?, ?, ?)", (
                    data.get("student_id"),
                    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    self.client_address[0],
                    data.get("average_time"),
                    score,
                    json.dumps(indexes),
                    json.dumps(data.get("cases"))
                ))
                database.commit()

                print("%s submitted: score = %f, average_time = %f" % (data.get("student_id"), score, float(data.get("average_time"))))

                self.send_response(200)
                self.end_headers()
                self.wfile.write(json.dumps({"success": True, "ip": self.client_address[0]}).encode("utf-8"))
            except Exception as e:
                self.send_response(200)
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

server = HTTPServer(("0.0.0.0", 54321), Handler)
print("Server started")
server.serve_forever()
