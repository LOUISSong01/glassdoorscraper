import csv

longest_link = ''
with open('glassdoor1.csv', 'r') as file:
    reader = csv.reader(file)
    # skip header row if it exists
    next(reader, None)
    
    for row in reader:
        if len(row) < 14:
            print(f'Error: row has only {len(row)} columns')
        else:
            link = row[13]  # assuming link is in the 14th column (Python is 0-indexed)
            if len(link) > len(longest_link):
                longest_link = link

print(f'The longest link is {longest_link}, which has {len(longest_link)} characters.')
