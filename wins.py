import re

class Wins():
    x_win_patterns = ['XXX......',
                    '...XXX...',
                    '......XXX',
                    'X..X..X..',
                    '.X..X..X.',
                    '..X..X..X',
                    'X...X...X',
                    '..X.X.X..']

    o_win_patterns = map(lambda s: s.replace('X','O'), x_win_patterns)
  
    x_wins = map(lambda s: re.compile(s), x_win_patterns)
    o_wins = map(lambda s: re.compile(s), o_win_patterns)
