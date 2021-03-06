#!/usr/bin/python2.4
#
# Copyright 2010 Google Inc. All Rights Reserved.

# pylint: disable-msg=C6310

"""Leetcoin Tic Tac Toe

This module demonstrates the App Engine Channel API by implementing a
simple tic-tac-toe game.

Connected through leetcoin.com
"""

import datetime
import logging
import os
import random
import re
import json as simplejson
from google.appengine.api import channel
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

from webapp2 import Route

from google.appengine.ext import deferred

from game import Game
from game_updater import GameUpdater
from wins import Wins


## leetcoin tools
## from server_create import serverCreate
## from activate_player import *


class GameFromRequest():
    game = None;

    def __init__(self, request):
        user = users.get_current_user()
        game_key = request.get('g')
        if user and game_key:
            self.game = Game.get_by_key_name(game_key)

    def get_game(self):
        return self.game


class MovePage(webapp.RequestHandler):

    def post(self):
        game = GameFromRequest(self.request).get_game()
        logging.info(game)
        user = users.get_current_user()
        logging.info(user)
        if game and user:
            id = int(self.request.get('i'))
            GameUpdater(game).make_move(id, user)


class OpenedPage(webapp.RequestHandler):
    def post(self):
        game = GameFromRequest(self.request).get_game()
        GameUpdater(game).send_update()

class MainPage(webapp.RequestHandler):
    """The main UI page, renders the 'index.html' template."""

    def get(self):
        template_values = {

                          }
        path = os.path.join(os.path.dirname(__file__), 'index.html')

        self.response.out.write(template.render(path, template_values))

class MatchmakerPage(webapp.RequestHandler):
    """The main UI page, renders the 'index.html' template."""

    def get(self):
        """Renders the main page. When this page is shown, we create a new
        channel to push asynchronous updates to the client."""

        user = users.get_current_user()
        
        if 'http' in str(user):
            return self.response.out.write("leetcoin tac toe only works with a gmail login.  ")
            
        title = "%s's game" %user
        game_key = self.request.get('g')
        game = None
        if user:
            logging.info('user found')
            if not game_key:
                logging.info('no game key found')
                
                #game_key = user.user_id()
                #return_link = 'http://leetcoin-tactoe.appspot.com/?g=' + game_key
                #server_api_key, server_secret, server_key = serverCreate('leetcoin-tactoe.appspot.com', return_link, title)
                
                
                
                ## Fire off a task to check to see if this user has authorized play on leetcoin.com
                ## deferred.defer(check_authorization, str(user), game.key(), playerid='X', _countdown=10)
                
                #result = check_authorization(str(user), game.server_secret, game.server_api_key)
                
            else:
                game = Game.get_by_key_name(game_key)
                
                if not game:
                    game = Game(key_name = game_key,
                                userX = user,
                                moveX = True,
                                board = '         ',
                                moves = 0,
                                match_key = game_key,
                                #server_api_key = server_api_key,
                                #server_secret = server_secret,
                                #server_key = server_key
                                )
                    game.put()
                
                
                if not str(game.userX) == str(user):
                    logging.info('not user X')
                
                    if not game.userO:
                        logging.info('adding user for player O')
                        
                        game.userO = user
                        game.put()
                  
                #deferred.defer(check_authorization, str(user), game.key(), playerid='O', _countdown=1)

            game_link = 'https://www.leetcoin.com/server/view/' + game_key

            if game:
                token = channel.create_channel(user.user_id() + game_key)
                template_values = {'token': token,
                                   'me': user.user_id(),
                                   'game_key': game_key,
                                   'game_link': game_link,
                                   'initial_message': GameUpdater(game).get_game_message(),
                                   'my_google_user': str(user)
                                  }
                path = os.path.join(os.path.dirname(__file__), 'matchmaker.html')

                self.response.out.write(template.render(path, template_values))
            else:
                self.response.out.write('No such game')
        else:
            self.redirect(users.create_login_url(self.request.uri))





application = webapp.WSGIApplication([
    ('/', MainPage),
    ('/mm', MatchmakerPage),
    ('/opened', OpenedPage),
    ('/move', MovePage),
    #('/_ah/login_required', OpenIDHandler),
    #('/openid_login_custom', OpenIDCustomHandler)
    ], debug=True)
    


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
