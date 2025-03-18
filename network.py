#File: network.py
#Author: Taylor King

from collections import Counter

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

    #Collection of unique nodes.
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

def inspect_node(*, network, node):
    """
    Retrieve information about a specific node in a network.
    This function works for both edge lists and neighbor lists. If the 
    network is an edge list (list of tuples), it returns a list of all 
    edges that contain the specified node. If the network is a neighbor 
    list (dictionary), it returns the set of neighbors for the node. 
    If the node is not present in the network, it returns an empty list or set.

    Args:
        network (dict or list of tuples): The network representation, 
            either as an adjacency dictionary (neighbor list) or an edge list.
        node (int): The node to inspect.

    Returns:
        set or list of tuples: 
            - If `network` is a dictionary (neighbor list), returns a set of neighbors.
            - If `network` is a list of edges, returns a list of edge tuples where the node appears.
            - If `node` is not found in `network`, returns an empty set or list.
    """

    #Check if it is a neighbour list (a dictionary), otherwise it is an edge list.
    if isinstance(network, dict):
        #Return set of neighbors if node exists, otherwise an empty set is returned.
        return network[node] if node in network else set()
    else:
        #Meaning an edge list: gather edges that contain 'node'.
        result = []
        for (a, b) in network:
            if a == node or b == node:
                result.append((a, b))

        return result

def get_degree_statistics(neighbour_dict):
    """
    Compute degree-related statistics from a neighbor list.
    Given a network represented as a dictionary where each node maps to 
    a set of its neighbors, this function calculates key statistics about 
    the node degrees.

    Args:
        neighbour_dict (dict): A dictionary where keys are nodes and 
            values are sets of neighboring nodes.

    Returns:
        tuple: A 4-element tuple containing:
            - max_degree (int): The highest degree among nodes.
            - min_degree (int): The lowest degree among nodes.
            - average_degree (float): The average degree across all nodes.
            - most_common_degree (int): The most frequently occurring degree.
        
        If `neighbour_dict` is empty, returns (0, 0, 0.0, 0).
    """
    #If empty
    if not neighbour_dict:
        return (0, 0, 0.0, 0)

    #Calculate each node's degree.
    degrees = [len(neighbour_dict[node]) for node in neighbour_dict]

    max_degree = max(degrees)
    min_degree = min(degrees)
    #Use a lambda for average
    avg_func = lambda x: sum(x) / len(x)
    avg_degree = avg_func(degrees)

    #For most common degree we can use collections.Counter.
    count = Counter(degrees)
    most_common_deg = count.most_common(1)[0][0]

    return (max_degree, min_degree, avg_degree, most_common_deg)

def get_clustering_coefficient(*, network, node):
    """
    Compute the clustering coefficient for a given node.
    The clustering coefficient quantifies how connected a node's neighbors 
    are to each other. It is calculated as:

        C = (2 * E_N) / [k * (k - 1)]

    where:
        - E_N is the number of edges among the node's k neighbors.
        - k is the number of neighbors (degree of the node).
    
    If the node has fewer than 2 neighbors, the clustering coefficient is 0.0.

    Args:
        network (dict): A dictionary where each node maps to a set of its neighbors.
        node (int): The node for which to calculate the clustering coefficient.

    Returns:
        float: The clustering coefficient for the node (between 0.0 and 1.0).
            Returns 0.0 if the node is missing or has fewer than 2 neighbors.
    """
    # If node is missing, 0.0.
    if node not in network:
        return 0.0

    neighbors = network[node]
    k = len(neighbors)
    #If fewer than 2 neighbors, coefficient is 0.0.
    if k < 2:
        return 0.0

    #Count edges among neighbors (E_N).
    #This can be done by iterating over each pair of neighbors (i, j) and checking if j is in network[i].
    #Since it's undirected, we can treat (i, j) the same as (j, i), so we should only count each pair once.
    E_N = 0
    neighbors_list = list(neighbors)  # easier to index pairs
    for i in range(k):
        for j in range(i+1, k):
            n1 = neighbors_list[i]
            n2 = neighbors_list[j]
            # We check if n2 is in the neighbor set of n1
            if n2 in network.get(n1, set()):
                E_N += 1

    # Now compute the coefficient
    # (2 * E_N) / [k * (k - 1)]
    numerator = 2 * E_N
    denominator = k * (k - 1)
    C = numerator / denominator

    return C
