#File: processing.py
#Author: Taylor King



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
