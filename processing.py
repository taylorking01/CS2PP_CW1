#File: processing.py
#Author: Taylor King
#Description:
#  Data Structures:
#    The CSV data is read into a list of dictionaries, 
#    where each dictionary represents a row with keys as column headers and corresponding data as values.
#    [
#      {"Make": "Lamborghini", "Model": "Adventador", "Year": "2015", "Price": "300000"},
#      {"Make": "Toyota", "Model": "Aygo", "Year": "2014", "Price": "3000"},
#      ...
#    ]

import csv
from typing import List, Dict, Tuple, Any

#Read CSV method
"""
Reads the csv into a list of dictionaries, each dictionary representing a row where the keys are the column headers.
"""
def read_csv(filepath: str) -> List[Dict[str, str]]:
    with open(filepath, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        data = [row for row in reader]
    return data

#Remove Columns method
"""
Removes specified columns from each dictionary (row) within the data list.
"""
def remove_columns(data: List[Dict[str, str]], columns_to_remove: List[str]) -> List[Dict[str, str]]:
    return [
        {key: value for key, value in row.items() if key not in columns_to_remove}
        for row in data
    ]

#Remove Makes method
"""
Removes entries from the dataset where 'Make' matches any of those listed in makes_to_remove.
"""
def remove_makes(data: List[Dict[str, str]], makes_to_remove: List[str]) -> List[Dict[str, str]]:
    return [
        row for row in data if row.get('Make') not in makes_to_remove
    ]

#Remove Duplicates method
"""
Removes duplicate rows from the dataset. A row is considered duplicate if all key-value pairs are identical.
"""
def remove_duplicates(data: List[Dict[str, str]]) -> List[Dict[str, str]]:
    seen = set()
    unique_data = []
    for row in data:
        #Convert dictionary into a tuple of sorted items to ensure consistent ordering for hashing
        row_tuple = tuple(sorted(row.items()))
        if row_tuple not in seen:
            seen.add(row_tuple)
            unique_data.append(row)
    return unique_data

#Rename Columns method
"""
Renames column headers based on the provided mapping dictionary (renaming_map), 
where keys are old column names and values are new column names.
"""
def rename_columns(data: List[Dict[str, str]], renaming_map: Dict[str, str]) -> List[Dict[str, str]]:
    renamed_data = []
    for row in data:
        renamed_row = {
            renaming_map.get(key, key): value for key, value in row.items()
        }
        renamed_data.append(renamed_row)
    return renamed_data

#Replace missing HP with median method
"""
Finds missing ('') values in the specified HP column and replaces them with the median of all existing HP values.
"""
def replace_missing_hp_with_median(data: List[Dict[str, str]], hp_key: str) -> List[Dict[str, str]]:
    hp_values = sorted([int(row[hp_key]) for row in data if row[hp_key].isdigit()])
    median_hp = hp_values[len(hp_values)//2] if len(hp_values) % 2 else (hp_values[len(hp_values)//2 - 1] + hp_values[len(hp_values)//2]) // 2

    for row in data:
        if not row[hp_key].isdigit():
            row[hp_key] = str(median_hp)
    return data

#Remove rows with missing values method
"""
Removes rows from the dataset if any column in the row contains missing ('') values.
"""
def remove_rows_with_missing_values(data: List[Dict[str, str]]) -> List[Dict[str, str]]:
    return [
        row for row in data if all(value.strip() != '' for value in row.values())
    ]

#Add HP_Type column method
"""
Adds a new column 'HP_Type' to each row.
'HP_Type' is 'high' if HP >= 300, otherwise 'low'.
"""
def add_hp_type_column(data: List[Dict[str, str]], hp_key: str) -> List[Dict[str, str]]:
    for row in data:
        row['HP_Type'] = 'high' if int(row[hp_key]) >= 300 else 'low'
    return data

#Add Price_class column method
"""
Adds a new column 'Price_class' categorizing price as:
    'high' if Price >= 50000
    'mid' if 30000 <= Price < 50000
    'low' if Price < 30000
"""
def add_price_class_column(data: List[Dict[str, str]], price_key: str) -> List[Dict[str, str]]:
    for row in data:
        price = int(row[price_key])
        if price >= 50000:
            row['Price_class'] = 'high'
        elif 30000 <= price < 50000:
            row['Price_class'] = 'mid'
        else:
            row['Price_class'] = 'low'
    return data

#Round price values method
"""
Rounds the values in the specified Price column to the nearest $100.
"""
def round_price(data: List[Dict[str, str]], price_key: str) -> List[Dict[str, str]]:
    for row in data:
        price = int(row[price_key])
        row[price_key] = str(int(round(price, -2)))
    return data






#Process CSV method.
def process_csv(filepath: str) -> Tuple[List[Any], List[Any]]:

    #Prep: Read in the data and compute the summary.
    original_data = read_csv(filepath)
    original_summary = compute_summary(original_data, 'MSRP')
    return None

    # #1. Remove columns.
    # modified_data = remove_columns(original_data, ["Engine Fuel Type", "Market Category", "Number of Doors", "Vehicle Size"])
    
    # #2. Remove makes.
    # modified_data = remove_makes(modified_data, ["Ford", "Kia", "Lotus"])

    # #3. Make all rows unique.
    # modified_data = remove_duplicates(modified_data)

    # #4. Modify column headers to match the specification table.
    # rename_map = {
    #     "Engine HP": "HP",
    #     "Engine Cylinders": "Cylinders",
    #     "Transmission Type": "Transmission",
    #     "Driven_Wheels": "Drive Mode",
    #     "highway MPG": "MPG-H",
    #     "city mpg": "MPG-C",
    #     "MSRP": "Price"
    # }
    # #modified_data = rename_columns(modified_data, rename_map)

    # #5. Replace missing values in HP column.
    # modified_data = replace_missing_hp_with_median(modified_data, "HP")

    # #6. Remove other rows with missing values.
    # modified_data = remove_rows_with_missing_values(modified_data)

    # #7. Create HP_Type column
    # modified_data = add_hp_type_column(modified_data, "HP")

    # #8. Create Price_class column
    # modified_data = add_price_class_column(modified_data, "Price")

    # #9. Round price values to nearest $100.
    # modified_data = round_price(modified_data, "Price")

    # #10. Filter year to after 2000.
    # modified_data = filter_year(modified_data, "Year", year_threshold=2000)

    # #11. Apply filter so only unique car makes with between 55 and 300 entries remain.
    # modified_data = filter_make_counts(modified_data, "Make", min_count=55, max_count=300)

    # #Finalising: Write the processed data to a new csv and then compute a summary before returning the original summary and modified summary.
    # write_csv('./data/cardata_modified.csv', modified_data, headers=list(modified_data[0].keys()))
    # modified_summary = compute_summary(modified_data, 'Price')

    # return original_summary, modified_summary
