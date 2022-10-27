import pandas as pd

data = pd.read_csv("data/posts2.csv")

data_clean = data.drop_duplicates()
data_clean = data_clean.loc[~data_clean.company.isnull()]
data_clean = data_clean.loc[~data_clean.text.isnull()]

data_clean.to_csv("data/posts2_clean.csv")