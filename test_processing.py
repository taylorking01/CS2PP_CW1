#File: test_processing.py
#Author: Taylor King

import unittest
from processing import (
    read_csv, remove_columns
)

# from processing import (
#     read_csv, remove_columns, remove_makes, remove_duplicates,
#     rename_columns, replace_missing_hp_with_median, remove_rows_with_missing_values,
#     add_hp_type_column, add_price_class_column, round_price,
#     filter_year, filter_make_counts, compute_summary, write_csv, process_csv
# )

class TestProcessing(unittest.TestCase):

    def test_read_csv(self):
        #Test file reading functionality using the read_csv method.
        data = read_csv('./data/cardata.csv')
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)
        self.assertIsInstance(data[0], dict)

    def test_remove_columns(self):
        #Test the success of removing a column using the remove_column method.
        data = [{'A': '1', 'B': '2', 'C': '3'}]
        result = remove_columns(data, ['B'])
        self.assertEqual(result, [{'A': '1', 'C': '3'}])

if __name__ == '__main__':
    unittest.main()
    