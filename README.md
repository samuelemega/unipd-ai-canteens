# AI-driven Sustainable Meal Planning in Institutional Canteens

## Panoramic

### Motivation and Goal

The project aims to develop an AI-based system to optimize weekly meal plans in institutional canteens (e.g. schools, hospitals, NGOs, workplaces).

The objectives are to:
- Ensure nutritionally balanced meals in line with WHO and CREA guidelines,
- Reduce food waste by prioritizing ingredients already in stock,
- Encourage the use of seasonal and locally sourced foods,
- Incorporate users' dietary preferences and restrictions,
- Minimize environmental impact by assigning an "eco-score" to each ingredient based on production method, origin, and emissions.

This work aligns with Sustainable Development Goals such as Zero Hunger and Responsible Consumption and Production.

### Data and Implementation

- **Nutritional data** (macronutrients and energy values) will be sourced from the official CREA food composition database.
- **Environmental impact scores** and **Seasonality score** are not available.

The system will be implemented in **Python**.

## Details

### Generic idea

The following context should be defined:
- A list of **foods**, for each food should be specified:
  - macronutrients
  - seasonality-score
  - eco-score
  - availability
  - price
  - last time the food was used
- A list of **recipes**, for each recipe should be specified:
  - a list of **ingredients**, for each ingredient should be specified:
    - a list of **foods** with similar macronutrients, that can be alternatively
      chosen
    - the quantity in terms of weight with respect to the toal
- The canteen propopses:
  - *N1* recipes for the starter, coming in *S1* different sizes
  - *N2* recipes for the first course, coming in *S2* different sizes
  - *N3* recipes for the second course, coming in *S3* different sizes
  - *N4* recipes for the dessert, coming in *S4* different sizes
- Each user votes:
  - each recipe for the starter from the most favourite to the least favourite
  - each recipe for the first course from the most favourite to the least
    favourite
  - each recipe for the second course from the most favourite to the least
    favourite
  - each recipe for the dessert from the most favourite to the least favourite
  - a size for the starter
  - a size for the first course
  - a size for the second course
  - a size for the dessert

The algorithm should implement the next steps:
  - chooses the **recipes**:
    - chooses the *M1* most favourite recipes for the starter
    - chooses the *M2* most favourite recipes for the first course
    - chooses the *M3* most favourite recipes for the second course
    - chooses the *M4* most favourite recipes for the dessert
  - chooses the **ingredients** for the recipes in order to:
    - prefer the foods already present in house
    - prefer the foods that, if buyed, cost less
    - prefer the foods not used recently
    - prefer the foods with a low eco-score
    - prefer the foods with high seasonality-score

#### Recipe choice

In order to lower the food waste, is important that as many users as possibile
are satisfied by the recipes finally chosen by the canteen.
To prioritize the choice of the recipes, the application will use the technique
of **Ranked Pairs**.
More specifically, the Python package `pyrankvote` will be used to determine the
most preferred recipes.

#### Ingredients choice

We chose metaheuristic approaches (**Genetic Algorithms**) over Soft CSPs
because they offer greater flexibility in handling multiple soft constraints — 
such as nutrition, cost, stock availability, and environmental
impact — using a unified objective function.

The soft constraints we are considering are:
- Environmental impact
- Seasonality
- Warehouse availability
- Stock shortage cost
- Last use
- Nutritional balance

#### Context

The context of the application is defined by:
- **Foods repository**: registry containing macronutrients, eco-score and
  seasonality-score of each food
- **Recipes repository**: registry containing all the recipes
- **Warehouse**: registry containing the availability of each food
- **Market**: registry containing the price on the market of each food

## Run

```
python3 scripts/random_preferences.py
python3 scripts/choose_recipes.py
python3 scripts/choose_ingredients.py
```
