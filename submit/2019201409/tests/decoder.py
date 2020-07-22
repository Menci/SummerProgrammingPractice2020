import json

with open("../data/100.json", "r") as f:
    s = f.read()
    text = json.loads(s)
    print(text)