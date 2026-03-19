import pandas as pd
import numpy as np
from database import Database

class Data():
    def __init__(self):
        self.db = Database()

    def return_stats(self, puuid, limit = 20):
        rows = [dict(row) for row in self.db.get_matches(puuid, limit)]
        df = pd.DataFrame(rows)
        if df.empty:
            return df
        
        df["cs"] = df["total_minions_killed"] + df["neutral_minions_killed"]
        df["kda"] = ((df["kills"] + df["assists"]) / df["deaths"].replace(0,1)).round(1)
        df["game_start_time"] = pd.to_datetime(df["game_start_timestamp"], unit = "ms")
        df.drop(columns=["total_minions_killed", "neutral_minions_killed", "game_start_timestamp"], inplace=True)
        return df
    
    def return_champion_stats(self, puuid, champion, limit = 20):
        champion = champion.replace(" ", "")
        rows = [dict(row) for row in self.db.get_champion_matches(puuid, champion, limit)]
        df = pd.DataFrame(rows)
        if df.empty:
            return df
        
        df["cs"] = df["total_minions_killed"] + df["neutral_minions_killed"]
        df["kda"] = ((df["kills"] + df["assists"]) / df["deaths"].replace(0,1)).round(1)
        df["game_start_time"] = pd.to_datetime(df["game_start_timestamp"], unit = "ms")
        df.drop(columns=["total_minions_killed", "neutral_minions_killed", "game_start_timestamp"], inplace=True)
        return df
    
    def return_role_stats(self, puuid, position, limit = 20):
        rows = [dict(row) for row in self.db.get_role_matches(puuid, position, limit)]
        df = pd.DataFrame(rows)
        if df.empty:
            return df
        df["cs"] = df["total_minions_killed"] + df["neutral_minions_killed"]
        df["kda"] = ((df["kills"] + df["assists"]) / df["deaths"].replace(0,1)).round(1)
        df["game_start_time"] = pd.to_datetime(df["game_start_timestamp"], unit = "ms")
        df.drop(columns=["total_minions_killed", "neutral_minions_killed", "game_start_timestamp"], inplace=True)
        return df
    
    def return_timeline_stats(self, match_id):
        rows = [dict(row) for row in self.db.get_match_timeline(match_id)]
        df = pd.DataFrame(rows)
        if df.empty:
            return df
        return df