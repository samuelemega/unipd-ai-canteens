def foods_by_category(foods_df, category):
  return foods_df[foods_df["category"] == category]["id"].tolist()

def get_recipes(foods_df):
  return {
    "first-1": {  # Whole wheat pasta with lentils and vegetables
      "ingredients": {
        "i-a": {
          "foods": foods_by_category(foods_df, "cereals-and-derivatives"),
          "quantity": 0.6,
        },
        "i-b": {
          "foods": foods_by_category(foods_df, "legumes"),
          "quantity": 0.25,
        },
        "i-c": {
          "foods": foods_by_category(foods_df, "vegetables-and-greens"),
          "quantity": 0.15,
        },
      },
      "macros": {"c": 0.55, "p": 0.25, "f": 0.20}
    },

    "first-2": {  # Rice with peas and grated cheese
      "ingredients": {
        "i-a": {
          "foods": foods_by_category(foods_df, "cereals-and-derivatives"),
          "quantity": 0.65,
        },
        "i-b": {
          "foods": foods_by_category(foods_df, "legumes"),
          "quantity": 0.2,
        },
        "i-c": {
          "foods": foods_by_category(foods_df, "cheese-and-dairy"),
          "quantity": 0.15,
        },
      },
      "macros": {"c": 0.60, "p": 0.20, "f": 0.20}
    },

    "first-3": {  # Pasta with meat sauce and vegetables
      "ingredients": {
        "i-a": {
          "foods": foods_by_category(foods_df, "cereals-and-derivatives"),
          "quantity": 0.6,
        },
        "i-b": {
          "foods": foods_by_category(foods_df, "fresh-meat"),
          "quantity": 0.25,
        },
        "i-c": {
          "foods": foods_by_category(foods_df, "vegetables-and-greens"),
          "quantity": 0.15,
        },
      },
      "macros": {"c": 0.50, "p": 0.30, "f": 0.20}
    },

    "first-4": {  # Cous cous cous with chickpeas, raisins and olive oil
      "ingredients": {
        "i-a": {
          "foods": foods_by_category(foods_df, "cereals-and-derivatives"),
          "quantity": 0.5,
        },
        "i-b": {
          "foods": foods_by_category(foods_df, "legumes"),
          "quantity": 0.3,
        },
        "i-c": {
          "foods": foods_by_category(foods_df, "oils-and-fats"),
          "quantity": 0.2,
        },
      },
      "macros": {"c": 0.55, "p": 0.20, "f": 0.25}
    },

    "second-1": {  # Salmon fillet with a side of vegetables and olive oil
      "ingredients": {
        "i-a": {
          "foods": foods_by_category(foods_df, "fish-products"),
          "quantity": 0.7,
        },
        "i-b": {
          "foods": foods_by_category(foods_df, "vegetables-and-greens"),
          "quantity": 0.2,
        },
        "i-c": {
          "foods": foods_by_category(foods_df, "oils-and-fats"),
          "quantity": 0.1,
        },
      },
      "macros": {"c": 0.15, "p": 0.55, "f": 0.30}
    },

    "second-2": {  # Chicken breast with legumes and olive oil
      "ingredients": {
        "i-a": {
          "foods": foods_by_category(foods_df, "fresh-meat"),
          "quantity": 0.65,
        },
        "i-b": {
          "foods": foods_by_category(foods_df, "legumes"),
          "quantity": 0.25,
        },
        "i-c": {
          "foods": foods_by_category(foods_df, "oils-and-fats"),
          "quantity": 0.1,
        },
      },
      "macros": {"c": 0.20, "p": 0.55, "f": 0.25}
    },

    "second-3": {  # Meat burger with salad and cheese
      "ingredients": {
        "i-a": {
          "foods": foods_by_category(foods_df, "processed-and-preserved-meat"),
          "quantity": 0.6,
        },
        "i-b": {
          "foods": foods_by_category(foods_df, "vegetables-and-greens"),
          "quantity": 0.25,
        },
        "i-c": {
          "foods": foods_by_category(foods_df, "cheese-and-dairy"),
          "quantity": 0.15,
        },
      },
      "macros": {"c": 0.20, "p": 0.50, "f": 0.30}
    },

    "second-4": {  # Egg and cheese omelet, legume side dish
      "ingredients": {
        "i-a": {
          "foods": foods_by_category(foods_df, "eggs"),
          "quantity": 0.5,
        },
        "i-b": {
          "foods": foods_by_category(foods_df, "cheese-and-dairy"),
          "quantity": 0.3,
        },
        "i-c": {
          "foods": foods_by_category(foods_df, "legumes"),
          "quantity": 0.2,
        },
      },
      "macros": {"c": 0.15, "p": 0.55, "f": 0.30}
    },

    "dessert-1": {  # Fruit salad with nuts
      "ingredients": {
        "i-a": {
          "foods": foods_by_category(foods_df, "fruit"),
          "quantity": 0.85,
        },
        "i-b": {
          "foods": foods_by_category(foods_df, "nuts-and-oilseeds"),
          "quantity": 0.15,
        },
      },
      "macros": {"c": 0.65, "p": 0.10, "f": 0.25}
    },

    "dessert-2": {  # Yogurt with dried fruit and honey
      "ingredients": {
        "i-a": {
          "foods": foods_by_category(foods_df, "milk-and-yogurt"),
          "quantity": 0.7,
        },
        "i-b": {
          "foods": foods_by_category(foods_df, "nuts-and-oilseeds"),
          "quantity": 0.2,
        },
        "i-c": {
          "foods": foods_by_category(foods_df, "fruit"),
          "quantity": 0.1,
        },
      },
      "macros": {"c": 0.45, "p": 0.20, "f": 0.35}
    },

    "dessert-3": {  # Fruit compote with oil seeds
      "ingredients": {
        "i-a": {
          "foods": foods_by_category(foods_df, "fruit"),
          "quantity": 0.9,
        },
        "i-b": {
          "foods": foods_by_category(foods_df, "nuts-and-oilseeds"),
          "quantity": 0.1,
        },
      },
      "macros": {"c": 0.60, "p": 0.10, "f": 0.30}
    },

    "dessert-4": {  # Fruit smoothie with milk and seeds
      "ingredients": {
        "i-a": {
          "foods": foods_by_category(foods_df, "fruit"),
          "quantity": 0.6,
        },
        "i-b": {
          "foods": foods_by_category(foods_df, "milk-and-yogurt"),
          "quantity": 0.3,
        },
        "i-c": {
          "foods": foods_by_category(foods_df, "nuts-and-oilseeds"),
          "quantity": 0.1,
        },
      },
      "macros": {"c": 0.50, "p": 0.25, "f": 0.25}
    },
  }
