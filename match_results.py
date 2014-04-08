import webapp2
import time
import json
import hashlib
import hmac
import urllib
import httplib
import logging
from config import *
from collections import OrderedDict

## our player data structure
from player import Player

def setMatchResults(game, map_title, player_keys, player_names, weapons, kills, deaths, ranks):
    """ send the list to the api server """
    logging.info(player_keys)
    logging.info(player_names)
    logging.info(weapons)
    logging.info(kills)
    logging.info(deaths)
    logging.info(ranks)
    logging.info(map_title)

    playerlist = []
    
    for index, playerkey in enumerate(player_keys):
        player = Player(
            playerkey,
            int(kills[index]),
            int(deaths[index]),
            player_names[index],
            weapons[index],
            ranks[index]
        )
        # key, kills, deaths, name, weapon, rank
        
        playerlist.append(player.to_dict())
        
    player_json_list = json.dumps(playerlist)
        
    uri = "/api/put_match_results"
    
    params = OrderedDict([
                      ("map_title", map_title),
                      ("nonce", time.time()),
                      ("player_dict_list", player_json_list),
                      ])
                      
    params = urllib.urlencode(params)
    
    logging.info(params)
    logging.info('game.server_secret: %s' %game.server_secret)

    # Hash the params string to produce the Sign header value
    H = hmac.new(str(game.server_secret), digestmod=hashlib.sha512)
    H.update(params)
    sign = H.hexdigest()

    headers = {"Content-type": "application/x-www-form-urlencoded",
                       "Key":game.server_api_key,
                       "Sign":sign}
                       
    conn = httplib.HTTPSConnection(url)
    
    conn.request("POST", uri, params, headers)
    response = conn.getresponse()
    
    return response.read()