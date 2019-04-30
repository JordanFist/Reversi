from Reversi import Board
from time import time
from random import randint,choice
from numpy import inf


class Stockfish:

    def return_best_move(self, b):
        alpha = -inf
        beta = inf
        best = alpha

        for i in b.legal_moves():
            b.push(i)
            best = max(best, self.max_min(b, alpha, beta))
            
            if (best > alpha):
                move = i
            alpha = max(best, alpha)
            b.pop()
            if beta <= alpha:
                print(move, best)

        print(move, best)

    def random_move(b):
        return choice(b.legal_moves())

    def min_max(self, b, alpha, beta):

        if b.is_game_over():
            return b.get_winner()

        best = inf
        for i in b.legal_moves():
            b.push(i)
            best = min(best, self.max_min(b, alpha, beta))
            beta = min(best, beta)
            b.pop()
            if beta <= alpha:
                return best
            
        return best

    def max_min(self, b, alpha, beta):

        if b.is_game_over():
            return b.get_winner()

        best = -inf
        for i in b.legal_moves():
            b.push(i)
            best = max(best, self.min_max(b, alpha, beta))
            alpha = max(best, alpha)
            b.pop()
            if beta <= alpha:
                return best
        return best

board = Board(4)
stockfish = Stockfish()
stockfish.return_best_move(board)
