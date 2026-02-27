import json
with open("sample-data.json", "r") as openfile:
    data = json.load(openfile)

print(data)