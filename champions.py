import json, requests

lang = "en_US"
version_link = "https://ddragon.leagueoflegends.com/api/versions.json"


def get_latest_version():
    response = requests.get(version_link, timeout=10)
    response.raise_for_status()
    versions = response.json()
    return versions[0]

def get_champions():
    latest_version = get_latest_version()
    response = requests.get(f"https://ddragon.leagueoflegends.com/cdn/{latest_version}/data/{lang}/champion.json")
    response.raise_for_status()
    champions = response.json()
    return champions

def save_champions():
    champions = get_champions()
    with open("data/champions.json", "w") as file:
        json.dump(champions, file)
    return