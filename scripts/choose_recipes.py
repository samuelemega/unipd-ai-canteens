import pandas as pd
import numpy as np
from rankedpairs import rp

from get_recipes import get_recipes_first, get_recipes_second, get_recipes_dessert

M1 = 2
M2 = 2
M3 = 2

#####################
##### FUNCTIONS #####
#####################

###############################################################################
# df_to_choices
#
def df_to_choices(df):
  choices = df.values.tolist()

  return([
    {
      candidate: (len(choice) - 2 - index) / (len(choice) - 2)
      for index, candidate in enumerate(choice[1:])
    }
    for choice in choices
  ])

###############################################################################
# result_to_list
#
def result_to_list(result):
  temp = [list(candidates) for candidates in result]
  return [item for sublist in temp for item in sublist]

###############################################################################
# recipe_totals
#
def recipe_totals(
  recipes_repository,
  recipes_result,
  recipes_choices,
  choices_df
):
  total = { recipe: 0 for recipe in recipes_result }

  for i, choice in enumerate(recipes_choices):
    qt = choices_df.loc[i]["qt"]
    best = max(recipes_result, key=lambda recipe: choice.get(recipe))
    total[best] += recipes_repository[best]["sizes"][qt - 1]

  return total

################
##### MAIN #####
################

foods_df = pd.read_csv("data/foods.csv", sep=";")
choices_first_df = pd.read_csv("data/choices-first.csv", sep=";")
choices_second_df = pd.read_csv("data/choices-second.csv", sep=";")
choices_dessert_df = pd.read_csv("data/choices-dessert.csv", sep=";")

recipes_first_repository = get_recipes_first(foods_df)
recipes_second_repository = get_recipes_second(foods_df)
recipes_dessert_repository = get_recipes_dessert(foods_df)

recipes_first_candidates = list(recipes_first_repository.keys())
recipes_second_candidates = list(recipes_second_repository.keys())
recipes_dessert_candidates = list(recipes_dessert_repository.keys())

recipes_first_choices = df_to_choices(choices_first_df)
recipes_second_choices = df_to_choices(choices_second_df)
recipes_dessert_choices = df_to_choices(choices_dessert_df)

recipes_first_result = rp.full_order(
  recipes_first_candidates,
  recipes_first_choices,
)

recipes_second_result = rp.full_order(
  recipes_second_candidates,
  recipes_second_choices,
)

recipes_dessert_result = rp.full_order(
  recipes_dessert_candidates,
  recipes_dessert_choices,
)

recipes_first_result = result_to_list(recipes_first_result)[:M1]
recipes_second_result = result_to_list(recipes_second_result)[:M2]
recipes_dessert_result = result_to_list(recipes_dessert_result)[:M3]

###################
##### RESULTS #####
###################

recipes_first_total = recipe_totals(
  recipes_first_repository,
  recipes_first_result,
  recipes_first_choices,
  choices_first_df,
)

recipes_second_total = recipe_totals(
  recipes_second_repository,
  recipes_second_result,
  recipes_second_choices,
  choices_second_df,
)

recipes_dessert_total = recipe_totals(
  recipes_dessert_repository,
  recipes_dessert_result,
  recipes_dessert_choices,
  choices_dessert_df,
)

totals = [
  [k, v]
  for k, v in {
    **recipes_first_total,
    **recipes_second_total,
    **recipes_dessert_total,
  }.items()
]

totals_df = pd.DataFrame(totals, columns=["recipe", "total"])
totals_df.to_csv("data/recipes-totals.csv", index=False, sep=";")

#####################
##### BENCHMARK #####
#####################

first_result_score = 0
second_result_score = 0
dessert_result_score = 0

for choice in recipes_first_choices:
  first_result_score += np.max([choice[k] for k in recipes_first_result])

for choice in recipes_second_choices:
  second_result_score += np.max([choice[k] for k in recipes_second_result])

for choice in recipes_dessert_choices:
  dessert_result_score += np.max([choice[k] for k in recipes_dessert_result])
