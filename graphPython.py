import json
import sys
import urllib.request


def create_graph(pkg):
    graph = {} 
    def get_req(pkg):
        graph[pkg] = set()
        url = "https://pypi.org/pypi/" + pkg + "/json"
        req = urllib.request.urlopen(url)
        data = json.load(req)
        if data["info"]["requires_dist"]:
            for i in data["info"]["requires_dist"]:
                if "extra" not in i and "sys_platform" not in i and "python_version" not in i:
                    req = i.split(" ")[0]
                    graph[pkg].add(req)
                    print(req)
                    if req not in graph:
                        get_req(req)
    get_req(pkg)
    return graph


graph = create_graph(sys.argv[1])
result = ["digraph G {"]
for i in graph:
    for j in graph[i]:
        result.append(f'"{i}" -> "{j}"')
result.append("}")
print("\n".join(result))