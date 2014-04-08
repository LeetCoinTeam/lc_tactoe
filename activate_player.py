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

from google.appengine.ext import deferred

from game import Game
from game_updater import GameUpdater

def check_authorization(user_str, game_key, playerid='O', count=0):
    """ check to see if a user has authorized play yet. """
    logging.info("check_authorization")
    ## get the game
    game = Game.get(game_key)
    if not game:
        return False
    
    result, leetcoinKey = activatePlayer(user_str, game.server_secret, game.server_api_key)
    logging.info('deferred')
    logging.info(result)
    if result == True:
        logging.info('player authorized')
        
        ## Which player was it?
        if playerid=='X':
            game.userXleetcoinKey = leetcoinKey
        else:
            game.userOleetcoinKey = leetcoinKey
            
        game.put()
        
        ## game = GameFromRequest(self.request).get_game()
        GameUpdater(game).send_update()
        
    else:
        logging.info('player not authorized')
        ## requeue a deferred
        logging.info('Count: %s' %count)
        count = count + 1
        if count < 10:
            deferred.defer(check_authorization, user_str, game_key, playerid=playerid, count=count, _countdown=10)
        
        
    return True

def activatePlayer(platformid, server_secret, server_api_key):
    """ send the player to the api server """

    logging.info(platformid)
    logging.info('server_secret: %s' %server_secret)
    logging.info('server_api_key: %s' %server_api_key)

    uri = "/api/activate_player"

    params = OrderedDict([
              ("nonce", time.time()),
              ("platformid", platformid)
              ])
                      
    params = urllib.urlencode(params)

    # Hash the params string to produce the Sign header value
    H = hmac.new(str(server_secret), digestmod=hashlib.sha512)
    H.update(params)
    sign = H.hexdigest()

    headers = {"Content-type": "application/x-www-form-urlencoded",
                       "Key":server_api_key,
                       "Sign":sign}
    conn = httplib.HTTPSConnection(url)
    
    conn.request("POST", uri, params, headers)

    response = conn.getresponse()
    response_text = response.read()
    json_response = json.loads(response_text)
    
    logging.info(json_response)
    
    return json_response['player_authorized'], json_response['player_platformid']