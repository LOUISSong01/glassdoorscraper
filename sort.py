import csv
import operator

# Open the CSV file and read its contents into a list of dictionaries
with open('US&CANADA.csv', 'r') as file:
    reader = csv.DictReader(file)
    data = list(reader)

# Sort the data by the ovr_rating column in descending order
sorted_data = sorted(data, key=operator.itemgetter('ovr_rating'), reverse=True)

# Write the sorted data to a new CSV file
with open('NA_rating_sorted.csv', 'w', newline='') as file:
    fieldnames = ['company', 'company type', 'hq', 'industry', 'size', 'revenue', 'ovr_rating', 'rating_CV', 'rating_DI', 'rating_WLB', 'rating_SM', 'rating_CB', 'rating_CO', 'link']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    for row in sorted_data:
        writer.writerow(row)
