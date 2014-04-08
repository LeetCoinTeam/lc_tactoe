
class Player():
    """ a leetcoin player """
    def __init__(self, key, kills, deaths, name, weapon, rank):
        self.key = key
        self.kills = kills
        self.deaths = deaths
        self.name = name
        self.rank = rank
        self.weapon = weapon
        
    def to_dict(self):
        return ({
                u'key': self.key,
                u'kills': self.kills,
                u'deaths': self.deaths,
                u'name': self.name,
                u'rank': self.rank,
                u'weapon': self.weapon
                })