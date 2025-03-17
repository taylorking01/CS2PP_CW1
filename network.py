def file_to_edge_list(fName):
    edge_list = []
    with open('./data/dolphins.tsv', 'r') as file:
        for line in file:
            line = line.strip()
            
            if not line: #If the line is blank then skip this iteration.
                continue

            a_str, b_str = line.split('\t')
            a, b = int(a_str), int(b_str)
            edge_list.append((a,b))

    return edge_list