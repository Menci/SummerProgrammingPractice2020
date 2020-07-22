import requests
import json
import time

LOCAL_SERVER_ADDR = "http://127.0.0.1:2333/query"

TEST_DATA_LOCATION = "./query.json"

def run_test():
    time0 = time.time()
    ans = []
    totalrank = 0
    callback = 0
    with open(TEST_DATA_LOCATION, "r") as f:
        testcases = json.loads(f.read())
        for test in testcases:
            req = requests.get(url = LOCAL_SERVER_ADDR, params = {"word" : test[0]})
            strng = req.text.strip().replace(' ', '').replace('\n', '')
            data = json.loads(strng)
            rnk = 0
            found = False
            for url in data:
                if url == test[1]:
                    found = True
                    break
                else:
                    rnk += 1
            callback += found
            if found == False:
                print(test)

            else:
                print(rnk, test)
                ans.append(rnk)
                totalrank += 1 / (rnk + 1)
    time1 = time.time()
    print("Time Elapsed:", time1 - time0)
    print("Callback Rate =", callback, ", Avg. Rank = ", totalrank / callback)
    print(totalrank, callback)

run_test()