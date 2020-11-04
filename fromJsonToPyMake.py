import json

with open("make.json", "r+") as f:
    data = json.load(f)
    for e in data:
        data[e] = dict(command=["echo " + e], depend=data[e])
    print(data)
    f.seek(0, 0 )
    json.dump(data, f)
    f.truncate()