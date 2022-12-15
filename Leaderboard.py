'''
    Leaderboard class for the sliding puzzle game
    This class is for the purpose of keeping track of the number of moves
    in the sliding puzzle game
'''


class ScoreKeeper:
    # initialize move when the program is first loaded, the default is zero
    def __init__(self):
        self.score = 0

    # add move if player made a legal swap of tile
    def add_score(self):
        self.score = self.score + 1
        return self.score

    # reset move back to zero when player loads a new puzzle
    def reset_score(self):
        self.score = 0

    # return a string representation of the score for display and
    # for the leaderboard
    def __str__(self):
        return self.score
