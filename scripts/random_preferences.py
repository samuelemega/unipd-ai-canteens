import numpy as np
import pandas as pd

from get_recipes import get_recipes_first, get_recipes_second, get_recipes_dessert

USERS_COUNT = 1000
QTS = 3

foods_df = pd.read_csv("data/foods.csv", sep=";")

recipes_first_repository = get_recipes_first(foods_df)
recipes_second_repository = get_recipes_second(foods_df)
recipes_dessert_repository = get_recipes_dessert(foods_df)

recipes_first = list(recipes_first_repository.keys())
recipes_second = list(recipes_second_repository.keys())
recipes_dessert = list(recipes_dessert_repository.keys())

choices_first_df = pd.DataFrame(columns=["qt"] + [f"choice-{i + 1}" for i in range(len(recipes_first))])
choices_second_df = pd.DataFrame(columns=["qt"] + [f"choice-{i + 1}" for i in range(len(recipes_second))])
choices_dessert_df = pd.DataFrame(columns=["qt"] + [f"choice-{i + 1}" for i in range(len(recipes_dessert))])

for i in range(USERS_COUNT):
  choices_first_df.loc[i] = (
    [np.random.randint(1, QTS + 1)] +
    list(np.random.permutation(recipes_first))
  )

  choices_second_df.loc[i] = (
    [np.random.randint(1, QTS + 1)] +
    list(np.random.permutation(recipes_second))
  )

  choices_dessert_df.loc[i] = (
    [np.random.randint(1, QTS + 1)] +
    list(np.random.permutation(recipes_dessert))
  )

choices_first_df.to_csv("data/choices-first.csv", index=False, sep=";")
choices_second_df.to_csv("data/choices-second.csv", index=False, sep=";")
choices_dessert_df.to_csv("data/choices-dessert.csv", index=False, sep=";")
