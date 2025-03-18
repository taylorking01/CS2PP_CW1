#File: processing.py
#Author: Taylor King

import csv

def read_csv(fName):
    """Reads the CSV file and returns header and data rows separately."""
    with open(fName, 'r') as file:
        reader = csv.reader(file)
        data = list(reader)
    return data[0], data[1:]

def count_unique_makes(rows, header):
    """Returns the number of unique car makes."""
    make_index = header.index("Make")
    return len(set(row[make_index] for row in rows))

def count_entries_from_year(rows, header, year="2009"):
    """Returns the number of entries from a specific year."""
    year_index = header.index("Year")
    return sum(1 for row in rows if row[year_index] == year)

def avg_msrp_by_model(rows, header, model_name):
    """Returns the average MSRP for a given model name, rounded to 2 decimal places."""
    model_index = header.index("Model")
    msrp_index = header.index("MSRP")
    values = [float(row[msrp_index]) for row in rows if row[model_index] == model_name]
    return round2dp(sum(values)/len(values)) if values else "0.00"

def model_with_fewest_midsize(rows, header):
    """Returns the model with the fewest Midsize car entries (alphabetically first if tied)."""
    vehicle_size_index = header.index("Vehicle Size")
    model_index = header.index("Model")

    model_counts = {}
    for row in rows:
        if row[vehicle_size_index] == "Midsize":
            model = row[model_index]
            model_counts[model] = model_counts.get(model, 0) + 1

    all_models = set(row[model_index] for row in rows)

    #Helper function for getting midsize counts (0 if no midsize cars).
    def midsize_count(model):
        return model_counts.get(model, 0)

    return min(sorted(all_models), key=midsize_count)

def round2dp(value):
    """Rounds a float to two decimal places as a formatted string."""
    return f"{round(value, 2):.2f}"

def get_original_data_stats(header, rows):
    """Returns the required original dataset statistics as a list."""
    num_rows = len(rows)
    num_columns = len(header)
    num_unique_makes = count_unique_makes(rows, header)
    num_2009 = count_entries_from_year(rows, header, year="2009")
    avg_impala = avg_msrp_by_model(rows, header, "Impala")
    avg_integra = avg_msrp_by_model(rows, header, "Integra")
    fewest_midsize_model = model_with_fewest_midsize(rows, header)

    return [
        num_rows,
        num_columns,
        num_unique_makes,
        num_2009,
        avg_impala,
        avg_integra,
        fewest_midsize_model
    ]

###Remove columns###
def remove_columns(header, rows, columns_to_remove):
    """Removes specified columns from header and rows."""
    #Determine column indices to keep.
    indices_to_keep = [i for i, col in enumerate(header) if col not in columns_to_remove]

    #Filter the header and rows.
    new_header = [header[i] for i in indices_to_keep]
    new_rows = [[row[i] for i in indices_to_keep] for row in rows]

    return new_header, new_rows

###Remove rows###
def remove_rows_by_make(rows, header, makes_to_remove):
    """Removes rows containing any of the specified Makes."""
    make_index = header.index("Make")
    return [row for row in rows if row[make_index] not in makes_to_remove]

###Remove dupes###
def remove_duplicates(rows):
    """Removes duplicate rows."""
    unique_rows = []
    seen_rows = set()

    for row in rows:
        row_tuple = tuple(row)
        if row_tuple not in seen_rows:
            seen_rows.add(row_tuple)
            unique_rows.append(row)

    return unique_rows
    
def process_csv(fName):
    """
    Main function for processing the CSV file.
    Currently calculates only original statistics and returns placeholders for modified data.
    """
    header, rows = read_csv(fName)
    original_info = get_original_data_stats(header, rows)

    # Step 1: Remove columns
    columns_to_remove = ["Engine Fuel Type", "Market Category", "Number of Doors", "Vehicle Size"]
    header_mod, rows_mod = remove_columns(header, rows, columns_to_remove)

    # Step 2: Remove specified Makes (Ford, Kia, Lotus)
    makes_to_remove = ["Ford", "Kia", "Lotus"]
    rows_mod = remove_rows_by_make(rows_mod, header_mod, makes_to_remove)

    # Step 3: Remove duplicates
    rows_mod = remove_duplicates(rows_mod)

    # Temporarily returning modified stats as placeholder values
    modified_info = [
        len(rows_mod),         # now should be correct (2 rows)
        len(header_mod),
        count_unique_makes(rows_mod, header_mod),
        0,
        "0.00",
        "0.00",
        "?"
    ]

    return original_info, modified_info
