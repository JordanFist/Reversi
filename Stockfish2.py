from Reversi import Board
import time
from random import randint,choice
from numpy import inf


class Stockfish2:
    
    _current_depth = 0
    _max_depth = 0
    _turn = 0
    _mid_game = 60 # quand on change de strategie (il faut bien verifier ce numero)
    _max_time = 3
    

    def __init__(self, player):
        self.player = player

        
    def getPlayerMove(self, b):

        depth = 30

        if self._turn >= 30:
            _depth = 15

        duration = 0
        while (duration < self._max_time/1.75):
            start = time.time()
            best = self.best_move(b, depth)
            end = time.time()
            duration += end-start
            depth += 1

        print("fui ate " + str(depth) + " em " + str(duration))
        return best
        
    def corners(self, b):
        result = 0
        corner = b._boardsize-1
        board = b._board
        
        if board[0][0] == self.player:
            result += 1
        if board[0][corner] == self.player:
            result += 1
        if board[corner][0] == self.player:
            result += 1
        if board[corner][corner] == self.player:
            result += 1

        return result

    def mobility(self, b):
        return len(b.legal_moves())

    def heuristique(self, b):
        return self.mobility(b)+self.corners(b)

    def best_move(self, b, depth):

        current_pieces = b.get_nb_pieces()
        self._current_depth = 0
        self._max_depth = depth
        
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

        #print("the best value for " + str(b._nextPlayer) + " is " + str(best))
        return move

    def random_move(b):
        return choice(b.legal_moves())

    def min_max(self, b, alpha, beta): # c'est au adversaire de jouer

        if len(b.stack) > self._pieces:
            self._current_depth += 1
            self._pieces = current_pieces[0]+current_pieces[1]
        
        if b.is_game_over() or self._current_depth >= self._max_depth:
 #           print("a heuristica achou " + str(b.heuristique(b._nextPlayer)) + " pro " + str(b._nextPlayer))
            return -self.heuristique(b)
                
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
        
        if len(b.stack) > self._pieces:
            self._current_depth += 1
            self.pieces = current_pieces[0]+current_pieces[1]
            
        if b.is_game_over() or self._current_depth >= self._max_depth:
#            print("a heuristica achou " + str(b.heuristique(b._nextPlayer)) + " pro " + str(b._nextPlayer))
            return self.heuristique(b)

        best = -inf
        for i in b.legal_moves():
            b.push(i)
            best = max(best, self.min_max(b, alpha, beta))
            alpha = max(best, alpha)
            b.pop()
            if beta <= alpha:
                break
        return best

