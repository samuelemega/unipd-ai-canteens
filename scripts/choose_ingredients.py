import numpy as np
import pandas as pd
import math
import random
import matplotlib.pyplot as plt

from get_foods import get_foods
from get_recipes import get_recipes_first, get_recipes_second, get_recipes_dessert
from get_warehouse import get_warehouse

QT_FACTOR_VAR = 1
MUTATION_RATE = .1
TOURNAMENT_SIZE = 5
CANDIDATES_COUNT = 100
GENERATIONS_COUNT = 100

CONSTRAINT_WEIGHT_MACROS = 1
CONSTRAINT_WEIGHT_ECO = 1
CONSTRAINT_WEIGHT_SEASONALITY = 1
CONSTRAINT_WEIGHT_PRICE = 1

PRINT_N = 5

###################
##### CONTEXT #####
###################

foods_df = pd.read_csv("data/foods.csv", sep=";")
recipes_totals_df = pd.read_csv("data/recipe-totals.csv", sep=";")

foods_repository = get_foods(foods_df)
warehouse = get_warehouse(foods_df)

recipes_first_repository = get_recipes_first(foods_df)
recipes_second_repository = get_recipes_second(foods_df)
recipes_dessert_repository = get_recipes_dessert(foods_df)

recipes_repository = {
  **recipes_first_repository,
  **recipes_second_repository,
  **recipes_dessert_repository,
}

###################
##### CLASSES #####
###################

class Recipe:

  def __init__(self, recipe_name, weight):
    self.recipe_name = recipe_name
    self.recipe = recipes_repository[recipe_name]
    self.weight = weight

  #############################################################################
  # random_gene
  #
  def random_gene(self):
    return [
      (
        str(np.random.choice(ingredient["foods"])),
        (1 - QT_FACTOR_VAR / 2) + QT_FACTOR_VAR * np.random.rand(),
      )
      for _, ingredient in self.recipe["ingredients"].items()
    ]

  #############################################################################
  # fitness
  #
  def fitness(self, gene):
    fitness = 0

    total_eco_score = 0
    total_seasonality_score = 0
    total_price = 0

    total_w = 0
    total_c = 0
    total_p = 0
    total_f = 0

    for index, key in enumerate(self.recipe["ingredients"].keys()):

      # details of the food chosen for the current ingredient
      food_key, quantity_factor = gene[index]
      food = foods_repository[food_key]

      # food weight considering its edible part

      food_weight_relative = (
        quantity_factor *
        self.recipe["ingredients"][key]["quantity"] /
        food["edible"]
      )

      food_weight_total = food_weight_relative * self.weight

      total_eco_score += food["eco-score"] * food_weight_relative
      total_seasonality_score += food["seasonality-score"] * food_weight_relative

      total_w += food_weight_relative
      total_c += food_weight_relative * food["macros"]["c"]
      total_p += food_weight_relative * food["macros"]["p"]
      total_f += food_weight_relative * food["macros"]["f"]

      if food_weight_total > warehouse[food_key]:
        total_price += (food_weight_total - warehouse[food_key]) * food["price"]

    macros_target = self.recipe["macros"]
    macros_var = (
      ((total_c / total_w - macros_target["c"]) / macros_target["c"]) ** 2 +
      ((total_p / total_w - macros_target["p"]) / macros_target["p"]) ** 2 +
      ((total_f / total_w - macros_target["f"]) / macros_target["f"]) ** 2
    )

    fitness -= CONSTRAINT_WEIGHT_MACROS * macros_var
    fitness += CONSTRAINT_WEIGHT_ECO * total_eco_score
    fitness += CONSTRAINT_WEIGHT_SEASONALITY * total_seasonality_score
    fitness -= CONSTRAINT_WEIGHT_PRICE * total_price

    return fitness

  #############################################################################
  # to_df
  #
  def to_df(self, gene):
    price = 0

    w = 0
    c = 0
    p = 0
    f = 0

    foods_df = pd.DataFrame(columns=[
      "Food", "Weight (kg)", "Carbohydrates", "Proteins", "Fats", "Price (€)",
    ])

    for index, key in enumerate(self.recipe["ingredients"].keys()):
      food_key, quantity_factor = gene[index]
      food = foods_repository[food_key]

      food_weight_relative = (
        quantity_factor *
        self.recipe["ingredients"][key]["quantity"] /
        food["edible"]
      )

      food_weight_total = food_weight_relative * self.weight

      food_price = food_weight_total * food["price"] / 1000

      food_c = food_weight_total * food["macros"]["c"]
      food_p = food_weight_total * food["macros"]["p"]
      food_f = food_weight_total * food["macros"]["f"]

      price += food_price

      w += food_weight_total
      c += food_c
      p += food_p
      f += food_f

      foods_df.loc[index] = [
        food["name"],
        round(food_weight_total / 1000, 2),
        f"{food_c / food_weight_total * 100:05.2f}%",
        f"{food_p / food_weight_total * 100:05.2f}%",
        f"{food_f / food_weight_total * 100:05.2f}%",
        round(food_price, 2),
      ]

    foods_df.loc[index + 1] = [
      "",
      round(w / 1000, 2),
      f"{c / w * 100:05.2f}%",
      f"{p / w * 100:05.2f}%",
      f"{f / w * 100:05.2f}%",
      round(price, 2),
    ]

    return pd.concat([foods_df], ignore_index=True)

  #############################################################################
  # mutate
  #
  def mutate(self, gene):
    mutated_gene = gene.copy()

    if np.random.rand() < MUTATION_RATE:
      mutation_index = np.random.randint(0, len(gene))

      ingredient_index = list(
        self.recipe["ingredients"].keys()
      )[mutation_index]

      mutated_gene[mutation_index] = (
        str(np.random.choice(
          self.recipe["ingredients"][ingredient_index]["foods"]
        )),
        (1 - QT_FACTOR_VAR / 2) + QT_FACTOR_VAR * np.random.rand(),
      )

    return mutated_gene

  #############################################################################
  # crossover
  #
  def crossover(self, gene_a, gene_b):
    mutation_index = np.random.randint(0, len(gene_a) + 1)

    return gene_a[:mutation_index] + gene_b[mutation_index:]

  #############################################################################
  # selection
  #
  def selection(self, pool):
    selected = random.sample(pool, k=TOURNAMENT_SIZE)

    gene_a, gene_b = sorted(
      selected,
      key=lambda gene: self.fitness(gene),
      reverse=True
    )[:2]

    gene_a = self.mutate(gene_a)
    gene_b = self.mutate(gene_b)

    return self.crossover(gene_a, gene_b)

  #############################################################################
  # solve
  #
  def solve(self):
    fitness_history = []

    pool = [
      self.random_gene()
      for i in range(CANDIDATES_COUNT)
    ]

    for i in range(GENERATIONS_COUNT):
      pool = [
        self.selection(pool)
        for _ in range(CANDIDATES_COUNT)
      ]

      fitness_values = [self.fitness(gene) for gene in pool]
      fitness_history.append({
        "pool": i,
        "mean": np.mean(fitness_values),
        "max": np.max(fitness_values),
      })

    # pools = [entry["pool"] for entry in fitness_history]
    # fitness_mean = [entry["mean"] for entry in fitness_history]
    # fitness_max = [entry["max"] for entry in fitness_history]
    #
    # plt.plot(pools, fitness_mean, label="Mean")
    # plt.plot(pools, fitness_max, label="Max")
    # plt.xlabel("Generation")
    # plt.ylabel("Fitness")
    # plt.title(f"Fitness for '{self.recipe_name}'")
    # plt.legend()
    # plt.grid(True)
    # plt.savefig(f"data/fitness_{self.recipe_name}.png")

    return sorted(
      pool,
      key=lambda gene: self.fitness(gene)
    )[:PRINT_N]

################
##### MAIN #####
################

empty_df = pd.DataFrame([""], columns=[""])

with pd.ExcelWriter("ricette.xlsx") as writer:
  for _, row in recipes_totals_df.iterrows():
    recipe = Recipe(row["recipe"], row["total"])

    solutions = recipe.solve()

    dfs = []

    for solution in solutions:
      dfs.append(recipe.to_df(solution))
      dfs.append(empty_df)

    pd.concat(dfs).to_excel(writer, sheet_name=row["recipe"], index=False)

