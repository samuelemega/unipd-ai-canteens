import numpy as np
import pandas as pd
import math
import random

from get_foods import get_foods
from get_recipes import get_recipes
from get_warehouse import get_warehouse

MUTATION_RATE = .1
TOURNAMENT_SIZE = 10
CANDIDATES_COUNT = 50
GENERATIONS_COUNT = 100

CONSTRAINT_WEIGHT_MACROS = 1
CONSTRAINT_WEIGHT_ECO = 1
CONSTRAINT_WEIGHT_SEASONALITY = 1
CONSTRAINT_WEIGHT_PRICE = 1

###################
##### CONTEXT #####
###################

foods_df = pd.read_csv("data/foods.csv", sep=";")

foods_repository = get_foods(foods_df)
recipes_repository = get_recipes(foods_df)
warehouse = get_warehouse(foods_df)

#####################
##### FUNCTIONS #####
#####################

#
# recipe_randomize
#
def recipe_randomize(recipe_name):
  result = []

  for _, ingredient in recipes_repository[recipe_name]["ingredients"].items():
    result.append(str(np.random.choice(ingredient["foods"])))

  return result

#
# recipe_fitness
#
def recipe_fitness(recipe_name, ingredients, weight):
  fitness = 0
  recipe = recipes_repository[recipe_name]

  total_eco_score = 0
  total_seasonality_score = 0
  total_price = 0

  total_w = 0
  total_c = 0
  total_p = 0
  total_f = 0

  for index, key in enumerate(recipe["ingredients"].keys()):

    # details of the food chosen for the current ingredient
    food_key = ingredients[index]
    food = foods_repository[food_key]

    # food weight considering its edible part
    food_weight_relative = recipe["ingredients"][key]["quantity"] / food["edible"]
    food_weight_total = food_weight_relative * weight

    total_eco_score += food["eco-score"] * food_weight_relative
    total_seasonality_score += food["seasonality-score"] * food_weight_relative

    total_w += food_weight_relative
    total_c += food_weight_relative * food["macros"]["c"]
    total_p += food_weight_relative * food["macros"]["p"]
    total_f += food_weight_relative * food["macros"]["f"]

    if food_weight_total > warehouse[food_key]:
      total_price += (food_weight_total - warehouse[food_key]) * food["price"]

  macros_target = recipes_repository[recipe_name]["macros"]
  macros_var = (
    (total_c / total_w - macros_target["c"]) ** 2 +
    (total_p / total_w - macros_target["p"]) ** 2 +
    (total_f / total_w - macros_target["f"]) ** 2
  )

  fitness -= CONSTRAINT_WEIGHT_MACROS * macros_var
  fitness += CONSTRAINT_WEIGHT_ECO * total_eco_score
  fitness += CONSTRAINT_WEIGHT_SEASONALITY * total_seasonality_score
  fitness -= CONSTRAINT_WEIGHT_PRICE * total_price

  return fitness

#
# recipe_print
#
def recipe_print(recipe_name, ingredients):
  result = ""
  recipe = recipes_repository[recipe_name]

  result += f"RECIPE {recipe_name}\n"

  price = 0

  c = 0
  p = 0
  f = 0

  ingredients_result = ""

  for index, key in enumerate(recipe["ingredients"].keys()):
    food_key = ingredients[index]
    food = foods_repository[food_key]

    food_weight = recipe["ingredients"][key]["quantity"] / food["edible"] * 100

    food_price = food_weight * food["price"] / 1000

    food_c = food_weight * food["macros"]["c"]
    food_p = food_weight * food["macros"]["p"]
    food_f = food_weight * food["macros"]["f"]

    price += food_price

    c += food_c
    p += food_p
    f += food_f

    ingredients_result += f"    INGREDIENT {index}\n"
    ingredients_result += f"      FOOD          {food["name"]}\n"
    ingredients_result += f"      WEIGHT        {food_weight:.2f}g\n"
    ingredients_result += f"      PROTEINS      {food_p:.2f}g\n"
    ingredients_result += f"      CARBOHYDRATES {food_c:.2f}g\n"
    ingredients_result += f"      FATS          {food_f:.2f}g\n"
    ingredients_result += f"      PRICE         {food_price:.2f}€\n"

  result += f"  PRICE {price:05.2f}€\n"

  result += "  MACROS\n"
  result += f"    PROTEINS      {p:05.2f}g\n"
  result += f"    CARBOHYDRATES {c:05.2f}g\n"
  result += f"    FATS          {f:05.2f}g\n"


  result += "  INGREDIENTS\n"
  result += ingredients_result

  print(result)

#############################
##### GENETIC FUNCTIONS #####
#############################

#
# recipe_genetic_mutation
#
def recipe_genetic_mutation(recipe_name, ingredients):
  mutated_ingredients = ingredients.copy()

  if np.random.rand() < MUTATION_RATE:
    mutation_index = np.random.randint(0, len(ingredients))

    ingredient_index = list(
      recipes_repository[recipe_name]["ingredients"].keys()
    )[mutation_index]

    mutated_ingredients[mutation_index] = str(np.random.choice(
      recipes_repository[recipe_name]["ingredients"][ingredient_index]["foods"]
    ))

  return mutated_ingredients

#
# recipe_genetic_crossover
#
def recipe_genetic_crossover(ingredients_a, ingredients_b):
  mutation_index = np.random.randint(0, len(ingredients_a) + 1)

  return ingredients_a[:mutation_index] + ingredients_b[mutation_index:]

#
# recipe_genetic_selection
#
def recipe_genetic_selection(recipe_name, ingredients_candidates, weight):
  selected = random.sample(ingredients_candidates, k=TOURNAMENT_SIZE)

  ingredients_a, ingredients_b = sorted(
    selected,
    key = lambda ingredients: recipe_fitness(recipe_name, ingredients, weight)
  )[:2]

  ingredients_a = recipe_genetic_mutation(recipe_name, ingredients_a)
  ingredients_b = recipe_genetic_mutation(recipe_name, ingredients_b)

  return recipe_genetic_crossover(ingredients_a, ingredients_b)

#
# recipe_genetic_solve
#
def recipe_genetic_solve(recipe_name, weight):
  generation = [
    recipe_randomize(recipe_name)
    for i in range(CANDIDATES_COUNT)
  ]

  for i in range(GENERATIONS_COUNT):
    generation_next = []

    for _ in range(CANDIDATES_COUNT):
      candidate = recipe_genetic_selection(recipe_name, generation, weight)
      generation_next.append(candidate)

    generation = generation_next

  return max(
    generation,
    key=lambda ingredients: recipe_fitness(recipe_name, ingredients, weight)
  )

################
##### MAIN #####
################

recipe_print("first-1", recipe_genetic_solve("first-1", 100))
recipe_print("first-2", recipe_genetic_solve("first-2", 100))
recipe_print("first-3", recipe_genetic_solve("first-3", 100))
recipe_print("first-4", recipe_genetic_solve("first-4", 100))
