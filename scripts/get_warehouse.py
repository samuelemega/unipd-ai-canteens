import numpy as np

def get_warehouse(foods_df):
  warehouse = {}

  for _, row in foods_df.iterrows():
    warehouse[row["id"]] = np.random.rand() * 100

  return warehouse
