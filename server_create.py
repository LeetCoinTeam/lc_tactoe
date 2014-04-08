import webapp2
import time
import json
import hashlib
import hmac
import urllib
import httplib
import logging
from collections import OrderedDict
from config import *
from server import Server

def serverCreate(hostAddress, hostConnectionLink, title):

    uri = "/api/server_create"
    
    server = Server(
        title,                                          # title, 
        hostAddress,                                  # hostAddress, 
        "80",                                        # hostPort, 
        hostConnectionLink,                            # hostConnectionLink, 
        game_key,                                       # gameKey, 
        2,                                            # maxActivePlayers, 
        2,                                             # maxAuthorizedPlayers, 
        10000,                                          # minimumBTCHold,
        1000,                                           # incrementBTC, 
        0.01,                                           # serverRakeBTCPercentage, 
        None,                                           # serverAdminUserKey, 
        0.01,                                           # leetcoinRakePercentage, 
        False,                                          # allowNonAuthorizedPlayers, 
        "LOW",                                         # stakesClass, 
        False,                                          # motdShowBanner, 
        "F00",                                          # motdBannerColor, 
        "leetcoin-tac-toe",                                  # motdBannerText
    )
    
    server_json = json.dumps(server.to_min_dict())
    
    nonce = time.time()
    
    params = OrderedDict([
              ("nonce", nonce),
              ("server", server_json),
              ])
                      
    params = urllib.urlencode(params)

    # Hash the params string to produce the Sign header value
    H = hmac.new(developer_shared_secret, digestmod=hashlib.sha512)
    H.update(params)
    sign = H.hexdigest()
    
    logging.info("Sign: %s" %sign)
    logging.info("nonce: %s" %nonce)
    logging.info("developer_api_key: %s" %developer_api_key)
    

    headers = {"Content-type": "application/x-www-form-urlencoded",
                       "Key":developer_api_key,
                       "Sign":sign}
    conn = httplib.HTTPSConnection(url)
    
    conn.request("POST", uri, params, headers)
    response = conn.getresponse()
    response_text = response.read()
    json_response = json.loads(response_text)
    logging.info(json_response['server']['apiKey'])
            
    return json_response['server']['apiKey'], json_response['server']['apiSecret'], json_response['server']['key'] 