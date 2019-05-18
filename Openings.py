from Reversi import Board
import re

class Openings:
    __BLACK = 1
    __WHITE = 2

    def __init__(self, boardSize):
        self.__boardSize = boardSize
        self.__simmetryYX = {}
        self.__simmetryYMinusX = {}
        self.__openings = {}

        self.__initSimmetryYX()
        self.__initSimmetryYMinusX()
        #self.blackData()
        #self.whiteData()

    """ Returns a book move """
    def getOpeningMove(self, b):
        key = re.sub('\ |\[|\]|\,', '', str(b._board))
        if (key in self.__openings):
            return self.__openings[key]
        return None

    """ Initialises the simmetryYX dictionnary """
    def __initSimmetryYX(self):
        size = self.__boardSize ** 2 - 1
        k = 0
        for i in range(self.__boardSize):
            for j in range(self.__boardSize - i):
                self.__simmetryYX[j + i * self.__boardSize] = size - j * self.__boardSize - k
            k += 1

    """ Initialises the simmetryYMinusX dictionnary """
    def __initSimmetryYMinusX(self):
        k = 0
        for i in range(self.__boardSize):
            for j in range(0 + i, self.__boardSize):
                self.__simmetryYMinusX[j + i * self.__boardSize] = j * self.__boardSize + k
            k += 1
        print(self.__simmetryYMinusX)

    """ Returns the key applied with the symmetry Y = X """
    def symetricalBoardYX(self, key):
        newKey = list(key)
        for i,j in self.__simmetryYX.items():
            newKey[i], newKey[j] = newKey[j], newKey[i]
        return ("".join(newKey))

    """ Returns the key applied with the symmetry Y = -X """
    def symetricalBoardYMinusX(self, key):
        newKey = list(key)
        for i,j in self.__simmetryYMinusX.items():
            newKey[i], newKey[j] = newKey[j], newKey[i]
        return ("".join(newKey))
    
    """ Returns the key applied with the two previous symmetry """
    def symetricalBoardCombination(self, key):
        newKey = self.symetricalBoardYX(key)
        newKey = self.symetricalBoardYMinusX(newKey)
        return newKey

    """ Adds black book moves in the dictionnary """
    def blackData(self):
        self.__openings["0000000000"
                        "0000000000"
                        "0000000000"
                        "0000000000"
                        "0000120000"
                        "0000210000"
                        "0000000000"
                        "0000000000"
                        "0000000000"
                        "0000000000"] = [self.__BLACK, 4, 5]

    """ Adds white book moves in the dictionnary """
    def whiteData(self):
        self.__openings["0000000000"
                        "0000000000"
                        "0000000000"
                        "0000000000"
                        "0000120000"
                        "0000210000"
                        "0000000000"
                        "0000000000"
                        "0000000000"
                        "0000000000"] = [self.__BLACK, 4, 5]

b = Board(10)
openings = Openings(10)

