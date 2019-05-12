from Reversi import Board
from time import time
from random import randint,choice
from numpy import inf


class Stockfish:


    
    current_depth = 0
    max_depth = 0

    pieces = 4

    def __init__(self, player):
        self.player = player

        
    def getPlayerMove(self, b):
        return self.best_move(b, 10)

    def corners(self, b):
        result = 0
        corner = b._boardsize-1
        
        if b[0][0] == player:
            result += 1
        if b[0][corner] == player:
            result += 1
        if b[corner][0] == player:
            result += 1
        if b[corner][corner] == player:
            result += 1

        return result

    def amount_legal_moves(self, b):
        return len(b.legal_moves())

    def best_move(self, b, depth):

        current_pieces = b.get_nb_pieces()
        self.pieces = current_pieces[0]+current_pieces[1]
        self.current_depth = 0
        self.max_depth = depth
        
        alpha = -inf
        beta = inf
        best = alpha

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

        current_pieces = b.get_nb_pieces()
        if current_pieces[0]+current_pieces[1] > self.pieces:
            self.current_depth += 1
            self.pieces = current_pieces[0]+current_pieces[1]
        
        if b.is_game_over() or self.current_depth >= self.max_depth:
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
        
        current_pieces = b.get_nb_pieces()
        if current_pieces[0]+current_pieces[1] > self.pieces:
            self.current_depth += 1
            self.pieces = current_pieces[0]+current_pieces[1]
            
        if b.is_game_over() or self.current_depth >= self.max_depth:
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

