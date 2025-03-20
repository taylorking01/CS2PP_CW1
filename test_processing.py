#File: test_processing.py
#Author: Taylor King

import unittest
from processing import (
    read_csv, remove_columns, remove_makes, remove_duplicates, rename_columns, replace_missing_hp_with_median, remove_rows_with_missing_values, add_hp_type_column, add_price_class_column, round_price, filter_year
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
        data = [{'ColA': 'Val1', 'ColB': 'Val2', 'ColC': 'Val3'}]
        result = remove_columns(data, ['ColB'])
        self.assertEqual(result, [{'ColA': 'Val1', 'ColC': 'Val3'}])

    def test_remove_makes(self):
        #Test the removal of entries based upon specified car makes using the remove_makes method.
        data = [
            {'Make': 'Toyota', 'Model': 'Aygo'},
            {'Make': 'BMW', 'Model': 'i8'},
            {'Make': 'Toyota', 'Model': 'Prius'},
            {'Make': 'KTM', 'Model': 'X-bow'}
        ]
        result = remove_makes(data, ['Toyota', 'BMW'])
        self.assertEqual(result, [{'Make': 'KTM', 'Model': 'X-bow'}])

    def test_remove_duplicates(self):
        #Test the removal of duplicate entries from dataset using remove_duplicates method.
        data = [
            {'Make': 'Toyota', 'Model': 'Aygo'},
            {'Make': 'Toyota', 'Model': 'Aygo'},
            {'Make': 'Toyota', 'Model': 'Prius'},
            {'Make': 'Toyota', 'Model': 'Aygo'}
        ]
        result = remove_duplicates(data)
        expected = [
            {'Make': 'Toyota', 'Model': 'Aygo'},
            {'Make': 'Toyota', 'Model': 'Prius'}
        ]
        self.assertEqual(result, expected)

    def test_rename_columns(self):
        #Test the renaming of column headers using the rename_columns method.
        data = [
            {'Make': 'Toyota', 'Model': 'Aygo'},
            {'Make': 'KTM', 'Model': 'X-bow'}
        ]
    
        renaming_map = {
            'Make': 'Manufacturer',
            'Model': 'CarModel'
        }
    
        result = rename_columns(data, renaming_map)
        expected = [
            {'Manufacturer': 'Toyota', 'CarModel': 'Aygo'},
            {'Manufacturer': 'KTM', 'CarModel': 'X-bow'}
        ]
        self.assertEqual(result, expected)

    def test_replace_missing_hp_with_median(self):
        #Test replacing missing HP values with median HP using replace_missing_hp_with_median method.
        data = [
            {'HP': '500'}, 
            {'HP': ''}, 
            {'HP': '100'}
        ]
        result = replace_missing_hp_with_median(data, 'HP')
        expected = [
            {'HP': '500'},
            {'HP': '300'},  # median of [500,100] is 300
            {'HP': '100'}
        ]
        self.assertEqual(result, expected)

    def test_remove_rows_with_missing_values(self):
        #Test removing rows with missing values using remove_rows_with_missing_values method.
        data = [
            {'Make': 'Toyota', 'Model': 'Aygo'},
            {'Make': '', 'Model': 'A6'},  #Missing a make
            {'Make': 'KTM', 'Model': ''}  #Missing a model
        ]
        result = remove_rows_with_missing_values(data)
        expected = [{'Make': 'Toyota', 'Model': 'Aygo'}]
        self.assertEqual(result, expected)

    def test_add_hp_type_column(self):
        #Test the addition of HP_Type column based on HP value using add_hp_type_column method.
        data = [{'HP': '300'}, {'HP': '299'}, {'HP': '301'}]
        result = add_hp_type_column(data, 'HP')
        expected = [
            {'HP': '300', 'HP_Type': 'high'},
            {'HP': '299', 'HP_Type': 'low'},
            {'HP': '301', 'HP_Type': 'high'}
        ]
        self.assertEqual(result, expected)
    
    def test_add_price_class_column(self):
        #Test the success of categorization of price into Price_class using add_price_class_column method.
        data = [{'Price': '50000'}, {'Price': '40000'}, {'Price': '29999'}]
        result = add_price_class_column(data, 'Price')
        expected = [
            {'Price': '50000', 'Price_class': 'high'},
            {'Price': '40000', 'Price_class': 'mid'},
            {'Price': '29999', 'Price_class': 'low'}
        ]
        self.assertEqual(result, expected)

    def test_round_price(self):
        #Test rounding of Price to the nearest $100 using round_price method.
        data = [{'Price': '91449'}, {'Price': '91950'}, {'Price': '10999'}]
        result = round_price(data, 'Price')
        expected = [
            {'Price': '91400'},
            {'Price': '92000'},
            {'Price': '11000'}
        ]
        self.assertEqual(result, expected)
    
    def test_filter_year(self):
        #Test the filtering of rows based on year greater than threshold using filter_year method.
        data = [{'Year': '1999'}, {'Year': '2001'}, {'Year': '2000'}]
        result = filter_year(data, 'Year', year_threshold=2000)
        expected = [{'Year': '2001'}]
        self.assertEqual(result, expected)




































































if __name__ == '__main__':
    unittest.main()
    test.main()
    