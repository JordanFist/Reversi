from Reversi import Board
from time import time
from random import randint,choice
from numpy import inf


class Stockfish:

    def return_best_move(self, b):
        alpha = -inf
        beta = inf
        best = alpha

  #      print("no best move o player é o " + str(b._nextPlayer))

        for i in b.legal_moves():
            b.push(i)
            best = max(best, self.min_max(b, alpha, beta))
            if (best > alpha):
                move = i
            alpha = max(best, alpha)
            b.pop()
            if beta <= alpha:
                break

        print("the best value for " + str(b._nextPlayer) + " is " + str(best))
        return move

    def random_move(b):
        return choice(b.legal_moves())

    def min_max(self, b, alpha, beta): # c'est au adversaire de jouer

        if b.is_game_over():
 #           print("a heuristica achou " + str(b.heuristique(b._nextPlayer)) + " pro " + str(b._nextPlayer))
            return -b.heuristique()
                
        best = inf
        for i in b.legal_moves():
            b.push(i)
            best = min(best, self.max_min(b, alpha, beta))
            beta = min(best, beta)
            b.pop()
            if beta <= alpha:
                break
            
        return best

    def max_min(self, b, alpha, beta): # c'est a toi de jouer

        if b.is_game_over():
#            print("a heuristica achou " + str(b.heuristique(b._nextPlayer)) + " pro " + str(b._nextPlayer))
            return b.heuristique()

        best = -inf
        for i in b.legal_moves():
            b.push(i)
            best = max(best, self.min_max(b, alpha, beta))
            alpha = max(best, alpha)
            b.pop()
            if beta <= alpha:
                break
        return best

