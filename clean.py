import pandas as pd

# Read the CSV file into a pandas DataFrame
df = pd.read_csv("glassdoor1.csv")

# Drop the duplicate entries in the "company" column
df.drop_duplicates(subset=df.columns, inplace=True)

# Write the cleaned DataFrame to a new CSV file
df.to_csv("cleaned_file.csv", index=False)