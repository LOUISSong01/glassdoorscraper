import pandas as pd

# Use this when the scraper crashses

my_list = []
df = pd.DataFrame(my_list)
df.to_csv('glassdoor2.csv', index=False)