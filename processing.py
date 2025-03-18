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
    
def process_csv(fName):
    """
    Main function for processing the CSV file.
    Currently calculates only original statistics and returns placeholders for modified data.
    """
    header, rows = read_csv(fName)
    original_info = get_original_data_stats(header, rows)

    #Placeholder for modified data until transformations are implemented
    modified_info = [
        0,       # rows
        0,       # columns
        0,       # unique makes
        0,       # 2009 entries
        "0.00",  # avg Impala price
        "0.00",  # avg Integra price
        "?"      # fewest midsize cars
    ]

    return original_info, modified_info
