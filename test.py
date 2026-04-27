import json

with open("data/champions.json", "r") as file:
    data = json.load(file)


champions = [{"id": champ_id, "name": champ_data["name"]} for champ_id, champ_data in data["data"].items()]

print(champions)
