import csv
import re

# Define a regular expression to match US and Canada state names/abbreviations
us_canada_states = r'^(?:(?:A[LKZR]|C[AOT]|D[EC]|FL|GA|HI|I[DLNA]|K[SY]|LA|M[ADEHINOPST]|N[BCDEHJLMNPVY]|O[HKNR]|P[AR]|RI|S[CD]|T[NX]|UT|V[AIT]|W[AIVY]))(?:,?\s+[A-Z]{2})?$'

# Open the input CSV file
with open('result.csv', 'r') as input_file:

    # Create a CSV reader object
    reader = csv.reader(input_file)

    # Skip the header row
    header = next(reader)

    # Create an empty list to store the rows with HQ in the US or Canada
    us_canada_rows = []

    # Loop through each row in the CSV file
    for row in reader:

        # Check if the row has at least 3 columns
        if len(row) < 3:
            print(f"Skipping row with insufficient data: {row}")
            continue

        # Extract the city and state names from the hq column
        city_state = row[2].split(',')

        # Check if the state name or abbreviation matches the US or Canada regex
        if len(city_state) < 2 or not re.match(us_canada_states, city_state[-1].strip()):
            continue

        # Add the row to the list
        us_canada_rows.append(row)

    # Sort the rows by the company name
    sorted_rows = sorted(us_canada_rows, key=lambda x: x[0])

# Open the output CSV file
with open('US&CANADA.csv', 'w', newline='') as output_file:

    # Create a CSV writer object
    writer = csv.writer(output_file)

    # Write the header row
    writer.writerow(header)

    # Write the sorted and filtered rows
    for row in sorted_rows:
        writer.writerow(row)
