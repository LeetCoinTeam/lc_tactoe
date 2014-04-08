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
from game import Game

def deactivatePlayer(game, platformid, rank, satoshi_balance):
    """ send the list to the api server """

    logging.info("platformid: %s" %platformid)
    logging.info("rank: %s" %rank)
    logging.info("satoshi_balance: %s" %satoshi_balance)
    
    uri = "/api/deactivate_player"

    params = OrderedDict([
              ("nonce", time.time()),
              ("platformid", platformid),
              #("rank", rank),
              #("satoshi_balance", satoshi_balance)
              ])
                      
    params = urllib.urlencode(params)

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