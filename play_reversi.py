from Reversi import Board
from time import time
from random import randint,choice
from numpy import inf

####################################################################
# Ceux à quoi on doit arriver sur ce fichier
####################################################################
from Reversi import Board
from Stockfish import Stockfish
from AlphaZero import AlphaZero

BOARD_SIZE = 8

# stockfish joue en premier
def match(board, stockfish, alphazero):
    round = 0
    while not (board.is_game_over()):
        print(board)
        if (round % 2 == 0):
            board.push(stockfish.returnBestMove(board))
            round += 1
        else:
            board.push(alphazero.returnBestMove(board))
            round += 1

    print(board.get_winner())

board = Board(BOARD_SIZE)
stockfish = Stockfish()
alphazero = AlphaZero()


####################################################################


####################################################################
# Ceux qui doit disparaitre
####################################################################
        
        
start = time()
b = Reversi.Board(4)

#random_match(b)
min_max(b, -inf, inf)
end = time()
print(end - start, 'secondes')
