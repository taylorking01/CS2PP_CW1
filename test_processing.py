#File: test_processing.py
#Author: Taylor King

import unittest
from unittest.mock import patch, mock_open

# We'll import process_csv once we have it implemented in processing.py
from processing import process_csv

class TestProcessCSV(unittest.TestCase):
    """
    Tests for Task 2's process_csv function which transforms cardata.csv and
    writes cardata_modified.csv.
    """

    @patch("builtins.open", new_callable=mock_open, read_data="""\
Make,Model,Year,Engine Fuel Type,Engine HP,Engine Cylinders,Transmission Type,Driven_Wheels,Number of Doors,Market Category,Vehicle Size,Vehicle Style,highway MPG,city mpg,Popularity,MSRP
Ford,Fiesta,2010,Petrol,120,4,Automatic,FWD,4,Some Market,Compact,Hatchback,36,28,150,16000
Kia,Rio,2009,Diesel,110,4,Manual,FWD,4,Economy,Subcompact,Hatchback,33,25,100,14000
Chevrolet,Impala,2009,Petrol,300,6,Automatic,FWD,4,Some Market,Midsize,Sedan,28,20,200,28000
Lotus,Elise,2012,Petrol,220,4,Manual,RWD,2,Performance,Compact,Convertible,33,25,300,65000
Chevrolet,Impala,2009,Petrol,300,6,Automatic,FWD,4,Some Market,Midsize,Sedan,28,20,200,28000
Acura,Integra,2009,Petrol,180,4,Manual,FWD,2,Performance,Compact,Coupe,31,23,150,22000
""")
    def test_process_csv_small_mock(self, mock_file):
        """
        Given a small mock CSV, ensure we get correct 7 pieces of info
        for original and modified forms.
        """
        # We'll call process_csv on our "fake" file
        # Note: we are patching open(...) so any file_path goes to our mock data
        original_info, modified_info = process_csv("fake_cardata.csv")

        # Now we can test that the function returned the correct stats
        # For example, if we expect 6 rows in original, 16 columns, etc.
        # The actual numbers below are placeholders for demonstration; 
        # you'll need to adjust them based on your final logic & transformation.

        # Check original_info
        # original_info = [num_rows, num_columns, num_unique_makes, num_2009_entries,
        #                  avg_msrp_impala, avg_msrp_integra, model_with_fewest_midsize_cars]
        self.assertEqual(original_info[0], 6, "Original CSV should have 6 rows")
        self.assertEqual(original_info[1], 16, "Original CSV should have 16 columns")
        self.assertEqual(original_info[2], 5, "Unique Make count is incorrect")
        self.assertEqual(original_info[3], 4, "Number of 2009 entries is incorrect")  
        self.assertEqual(original_info[4], "28000.00", "Avg MSRP for Impala is incorrect")
        self.assertEqual(original_info[5], "22000.00", "Avg MSRP for Integra is incorrect")
        self.assertEqual(original_info[6], "Elise", "Model with fewest Midsize cars is incorrect")

        # Check modified_info
        # Suppose after transformations, only 2 rows remain, 10 columns, etc.
        self.assertEqual(modified_info[0], 2, "Modified CSV row count is incorrect")
        self.assertEqual(modified_info[1], 12, "Modified CSV column count is incorrect")
        self.assertEqual(modified_info[2], 2, "Unique Make count in modified data is incorrect")
        self.assertEqual(modified_info[3], 2, "Number of 2009 entries in modified data is incorrect")
        self.assertEqual(modified_info[4], '28000.00', "Avg Price for Impala in modified data is incorrect")
        self.assertEqual(modified_info[5], "22000.00", "Avg Price for Integra in modified data is incorrect")
        self.assertEqual(modified_info[6], "Impala", "Model with fewest Midsize cars in modified data is incorrect")

        # The above is purely an example. You'll adjust each item to match your logic
        # & expected final transformation results.


if __name__ == "__main__":
    unittest.main()
