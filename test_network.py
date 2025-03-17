#File: test_network.py
#Author: Taylor King

import unittest
from unittest.mock import patch, mock_open

from network import (
    file_to_edge_list,
    edge_to_neighbour_list_1,
    edge_to_neighbour_list_2,
    inspect_node,
    get_degree_statistics,
    get_clustering_coefficient
)

class TestFileToEdgeList(unittest.TestCase):
    """
    Tests for the file_to_edge_list function.
    """
    @patch("builtins.open", new_callable=mock_open, read_data="")
    def test_empty_input(self, mock_file):
        """
        Test that an empty file returns an empty edge list.
        """
        edges = file_to_edge_list("fake_path.tsv")
        self.assertEqual(edges, [], "An empty input should give an empty list")

    @patch("builtins.open", new_callable=mock_open, read_data="99\t26\n27\t67\n")
    def test_basic_small_input(self, mock_file):
        """
        Test a small TSV file input.
        """
        edges = file_to_edge_list("fake_path.tsv")
        expected = [(99, 26), (27, 67)]
        self.assertEqual(edges, expected, "Small input edges do not match the expected output")

    @patch("builtins.open", new_callable=mock_open,
           read_data="1\t2\n1\t3\n2\t4\n3\t4\n999\t1000\n")
    def test_basic_larger_input(self, mock_file):
        """
        Test a larger TSV file input.
        """
        edges = file_to_edge_list("fake_path.tsv")
        #Check to ensure correct number of edges and one of the known pairs exists.
        self.assertEqual(len(edges), 5, "Should have 5 edges total")
        self.assertIn((999, 1000), edges, "Edge (999, 1000) should be in the list")

class TestEdgeToNeighbourList(unittest.TestCase):
    """
    Tests for edge_to_neighbour_list_1 and edge_to_neighbour_list_2.
    """

    def test_neighbour_list_equivalence(self):
        """
        Test both functions produce the same neighbor list on a known sample input.
        """
        edge_list = [(0, 1), (1, 2), (2, 3), (0, 3)]
        #Manually define the expected neighbor list (undirected).
        #Node 0 => {1,3}, Node 1 => {0,2}, Node 2 => {1,3}, Node 3 => {0,2}.
        expected = {
            0: {1, 3},
            1: {0, 2},
            2: {1, 3},
            3: {0, 2}
        }

        result_1 = edge_to_neighbour_list_1(edge_list)
        result_2 = edge_to_neighbour_list_2(edge_list)

        self.assertEqual(result_1, expected, "edge_to_neighbour_list_1 result is incorrect")
        self.assertEqual(result_2, expected, "edge_to_neighbour_list_2 result is incorrect")

    def test_neighbour_list_empty_input(self):
        """
        Test that an empty edge list returns an empty neighbor list.
        """
        edge_list = []
        expected = {}
        result_1 = edge_to_neighbour_list_1(edge_list)
        result_2 = edge_to_neighbour_list_2(edge_list)
        self.assertEqual(result_1, expected, "Empty edge list should give empty dict (method 1)")
        self.assertEqual(result_2, expected, "Empty edge list should give empty dict (method 2)")

    def test_neighbour_list_disconnected_nodes(self):
        """
        Ensure that if we have, say, edges among (0,1) and (2,3), no spurious connections appear.
        """
        edge_list = [(0, 1), (2, 3)]
        #Expected neighbor list has 2 disconnected components.
        expected = {
            0: {1},
            1: {0},
            2: {3},
            3: {2}
        }
        result_1 = edge_to_neighbour_list_1(edge_list)
        result_2 = edge_to_neighbour_list_2(edge_list)
        self.assertEqual(result_1, expected, "Disconnected nodes not handled correctly (method 1)")
        self.assertEqual(result_2, expected, "Disconnected nodes not handled correctly (method 2)")

class TestInspectNode(unittest.TestCase):
    """
    Tests for the inspect_node function.
    """
    def test_inspect_node_edge_list(self):
        """
        Ensure we get the correct list of edges for a node when 'network' is an edge list.
        """
        # Example edge list: (10,20), (20,30), (10,40)
        edge_list = [(10, 20), (20, 30), (10, 40)]
        # The edges for node 10 should be [(10, 20), (10, 40)] in any order
        expected = [(10, 20), (10, 40)]

        result = inspect_node(network=edge_list, node=10)
        self.assertEqual(sorted(result), sorted(expected),
                         "Inspect node failed to return correct edges from edge list")

    def test_inspect_node_neighbor_list(self):
        """
        Ensure we get the correct set of neighbors for a node when 'network' is a neighbor dictionary.
        """
        neighbor_dict = {
            10: {20, 40},
            20: {10, 30},
            30: {20},
            40: {10}
        }
        expected = {20, 40}

        result = inspect_node(network=neighbor_dict, node=10)
        self.assertEqual(result, expected,
                         "Inspect node failed to return correct neighbors from neighbor list")

    def test_inspect_node_missing_node_edge_list(self):
        """
        Inspect a node not present in an edge list; expect an empty list.
        """
        edge_list = [(1, 2), (2, 3)]
        result = inspect_node(network=edge_list, node=99)
        self.assertEqual(result, [],
                         "Missing node in an edge list should return an empty list")

    def test_inspect_node_missing_node_neighbor_list(self):
        """
        Inspect a node not present in a neighbor list; expect an empty set.
        """
        neighbor_dict = {
            1: {2},
            2: {1, 3},
            3: {2}
        }
        result = inspect_node(network=neighbor_dict, node=99)
        self.assertEqual(result, set(),
                         "Missing node in a neighbor list should return an empty set")

class TestGetDegreeStatistics(unittest.TestCase):
    """
    Tests for the get_degree_statistics function, which accepts a neighbourlist dictionary and returns (max_degree, min_degree, average_degree, most_common_degree).
    """
    def test_uniform_distribution(self):
        """
        All nodes have the same degree => max, min, average, and most common degree
        should all be the same.
        """
        #Fully connected triad:
        #Node 0 neighbors -> {1, 2}, Node 1 -> {0, 2}, Node 2 -> {0, 1}
        #Each node has degree 2.
        neighbour_dict = {
            0: {1, 2},
            1: {0, 2},
            2: {0, 1},
        }
        #Should expect (2, 2, 2.0, 2)
        result = get_degree_statistics(neighbour_dict)
        expected = (2, 2, 2.0, 2)
        self.assertEqual(result, expected,
            "Uniform distribution test failed: all degrees should be 2.")

    def test_varied_distribution(self):
        """
        Nodes have different degrees, so test that max, min, average, and most common are computed correctly.
        """
        #Node degrees:
        # 10: {20, 30} => degree 2
        # 20: {10} => degree 1
        # 30: {10, 40, 50} => degree 3
        # 40: {30} => degree 1
        # 50: {30} => degree 1
        # So degrees = [2, 1, 3, 1, 1]
        # max=3, min=1, average= (2+1+3+1+1)/5 = 8/5=1.6, most_common_degree=1
        neighbour_dict = {
            10: {20, 30},
            20: {10},
            30: {10, 40, 50},
            40: {30},
            50: {30},
        }
        result = get_degree_statistics(neighbour_dict)
        expected = (3, 1, 1.6, 1)
        self.assertEqual(result, expected, "Varied distribution test failed.")

    def test_single_node_no_edges(self):
        """
        A single node with no neighbors => degree=0.
        So the result should be (0, 0, 0.0, 0).
        """
        neighbour_dict = {
            99: set()
        }
        result = get_degree_statistics(neighbour_dict)
        expected = (0, 0, 0.0, 0)
        self.assertEqual(result, expected,
            "Single node with no edges test failed: should yield (0,0,0.0,0).")

    def test_no_nodes(self):
        """
        Edge case: an empty neighbor dictionary.
        The specification doesn't say explicitly what to do here.
        Either raise an exception or return (0,0,0.0,0).
        Let's assume (0,0,0.0,0).
        """
        neighbour_dict = {}
        result = get_degree_statistics(neighbour_dict)
        expected = (0, 0, 0.0, 0)
        self.assertEqual(result, expected,
            "Empty dictionary test failed: should yield (0,0,0.0,0) if no nodes exist.")

import unittest
# We'll import get_clustering_coefficient later once implemented
from network import get_clustering_coefficient

class TestGetClusteringCoefficient(unittest.TestCase):
    """
    Tests for the get_clustering_coefficient function.
    """

    def test_no_neighbors(self):
        """
        If a node has no neighbors, the clustering coefficient should be 0.0 
        (or potentially undefined, but here we'll expect 0.0).
        """
        # Node '50' has no neighbors
        neighbour_dict = {
            50: set()
        }
        result = get_clustering_coefficient(network=neighbour_dict, node=50)
        self.assertEqual(result, 0.0, 
            "A node with no neighbors should have a 0.0 clustering coefficient")

    def test_fully_connected_neighbors(self):
        """
        If a node's neighbors form a complete subgraph, the clustering coefficient should be 1.0.
        """
        # Node 10 has neighbors 20, 30
        # And 20, 30 are also neighbors with each other => fully connected subgraph
        neighbour_dict = {
            10: {20, 30},
            20: {10, 30},
            30: {10, 20},
        }
        result = get_clustering_coefficient(network=neighbour_dict, node=10)
        self.assertEqual(result, 1.0, 
            "Fully connected neighbors should result in a clustering coefficient of 1.0")

    def test_partial_connectivity(self):
        """
        A node with multiple neighbors where some but not all are connected.
        We'll use a small example where the coefficient is 0.5 or something similar.
        """
        # Node 1 has neighbors 2, 3, 4
        # Among those neighbors:
        #  2 is connected to 3
        #  3 is connected to 2
        #  4 is disconnected from 2 and 3
        #
        # k = 3 (neighbors 2, 3, 4)
        # Among those 3 neighbors, we have 1 edge (2,3).
        # E_N = 1
        # So coefficient = 2*E_N / [k*(k-1)] = 2*1 / (3*2) = 2/6 = 0.3333...
        #
        neighbour_dict = {
            1: {2, 3, 4},
            2: {1, 3},
            3: {1, 2},
            4: {1}
        }
        result = get_clustering_coefficient(network=neighbour_dict, node=1)
        # We'll allow some floating tolerance
        self.assertAlmostEqual(result, 1/3, places=4,
            msg="Partial connectivity among neighbors should yield ~0.3333")

    def test_node_not_in_network(self):
        """
        If the node does not exist in the network, we might return 0.0 or raise an error.
        We'll assume 0.0 here for convenience.
        """
        neighbour_dict = {
            10: {20},
            20: {10, 30},
            30: {20}
        }
        result = get_clustering_coefficient(network=neighbour_dict, node=99)
        self.assertEqual(result, 0.0, 
            "Missing node in the network should yield 0.0 (or some default value).")

if __name__ == "__main__":
    unittest.main()


if __name__ == "__main__":
    unittest.main()
