from player_info import PlayerInfo
from match_ingester import MatchIngester
from match_v5 import MatchV5
from timeline import Timeline

class Session():
    def __init__(self, name , tag , region, queue):
        self.region = region
        self.queue = queue
        self.player = PlayerInfo(name = name, tag = tag, region = self.region)
        self.puuid = self.player.get_puuid()
        self.match_ingester = MatchIngester(puuid = self.puuid, region = self.region, queue = self.queue)
        self.timeline = Timeline(puuid = self.puuid, region = self.region)

    def get_puuid(self):
        return self.puuid
    
    def get_region(self):
        return self.region
    
    def get_queue(self):
        return self.queue

    def fetch_match(self):
        self.match = self.match_ingester.fetch_match()
        return self.match

    def get_timeline(self, match_id):
        timeline_stats = self.timeline.stats(match_id)
        return timeline_stats