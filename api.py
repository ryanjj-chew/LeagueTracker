import requests

## Uses the ACCOUNT-V1 API FROM RIOT
class Functions:
    def __init__(self, api, name, tag, region):
        self.headers = {"X-Riot-Token": api}
        self.name = name
        self.tag = tag
        self.region = region.lower()
        region_hosts = {
            "europe": "https://europe.api.riotgames.com",
            "americas": "https://americas.api.riotgames.com",
            "asia": "https://asia.api.riotgames.com"
        }
        try:
            self.region_host = region_hosts[self.region]
        except:
            raise ValueError("Invalid Region")

    def get_puuid(self):
        account_v1_puuid_url = f"{self.region_host}/riot/account/v1/accounts/by-riot-id/{self.name}/{self.tag}"
        response = requests.get(account_v1_puuid_url, headers = self.headers)
        if response.status_code == 200:
            return response.json()["puuid"]
        else:
            raise Exception(response.status_code, response.reason)