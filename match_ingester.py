from match_v5 import MatchV5
import jsonlines

class MatchIngester():
    def __init__(self, puuid, region, queue):
        self.puuid = puuid
        self.region = region
        self.queue = queue
        self.Player = MatchV5(puuid = self.puuid, region = self.region, queue = self.queue)
        self.seen_match_ids = set()
        try:
            with jsonlines.open("data/match_data.jsonl", mode = "r") as reader:
                for record in reader:
                    id = record.get("matchID")
                    if id:
                        self.seen_match_ids.add(id)
        except FileNotFoundError:
            pass

        self.wanted_stats = ("championName", "individualPosition", "kills", "deaths", "assists", "totalMinionsKilled", "win")
    
    def fetch_match(self):
        results = []

        start = 0
        page_size = 20
        while True:
            self.match_ids = self.Player.match_ids(start = start, count = page_size)

            if not self.match_ids:
                break

            for match_id in self.match_ids:
                if match_id not in self.seen_match_ids:
                    try:
                        self.match = self.Player.match(match_id)
                    except:
                        raise Exception("Match fetch failed")
                    
                    self.player_list = self.match["metadata"]["participants"]
                    player_index = None
                    for index, participant in enumerate(self.player_list): # Store player index
                        if participant == self.puuid:
                            player_index = index
                            break
                    if player_index == None:
                        raise Exception("Player PUUID not found")
                    match_details = self.match["info"]["participants"][player_index]

                    gameStartTimestamp = self.match["info"]["gameStartTimestamp"]
                    wanted_match_details = {"matchID": match_id, "puuid": self.puuid, "gameStartTimestamp": gameStartTimestamp}
                    for stat in self.wanted_stats:
                        if stat in match_details:
                            wanted_match_details[stat] = match_details[stat]

                    with jsonlines.open("data/match_data.jsonl", mode = "a") as writer:
                        writer.write(wanted_match_details)
                        self.seen_match_ids.add(match_id)
                    
                    results.append(wanted_match_details)

                else:
                    continue
                
            start += page_size

        return results