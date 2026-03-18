import os
from dotenv import load_dotenv
import requests
import time
import jsonlines

# Json data in "info" separated into "frames"
# Each "frame" has an interval of "frameInterval" in "info[frameInterval]"
# Within each frame, the 10 participant(players) data are stored under "participantFrames" in "info[frames][participantFrames]"
# Within each participant frame, the relevant data for the project are:
# "totalGold", "xp", "level", "jungleMinionsKilled" + "minionsKilled"

class Timeline:
    def __init__(self, puuid, region):
        self.puuid = puuid
        self.region = region
        self.api_key = os.getenv("RIOT_API_KEY")
        self.headers = {"X-Riot-Token": self.api_key}

    def api(self, match_id):
        api = f"https://{self.region}.api.riotgames.com/lol/match/v5/matches/{match_id}/timeline"
        response = requests.get(api, headers = self.headers)
        if response.status_code == 200:
            time.sleep(1)
            return response.json()
        elif response.status_code == 429:
            time.sleep(10)
            print("Rate limited, waiting 10s")
            return response.json()
        else:
            raise Exception(response.status_code, response.reason)
        
    def stats(self, match_id):
        result = []
        timeline = self.api(match_id)
        # Frames are in 1min intervals

        for participant in timeline["info"]["participants"]:
            if participant["puuid"] == self.puuid:
                participant_id = participant["participantId"]
                break

        if participant_id <= 5:
            player_team = range(1, 5+1)
            enemy_team = range(6, 10+1)
        else:
            player_team = range(6, 10+1)
            enemy_team = range(1, 5+1)

        for frame_number, frame in enumerate(timeline["info"]["frames"]):
            player_frame = frame["participantFrames"][str(participant_id)]

            cs = player_frame["jungleMinionsKilled"] + player_frame["minionsKilled"]
            gold = player_frame["totalGold"]
            xp = player_frame["xp"]
            level = player_frame["level"]
            player_team_gold = 0
            enemy_team_gold = 0
            player_team_xp = 0
            enemy_team_xp = 0

            for player in player_team:
                player_team_gold += frame["participantFrames"][str(player)]["totalGold"]
                player_team_xp += frame["participantFrames"][str(player)]["xp"]

            for enemy in enemy_team:
                enemy_team_gold += frame["participantFrames"][str(enemy)]["totalGold"]
                enemy_team_xp += frame["participantFrames"][str(enemy)]["xp"]

            frame_stats = {"match_id": match_id,"minute": frame_number,"cs": cs, "gold": gold, "xp": xp, "level": level, "player_team_gold": player_team_gold, "player_team_xp": player_team_xp, "enemy_team_gold": enemy_team_gold, "enemy_team_xp": enemy_team_xp}
            result.append(frame_stats)
            
        return result