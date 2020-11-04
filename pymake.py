import json
import random
import hashlib
import os
import sys
from collections import deque
import shutil

def tp_sort(graph):
    order, enter, state = deque(), set(graph), {}
    def dfs(node):
        state[node] = 0
        q = graph.get(node, ())
        for k in q.get("depend"):
            sk = state.get(k, None)
            if sk == 0: raise ValueError("cycle")
            if sk == 1: continue
            enter.discard(k)
            dfs(k)
        order.appendleft(node)
        state[node] = 1  
    while enter: 
        dfs(enter.pop())
    order.reverse()
    return order

def add_hash_db(package, content):
    with open("database.json", 'r+') as f:
        data = json.load(f)
        object_hash = hashlib.sha1(content.encode())
        data[package]["hash"] = object_hash.hexdigest()
        f.seek(0, 0)
        json.dump(data, f)
        f.truncate()

def init_db(data):
    with open("database.json", "r+") as f:
        try:
            db = json.load(f)
        except:
            db = {}
        for i in data:
            try:
                if db[i]['hash'] is not None:
                    data[i]['hash'] = db[i]['hash']
            except:
                data[i]["hash"] = ""
        f.seek(0, 0 )
        json.dump(data, f)
        f.truncate()
        
def run(package, need):
    with open("database.json", ) as f:
        db = json.load(f)

    hs = db[package]["hash"]

    with open("py_make_file", 'r' ) as f:
        data = json.load(f)
        dep = data[package]["depend"]

        if os.path.exists("packages/" + package):
            with open("packages/" + package) as f:
                content = f.read()
                object_hash = hashlib.sha1(content.encode())
                file_hash = object_hash.hexdigest()
            if file_hash != hs:
                add_hash_db(package, content)
                need[package] = data[package]
                for d in dep:
                    run(d, need)
        else:
            need[package] = data[package]
            for d in dep:
                run(d, need)
            with open("packages/" + package, 'w') as f:
                content = package
                f.write(content)

            add_hash_db(package, content)
        
        return need

if __name__ == "__main__":
    if sys.argv[1] == "make":
        package = sys.argv[2]
        with open("py_make_file") as f:
            data = json.load(f)
        init_db(data)
        need = run(package, {})
        order = tp_sort(data)
        if len(need) != 0:
            for pack in order:
                if pack in need:
                    for com in data[pack]['command']:
                        os.system(com)
        else:
            print(package + " is up to date.")
    elif sys.argv[1] == "clear":
        for f in os.listdir("packages/"):
            os.remove(os.path.join("packages/", f))


