import numpy as np

def get_foods(foods_df):
  foods_repository = {}

  for _, row in foods_df.iterrows():
    foods_repository[row["id"]] = {
      "name": row["name"],
      "edible": row["edible"],
      "eco-score": row["eco-score"],
      "seasonality-score": row["seasonality-score"],
      "price": row["price"],
      "macros": {
        "c": row["carbohydrates"],
        "p": row["proteins"],
        "f": row["fats"],
      },
    }

  return foods_repository
