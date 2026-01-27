from player_info import PlayerInfo
import os
from dotenv import load_dotenv
import requests
import time

## USES THE MATCH-V5 API FROM RIOT
class MatchID:
    def __init__(self, name, tag, region, queue):
        load_dotenv(override=True)
        try:
            self.api_key = os.getenv("RIOT_API_KEY")
        except:
            raise ValueError("No API Key")
        queue_type = {
            "ranked": 420,
            "normal": 400,
            "flex": 440
        }
        region_hosts = {
            "europe": "https://europe.api.riotgames.com",
            "americas": "https://americas.api.riotgames.com",
            "asia": "https://asia.api.riotgames.com"
        }

        self.region = region_hosts[region.lower()]
        self.queue = queue_type[queue.lower()]
        self.player = PlayerInfo(name = name, tag = tag, region = region)
        self.puuid = self.player.get_puuid()

        self.headers = {
            "X-Riot-Token": self.api_key
        }

    def match_ids(self, startTime = None, endTime = None, queue = None, type = None, start = None, count = None):
        actual_queue = queue if queue is not None else self.queue
        query_params = {"startTime": startTime, "endTime": endTime, "queue": actual_queue, "type": type, "start": start, "count": count}
        params = []
        for key, value in query_params.items():
            if value is not None:
                params.append(key + "=" + str(value))
        params_str = "?" + "&".join(params) if params else ""
        api = f"{self.region}/lol/match/v5/matches/by-puuid/{self.puuid}/ids{params_str}"
        response = requests.get(api, headers = self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(response.status_code, response.reason)
    
    def match(self, match_id):
        api = f"{self.region}/lol/match/v5/matches/{match_id}"
        response = requests.get(api, headers = self.headers)
        time.sleep(1) # Sleep for 1s to prevent rate limit exceeded
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(response.status_code, response.reason)