from Reversi import Board
from Stockfish import Stockfish
from Stockfish2 import Stockfish2
from AlphaZero import AlphaZero
import time
import re

BOARD_SIZE = 10

def match_vs_player(board, stockfish):
    round = 0 #round = 1 pour que le joueur joue en premier
    while not (board.is_game_over()):
        print(board)
        if (round % 2 == 0):
            board.push(stockfish.best_move(board))
            round += 1
        else:
            print("x")
            x = input()
            print("y")
            y = input()
            move = [2, int(x), int(y)] # 2 remplacé par 1 pour que le joueur joue en premier
            board.push(move)
            round += 1

    print(board.get_winner())

# stockfish joue en premier
def match(board, stockfish, alphazero):
    while not (board.is_game_over()):
        #print(board)
        if board._nextPlayer == stockfish._player:
            board.push(stockfish.getPlayerMove(board))
        else:
            board.push(alphazero.getPlayerMove(board))

    print(board)
    board.get_winner()

board = Board(BOARD_SIZE)
stockfish = Stockfish(board._WHITE, BOARD_SIZE)
alphazero = Stockfish2(board._BLACK, BOARD_SIZE)
start = time.time()
match(board, stockfish, alphazero)
end = time.time()
print("total time: " + str(end-start))
