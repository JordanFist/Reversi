from Reversi import Board
import time
import math
from random import randint,choice
from numpy import inf
import re


class Stockfish:
    
    _initial_depth = 2
    _last_duration = 0

    UNKNOWN = -10000
    
    def __init__(self, player, size):
        self._player = player
        self._remaining_turns = size**2/2
        self._remaining_time = 300
        self._max_time = self._remaining_time/self._remaining_turns
        self._dict = {}
        
        self._coef = 3

        
    def update_time(self, duration):
        self._remaining_time -= duration
        self._remaining_turns -= 1
        self._max_time = self._remaining_time/self._remaining_turns


    def store_value(self, b, value):
        key = re.sub('\ |\[|\]|\,', '', str(b._board))
        self._dict[key] = value
#        print("guardando em " + key)
        
    def load_value(self, b):
        
        key = re.sub('\ |\[|\]|\,', '', str(b._board))
 #       print("catando em " + key)
        if key in self._dict:
            return self._dict[key]
        else:
            return self.UNKNOWN

        
    def getPlayerMove(self, b):

        duration = 0
        depth = self._initial_depth
        expo = 0
        estimated_duration = 0
        
        while (depth < 5):
            start = time.time()
            best = self.best_move(b, depth)
            end = time.time()
            duration += end-start
            depth += 1
            expo = math.log(duration, depth)
            estimated_duration = duration + depth**(expo+0.5)

            
        print("Stockfish: " + str(round(50-self._remaining_turns)) + " - " + str(duration)+ "s")

        self.update_time(duration)        
        return best


    def order_moves(self, b, before):

        moves = []
        for i in before: # for each move
            b.push(i) # we make the move
            value = self.load_value(b) # we load its value
            moves.append((i, value)) # we add it to a new list with the move and its value
            b.pop() # we go back to the previous state of the board

        rev = b._nextPlayer == self._player # if it's our turn (maxmin), we want it ordered descendingly
        result = sorted(moves, key=lambda x: x[1], reverse=rev) 

        return result
        
    def best_move(self, b, depth):
        
        alpha = -inf
        beta = inf
        best = alpha

        moves = b.legal_moves()
    
        for i in moves:
            b.push(i)
            best = max(best, self.min_max(b, alpha, beta, depth-1))
            
            if (best > alpha):
                move = i
            alpha = max(best, alpha)
            b.pop()
            if beta <= alpha:
                break

        return move


    def min_max(self, b, alpha, beta, depth): # c'est au adversaire de jouer
        
        if b.is_game_over() or depth == 0:
            value = -self.heuristique(b)
            return value
                
        best = inf

        moves = b.legal_moves()
                
        for i in moves:
            b.push(i)
            best = min(best, self.max_min(b, alpha, beta, depth-1))
            beta = min(best, beta)
            b.pop()

            if beta <= alpha:
                break
            
        return best

    def max_min(self, b, alpha, beta, depth): # c'est a toi de jouer
        
        if b.is_game_over() or depth == 0:
            value = self.heuristique(b)
            return value

        best = -inf

        moves = b.legal_moves()
                
        for i in moves:
            b.push(i)
            best = max(best, self.min_max(b, alpha, beta, depth))
            alpha = max(best, alpha)
            b.pop()
            self.store_value(b, best)
            
            if beta <= alpha:
                break
        return best


    def corners(self, b):
        result = 0
        corner = b._boardsize-1
        board = b._board
        
        if board[0][0] == self._player:
            result += 3
        if board[0][corner] == self._player:
            result += 3
        if board[corner][0] == self._player:
            result += 3
        if board[corner][corner] == self._player:
            result += 3

        return result

    def mobility(self, b):
        return len(b.legal_moves())

    def disks(self, b):
        player = b._nextPlayer
        if player is b._WHITE:
            return b._nbWHITE - b._nbBLACK
        return b._nbBLACK - b._nbWHITE


    def heuristique(self, b):
        return self.mobility(b)+self.corners(b)+self.disks(b)
