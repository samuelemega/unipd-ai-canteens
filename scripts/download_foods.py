import requests
from bs4 import BeautifulSoup
import re
import json

host_url = "https://www.alimentinutrizione.it/"
food_list_url = "tabelle-nutrizionali/ricerca-per-ordine-alfabetico"

def get_food_list():
    response = requests.get(f"{host_url}/{food_list_url}")
    soup = BeautifulSoup(response.text, "html.parser")

    return [a.get("href") for a in soup.select("#listTwo li a")]

def get_food(food_url):
    food = {}

    response = requests.get(f"{host_url}/{food_url}")
    soup = BeautifulSoup(response.text, "html.parser")

    table_main = soup.select(".table")[0]
    table_data = soup.select_one(".tblmain")

    ##################
    ### MAIN TABLE ###
    ##################

    rows = table_main.select("tr")

    for row in rows:
        cols = row.select("td")

        if len(cols) == 2:
            food[cols[0].text] = cols[1].text

    ##################
    ### DATA TABLE ###
    ##################

    groups = [
        table_data.select("tr.corponutriente"),
        table_data.select("tr.corpominerali"),
        table_data.select("tr.corpovitamine"),
        table_data.select("tr.corpograssi"),
        table_data.select("tr.corpoaminoacidi"),
        table_data.select("tr.corpoaltri"),
    ]

    for rows in groups:
        for row in rows:
            cols = row.select("td")
            food[cols[0].text] = re.sub(r"[^\d.,-]", "", cols[2].text).strip()

    return food

foods = []

for food_url in get_food_list():
    print(f"Parsing {food_url}")
    foods.append(get_food(food_url))

with open('foods.json', 'w') as f:
    json.dump(foods, f, indent=2)
