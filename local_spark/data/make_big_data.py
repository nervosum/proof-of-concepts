import pandas as pd


df = pd.read_csv("input.csv")
dfs = []
for i in range(200):
    dfs.append(df)

df_large = pd.concat(dfs)
df_large.to_csv("input_large.csv", index=False)
