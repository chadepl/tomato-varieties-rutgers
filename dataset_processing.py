""" Processes tomato_rutgers_raw.csv
What it does:
- Separates Plant Height column into unit and value.
- Separates Fruit Size column into unit and value.
"""

import pandas as pd

raw_df = pd.read_csv("tomato_rutgers_raw.csv")

print(raw_df.iloc[0, :])

# print(raw_df["Plant Height"].apply(lambda s: s.split(" ")[1].strip(".")))

print(raw_df["Plant Height"])

# Split the 'Name' column into two columns using a space as a separator
raw_df[['Plant Height', 'Plant Height Unit']] = raw_df['Plant Height'].str.split(' ', n=1, expand=True)
raw_df[['Fruit Size', 'Fruit Size Unit']] = raw_df['Fruit Size'].str.split(' ', n=1, expand=True)


print(raw_df.isna().sum(axis=0))

raw_df.to_csv("tomato_rutgers.csv")