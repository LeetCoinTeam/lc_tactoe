
class Server():
    """ a leetcoin server """
    def __init__(self, title, hostAddress, hostPort, hostConnectionLink, gameKey, maxActivePlayers, maxAuthorizedPlayers, minimumBTCHold,
                incrementBTC, serverRakeBTCPercentage, serverAdminUserKey, leetcoinRakePercentage, allowNonAuthorizedPlayers, stakesClass, 
                motdShowBanner, motdBannerColor, motdBannerText ):
        
        self.title = title
        self.hostAddress = hostAddress
        self.hostPort = hostPort
        self.hostConnectionLink = hostConnectionLink
        self.gameKey = gameKey
        self.maxActivePlayers = maxActivePlayers
        self.maxAuthorizedPlayers = maxAuthorizedPlayers
        self.minimumBTCHold = minimumBTCHold
        self.incrementBTC = incrementBTC
        self.serverRakeBTCPercentage = serverRakeBTCPercentage
        self.serverAdminUserKey = serverAdminUserKey
        self.leetcoinRakePercentage = leetcoinRakePercentage
        self.allowNonAuthorizedPlayers = allowNonAuthorizedPlayers
        self.stakesClass = stakesClass
        self.motdShowBanner = motdShowBanner
        self.motdBannerColor = motdBannerColor
        self.motdBannerText = motdBannerText
        
    def to_dict(self):
        return ({
                u'title': self.title,
                u'hostAddress': self.hostAddress,
                u'hostPort': self.hostPort,
                u'hostConnectionLink': self.hostConnectionLink,
                u'gameKey': self.gameKey,
                u'maxActivePlayers': self.maxActivePlayers,
                u'maxAuthorizedPlayers': self.maxAuthorizedPlayers,
                u'minimumBTCHold': self.minimumBTCHold,
                u'incrementBTC': self.incrementBTC,
                u'serverRakeBTCPercentage': self.serverRakeBTCPercentage,
                u'serverAdminUserKey': self.serverAdminUserKey,
                u'leetcoinRakePercentage': self.leetcoinRakePercentage,
                u'allowNonAuthorizedPlayers': self.allowNonAuthorizedPlayers,
                u'stakesClass': self.stakesClass,
                u'motdShowBanner': self.motdShowBanner,
                u'motdBannerColor': self.motdBannerColor,
                u'motdBannerText': self.motdBannerText,
                })
                
    def to_min_dict(self):
        return ({
                u'gameKey': self.gameKey,
                u'hostConnectionLink': self.hostConnectionLink,
                u'title': self.title,
                })
                
    def to_small_dict(self):
        return ({
                u'gameKey': self.gameKey
                })