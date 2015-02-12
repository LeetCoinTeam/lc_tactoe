import re
import logging
import json as simplejson
from google.appengine.api import channel

from wins import Wins
#from match_results import setMatchResults
from matchmaker_results import setMatchMakerResults
from deactivate_player import deactivatePlayer


class GameUpdater():
    game = None

    def __init__(self, game):
        self.game = game

    def get_game_message(self):
        gameUpdate = {
          'board': self.game.board,
          'userX': self.game.userX.user_id(),
          'userO': '' if not self.game.userO else self.game.userO.user_id(),
          'moveX': self.game.moveX,
          'winner': self.game.winner,
          'winningBoard': self.game.winning_board,
          
          'tied': self.game.tied,
          'userXleetcoinKey' : self.game.userXleetcoinKey or '',
          'userOleetcoinKey' :self.game.userOleetcoinKey or '',
        }
        logging.info('gameUpdate: %s'%gameUpdate)
        gameJson = simplejson.dumps(gameUpdate)
        logging.info('gameJson: %s'%gameJson)
        return gameJson

    def send_update(self):
        message = self.get_game_message()
        channel.send_message(self.game.userX.user_id() + self.game.key().id_or_name(), message)
        if self.game.userO:
            channel.send_message(self.game.userO.user_id() + self.game.key().id_or_name(), message)

    def check_win(self):
        if self.game.moveX:
            # O just moved, check for O wins
            wins = Wins().o_wins
            potential_winner = self.game.userO.user_id()
        else:
            # X just moved, check for X wins
            wins = Wins().x_wins
            potential_winner = self.game.userX.user_id()
            
        ## Check for a draw.
        if self.game.moves >= 8:
            player_keys = [str(self.game.userX), str(self.game.userO)]
            player_names = [str(self.game.userX), str(self.game.userO)]
            weapons = ['X', 'O']
            

            kills = [0,0]
            deaths = [0,0]
            ranks = [1600, 1600]

                
            setMatchMakerResults(self.game, 'leetcointactoe', player_keys, player_names, weapons, kills, deaths, ranks)
            
            return
            
  
        for win in wins:
            if win.match(self.game.board):
                logging.info("potential_winner: %s" % potential_winner)
                self.game.winner = potential_winner
                self.game.winning_board = win.pattern
                
                player_keys = [str(self.game.userX), str(self.game.userO)]
                player_names = [str(self.game.userX), str(self.game.userO)]
                weapons = ['X', 'O']
                
                if potential_winner == self.game.userX.user_id():
                    kills = [1,0]
                    deaths = [0,1]
                    ranks = [1601, 1599]
                else:
                    kills = [0,1]
                    deaths = [1,0]
                    ranks = [1599, 1601]
                    
                setMatchMakerResults(self.game, 'leetcointactoe', player_keys, player_names, weapons, kills, deaths, ranks)
                
                ## deactivate players
                #if potential_winner == self.game.userX.user_id():
                #    deactivatePlayer(self.game, str(self.game.userX), 1601, 10980)
                #    deactivatePlayer(self.game, str(self.game.userO), 1599, 9000)
                #else:
                #    deactivatePlayer(self.game, str(self.game.userO), 1601, 10980)
                #    deactivatePlayer(self.game, str(self.game.userX), 1599, 9000)

                return

    def make_move(self, position, user):
        logging.info('make_move')
        logging.info('user: %s' %user)
        logging.info('self.game.userX: %s' %self.game.userX)
        logging.info('self.game.userO: %s' %self.game.userO)
        
        
        
        if position >= 0 and str(user) == str(self.game.userX) or str(user) == str(self.game.userO):
            logging.info('position >= 0 and user == self.game.userX or user == self.game.userO')
            if self.game.moveX == (str(user) == str(self.game.userX)):
                logging.info('self.game.moveX == (user == self.game.userX)')
                boardList = list(self.game.board)
                if (boardList[position] == ' '):
                    boardList[position] = 'X' if self.game.moveX else 'O'
                    self.game.board = "".join(boardList)
                    self.game.moveX = not self.game.moveX
                    self.game.moves = self.game.moves +1
                    logging.info('self.game.moves: %s' %self.game.moves)
                    self.check_win()
                    if self.game.moves >=9:
                        self.game.tied = True
                    self.game.put()
                    self.send_update()
                    return