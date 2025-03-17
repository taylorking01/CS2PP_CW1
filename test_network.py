#File: test_network.py
#Author: Taylor King

import unittest
from unittest.mock import patch, mock_open

from network import (
    file_to_edge_list,
    edge_to_neighbour_list_1,
    edge_to_neighbour_list_2,
    inspect_node
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

if __name__ == "__main__":
    unittest.main()
