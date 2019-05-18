from Reversi import Board
import re

class Openings:
    __BLACK = 1
    __WHITE = 2

    def __init__(self, boardSize):
        self.__boardSize = boardSize
        self.__symmetryYX = {}
        self.__symmetryYMinusX = {}
        self.__openings = {}

        self.__initSymmetryYX()
        self.__initSymmetryYMinusX()
        self.blackData()
        self.whiteData()
        
        self.addAllSymmetries()

        #for key, move in self.__openings.items():
        #    print(move)
        #    self.printKey(key)

    def printKey(self, key):
            for i in range(len(key)):
                if (i != 0 and i % 10 == 0):
                    print()
                print(key[i], end='')
            print("\n")

    """ Returns a book move """
    def getOpeningMove(self, b):
        key = re.sub('\ |\[|\]|\,', '', str(b._board))
        if (key in self.__openings):
            return self.__openings[key]
        return None

    """ Initialises the simmetryYX dictionnary """
    def __initSymmetryYX(self):
        size = self.__boardSize ** 2
        j = 0
        for i in range(size):
            if (i != 0 and i % 10 == 0):
                j += 1
            self.__symmetryYX[i] = (size - 1) - (i % 10) * self.__boardSize - j

    """ Initialises the simmetryYMinusX dictionnary """
    def __initSymmetryYMinusX(self):
        j = 0
        for i in range(self.__boardSize ** 2):
            if (i != 0 and i % 10 == 0):
                j += 1
            self.__symmetryYMinusX[i] = (i % 10) * self.__boardSize + j

    """ Returns the key applied with the symmetry Y = X """
    def symmetricalBoardYX(self, key):
        newKey = list(key)
        for i in range(self.__boardSize):
            for j in range(self.__boardSize - i):
                newKey[j + i * self.__boardSize], newKey[self.__symmetryYX[j + i * self.__boardSize]] = newKey[self.__symmetryYX[j + i * self.__boardSize]], newKey[j + i * self.__boardSize]
        return ("".join(newKey))

    """ Returns the key applied with the symmetry Y = -X """
    def symmetricalBoardYMinusX(self, key):
        newKey = list(key)
        for i in range(self.__boardSize):
            for j in range(0 + i, self.__boardSize):
                newKey[j + i * self.__boardSize], newKey[self.__symmetryYMinusX[j + i * self.__boardSize]] = newKey[self.__symmetryYMinusX[j + i * self.__boardSize]], newKey[j + i * self.__boardSize]
        return ("".join(newKey))
    
    """ Returns the key applied with the two previous symmetry """
    def symmetricalBoardCombination(self, key):
        newKey = self.symmetricalBoardYX(key)
        newKey = self.symmetricalBoardYMinusX(newKey)
        return newKey

    """ Changes coordinates to index """
    def coordinatesToIndex(self, x, y):
        return int(str(y) + str(x))

    """ Changes index to coordinates"""
    def indexToCoordinates(self, i):
        return (int(str(i)[1]), int(str(i)[0]))

    """ Adds all the symmetrical boards in the opening dicts """
    def addAllSymmetries(self):
        symmetricalOpenings = {}
        for key, move in self.__openings.items():
            coord = self.indexToCoordinates(self.__symmetryYX[self.coordinatesToIndex(move[1], move[2])])
            symmetricalOpenings[self.symmetricalBoardYX(key)] = [move[0], coord[0], coord[1]]

            coord = self.indexToCoordinates(self.__symmetryYMinusX[self.coordinatesToIndex(move[1], move[2])])
            symmetricalOpenings[self.symmetricalBoardYMinusX(key)] = [move[0], coord[0], coord[1]]

            coord = self.indexToCoordinates(self.__symmetryYX[self.__symmetryYMinusX[self.coordinatesToIndex(move[1], move[2])]])
            symmetricalOpenings[self.symmetricalBoardCombination(key)] = [move[0], coord[0], coord[1]]

        self.__openings.update(symmetricalOpenings)

    """ Adds black book moves in the dictionnary """
    def blackData(self):
        # Depth = 1
        self.__openings["0000000000"
                        "0000000000"
                        "0000000000"
                        "0000000000"
                        "0000120000"
                        "0000210000"
                        "0000000000"
                        "0000000000"
                        "0000000000"
                        "0000000000"] = [self.__BLACK, 6, 4]

        # Depth = 2
        self.__openings["0000000000"
                        "0000000000"
                        "0000000000"
                        "0000210000"
                        "0000210000"
                        "0000210000"
                        "0000000000"
                        "0000000000"
                        "0000000000"
                        "0000000000"] = [self.__BLACK, 4, 3]
        self.__openings["0000000000"
                        "0000000000"
                        "0000000000"
                        "0000012000"
                        "0000120000"
                        "0000210000"
                        "0000000000"
                        "0000000000"
                        "0000000000"
                        "0000000000"] = [self.__BLACK, 4, 6]
        self.__openings["0000000000"
                        "0000000000"
                        "0000000000"
                        "0000010000"
                        "0000110000"
                        "0000222000"
                        "0000000000"
                        "0000000000"
                        "0000000000"
                        "0000000000"] = [self.__BLACK, 6, 4]

    """ Adds white book moves in the dictionnary """
    def whiteData(self):
        # Depth = 1
        self.__openings["0000000000"
                        "0000000000"
                        "0000000000"
                        "0000010000"
                        "0000110000"
                        "0000210000"
                        "0000000000"
                        "0000000000"
                        "0000000000"
                        "0000000000"] = [self.__WHITE, 3, 6]
        # Depth = 2
        self.__openings["0000000000"
                        "0000000000"
                        "0000000000"
                        "0000011100"
                        "0000120000"
                        "0000210000"
                        "0000000000"
                        "0000000000"
                        "0000000000"
                        "0000000000"] = [self.__WHITE, 3, 4]
        self.__openings["0000000000"
                        "0000000000"
                        "0000000000"
                        "0000012000"
                        "0000111000"
                        "0000210000"
                        "0000000000"
                        "0000000000"
                        "0000000000"
                        "0000000000"] = [self.__WHITE, 3, 4]
        self.__openings["0000000000"
                        "0000000000"
                        "0000000000"
                        "0000012000"
                        "0000120000"
                        "0000110000"
                        "0000100000"
                        "0000000000"
                        "0000000000"
                        "0000000000"] = [self.__WHITE, 2, 5]
        self.__openings["0000000000"
                        "0000000000"
                        "0000000000"
                        "0000012000"
                        "0000120000"
                        "0001110000"
                        "0000000000"
                        "0000000000"
                        "0000000000"
                        "0000000000"] = [self.__WHITE, 2, 5]


#b = Board(10)
#openings = Openings(10)
