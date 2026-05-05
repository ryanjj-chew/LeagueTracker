import pandas as pd
import champions

class Data_Flask():
    def __init__(self, rows):
        self.rows = rows

    def return_stats(self):
        rows = [dict(row) for row in self.rows]
        df = pd.DataFrame(rows)
        version = champions.get_latest_version()

        if df.empty:
            return df
        
        df["cs"] = df["total_minions_killed"] + df["neutral_minions_killed"]
        df["kda"] = ((df["kills"] + df["assists"]) / df["deaths"].replace(0,1)).round(1)
        df["game_start_time"] = pd.to_datetime(df["game_start_timestamp"], unit="ms")
        df["game_start_time"] = df["game_start_time"].dt.strftime("%d %b %Y, %H:%M")
        df.drop(columns=["total_minions_killed", "neutral_minions_killed", "game_start_timestamp"], inplace=True)
        df["position"] = df["position"].str.title()
        df["champion_icon"] = f"https://ddragon.leagueoflegends.com/cdn/{version}/img/champion/" + df["champion_name"] + ".png"
        df["role_icon"] = ("https://raw.communitydragon.org/latest/plugins/rcp-fe-lol-clash/global/default/assets/images/position-selector/positions/icon-position-" + df["position"].str.strip().str.lower() + "-hover.png")

        return df.to_dict(orient="records")