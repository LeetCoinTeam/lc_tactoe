from google.appengine.ext import db

class Game(db.Model):
    """All the data we store for a game"""
    userX = db.UserProperty()
    userO = db.UserProperty()
    board = db.StringProperty()
    moveX = db.BooleanProperty()
    winner = db.StringProperty()
    winning_board = db.StringProperty()
    ## We need to keep track of the server key which is assigned by leetcoin
    #server_key = db.StringProperty()
    #server_api_key = db.StringProperty()
    #server_secret = db.StringProperty()
    
    ## We need to store the leetcoin userids
    userXleetcoinKey = db.StringProperty()
    userOleetcoinKey = db.StringProperty()
    
    match_key = db.StringProperty()