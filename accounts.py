from sys import argv


def generate_graph(accounts):
    nodes = {}
    for account in accounts:
        node1_name = account["c1"]
        node2_name = account["c2"]
        if account["c1"] in nodes:
            node1 = nodes[account["c1"]]
        else:
            node1 = {"name": node1_name, "edges": []}
            nodes[node1_name] = node1

        if node2_name in nodes:
            node2 = nodes[node2_name]
        else:
            node2 = {"name": node2_name, "edges": []}
            nodes[node2_name] = node2
        node1["edges"] += [{"num": account["num"], "with": node2_name}]
        node2["edges"] += [{"num": account["num"], "with": node1_name}]
    return nodes


def find_path(graph, initial, end):
    initial_node = graph[initial]
    to_visit = [initial_node]
    visited = []
    previous = {}
    while len(to_visit) > 0:
        node = to_visit.pop(0)
        for edge in node["edges"]:
            node2_name = edge['with']
            if node2_name in visited:
                continue
            visited.append(node2_name)
            previous[node2_name] = node['name']
            to_visit.append(graph[node2_name])
    if end in previous:
        path = []
        previous_node = end
        while previous_node != initial:
            previous_previous_node = previous[previous_node]
            path.append((previous_previous_node, previous_node))
            previous_node = previous_previous_node
        return path



def clean_str(input):
    return input.replace('\r', '').replace(' \n', '').replace('\n', '')


file_name = argv[1]
file = open(file_name)

lines = file.readlines()
num_accounts = int(lines[0])

print "Accounts: %d" % num_accounts

accounts = []
for i in range(1, num_accounts + 1):
    line = lines[i]
    num, c1, c2 = clean_str(line).split(" ")
    accounts.append({"num": num, "c1": c1, "c2": c2})

last_line = lines[num_accounts + 1]
(initial, end) = clean_str(last_line).split(" ")

graph = generate_graph(accounts)
path = find_path(graph, initial, end)
for c1, c2 in path:
    print "%s, %s" % (c1, c2)

print "Steps: %d" % len(path)
