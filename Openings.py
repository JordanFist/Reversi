from Reversi import Board
import re

class Openings:

    def __init__(self):
        self.__openings = {}
        self.data()

    def getOpeningMove(self, b):
        key = re.sub('\ |\[|\]|\,', '', str(b._board))
        if (key in self.__openings):
            return self.__openings[key]
        return None

    def data(self):
        key = re.sub('\ |\[|\]|\,', '', str(b._board))
        self.__openings[key] = [1, 2, 3]
        #self.__openings[""] = [1, 2, 3]

b = Board()
openings = Openings()
openings.getOpeningMove(b)