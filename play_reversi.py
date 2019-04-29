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
def random_move(b):
    return choice(b.legal_moves())
    
def random_match(b):
    if b.is_game_over():
        print(b)
        print(b.get_winner())
        return

    print(b)
    print(b.heuristique(b._nextPlayer))
    b.push(random_move(b))
    random_match(b)
    b.pop()
    

def every_match(b):
    '''Effectue un déroulement aléatoire du jeu de morpion.'''
    #print("----------")
    #print(b)
    if b.is_game_over():
        #pieces = b.get_nb_pieces()
        #print(pieces)
        b.get_winner()
        return

    for move in b.legal_moves():
        b.push(move)
        every_match(b)
        b.pop()

def min_max(b, alpha, beta):

    if b.is_game_over():
        return b.get_winner()

    best = inf
    for i in b.legal_moves():
        b.push(i)
        best = min(best, max_min(b, alpha, beta))
        beta = min(best, beta)
        b.pop()
        if beta <= alpha:
            break;
    print(b)
    return best

def max_min(b, alpha, beta):

    if b.is_game_over():
        return b.get_winner()

    best = -inf
    for i in b.legal_moves():
        b.push(i)
        best = max(best, min_max(b, alpha, beta))
        alpha = max(best, alpha)
        b.pop()
        if beta <= alpha:
            break;
    print(b)
    return best
        
        
start = time()
b = Reversi.Board(4)

#random_match(b)
min_max(b, -inf, inf)
end = time()
print(end - start, 'secondes')
