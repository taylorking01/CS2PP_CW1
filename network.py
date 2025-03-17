def file_to_edge_list(fName):
    edge_list = []
    with open(fName, 'r') as file:
        for line in file:
            line = line.strip()
            
            if not line: #If the line is blank then skip this iteration.
                continue

            a_str, b_str = line.split('\t')
            a, b = int(a_str), int(b_str)
            edge_list.append((a,b))

    return edge_list

def edge_to_neighbour_list_1(edge_list):
    """
    Build a neighbour list (type is dictionary) from a list of edges (type is tuple). Implementation #1 is developed to be more efficient than #2.
    """
    neighbour_dict = {}

    for (a, b) in edge_list:
        if a not in neighbour_dict:
            neighbour_dict[a] = set()
        if b not in neighbour_dict:
            neighbour_dict[b] = set()

        neighbour_dict[a].add(b)
        neighbour_dict[b].add(a)

    return neighbour_dict

def edge_to_neighbour_list_2(edge_list):
    """
    A less efficient approach to constructing a neighbour list using a multi-pass approach.
    """
    neighbour_dict = {}

    #Collection of unique nodes
    unique_nodes = set()
    for (a, b) in edge_list:
        unique_nodes.add(a)
        unique_nodes.add(b)

    #For each node, then find which edges are connecting to it.
    for node in unique_nodes:
        neighbours = set()
        for (a, b) in edge_list:
            if a == node:
                neighbours.add(b)
            elif b == node:
                neighbours.add(a)
        neighbour_dict[node] = neighbours

    return neighbour_dict
    