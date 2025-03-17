#File: test_network.py
#Author: Taylor King

import unittest
from unittest.mock import patch, mock_open

from network import file_to_edge_list

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

if __name__ == "__main__":
    unittest.main()
