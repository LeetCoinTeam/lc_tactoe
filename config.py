## Developer key and secret, Obtainable here:  www.leetcoin.com/developer/

## Game key, which is used to identify the game that is being played
## This points to leetcoin-tac-toe, which can be viewed here:  www.leetcoin.com/game/view/agpzfjEzMzdjb2luchELEgRHYW1lGICAgIDHuZ8LDA
## If you want to deploy another appengine instance of this code, you can use this game key, or create your own game in the leetcoin developer console.
game_key = "agpzfjEzMzdjb2luchELEgRHYW1lGICAgIDHuZ8LDA"

## Are we running on the development server?
local_testing = False

if local_testing:
    url="localhost:10081"
    developer_api_key = "xxx"
    developer_shared_secret = "xxx"
else:
    url="apitest-dot-1337coin.appspot.com"
    developer_api_key = "xxx"
    developer_shared_secret = "xxx"