def file_to_edge_list(fName):
    """
    Read a TSV file and build a list of edges.

    Each line in the TSV file is assumed to contain two integers (node a, node b).
    These integers will be converted into an (a, b) tuple and appended to the returned 
    list. Any blank lines are skipped.

    Args:
        fName (str): Path to the TSV file.

    Returns:
        list of tuples: Each tuple is (a, b), representing an undirected edge.
    """
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
    Build a neighbor dictionary from a list of edges using a single-pass approach.

    For each edge (a, b) in the list, add both 'a' and 'b' to the dictionary 
    as keys (if they are not already present), then insert each one into 
    the other's set of neighbors. This version aims to be more efficient 
    than edge_to_neighbour_list_2.

    Args:
        edge_list (list of tuples): Each tuple is (a, b), representing an undirected edge.

    Returns:
        dict: A dictionary mapping each node to a set of its neighbors.
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
    Build a neighbor dictionary from a list of edges using a multi-pass approach.

    This method is intentionally less efficient. For every unique node in the 
    edge list, the algorithm scans the entire edge list to discover all edges 
    linked to that node.

    Args:
        edge_list (list of tuples): Each tuple is (a, b), representing an undirected edge.

    Returns:
        dict: A dictionary mapping each node to a set of its neighbors.
    """
    neighbour_dict = {}

    #Collection of unique nodes
    unique_nodes = set()
    for (a, b) in edge_list:
        unique_nodes.add(a)
        unique_nodes.add(b)

    #For each node, find which edges are connecting to it.
    for node in unique_nodes:
        neighbours = set()
        for (a, b) in edge_list:
            if a == node:
                neighbours.add(b)
            elif b == node:
                neighbours.add(a)
        neighbour_dict[node] = neighbours

    return neighbour_dict
    