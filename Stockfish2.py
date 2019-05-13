from Reversi import Board
import time
import math
from random import randint,choice
from numpy import inf


class Stockfish2:
    
    _initial_depth = 2
    _last_duration = 0
    
    def __init__(self, player, size):
        self._player = player
        self._remaining_turns = size**2/2
        self._remaining_time = 300
        self._max_time = self._remaining_time/self._remaining_turns
        self._coef = 3

    def update_time(duration):
        self._remaining_time -= duration
        self._remaining_turns -= 1
        self._max_time = self._remaining_time/self._remaining_turns

        
    def getPlayerMove(self, b):

        duration = 0
        depth = self._initial_depth
        expo = 0
        estimated_duration = 0
        
        while (estimated_duration < self._max_time):
            start = time.time()
            best = self.best_move(b, depth)
            end = time.time()
            duration += end-start
            depth += 1
            expo = math.log(duration, depth)
            #estimated_duration = duration + depth**(expo+1)
            #print("avec la prochaine ça prendrait " + str(estimated_duration))
            #self._coef = 2*duration/((depth-1)**expo) # 2 to be verified

        depth -= 1
        print(str(50-self._remaining_turns) + ": " +str(depth)+ " in " + str(duration)+ "s")
        #print("took " + str(duration) + "s at depth " + str(depth-1) + " which was " + str(self._coef) + "*" + str(depth-1) + "^" + str(expo))

        update_time(duration)

        #print("turn " + str(50-self._remaining_turns) + " and i still have " + str(self._remaining_time) + "(" + str(self._max_time) + " per turn)")        
        return best

    def best_move(self, b, depth):
        
        alpha = -inf
        beta = inf
        best = alpha

        for i in b.legal_moves():
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
            return -self.heuristique(b)
                
        best = inf
        for i in b.legal_moves():
            b.push(i)
            best = min(best, self.max_min(b, alpha, beta, depth-1))
            beta = min(best, beta)
            b.pop()
            if beta <= alpha:
                break
            
        return best

    def max_min(self, b, alpha, beta, depth): # c'est a toi de jouer
        
        if b.is_game_over() or depth == 0:
            return self.heuristique(b)

        best = -inf
        for i in b.legal_moves():
            b.push(i)
            best = max(best, self.min_max(b, alpha, beta, depth))
            alpha = max(best, alpha)
            b.pop()
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
        player = self._nextPlayer
        if player is self._WHITE:
            return self._nbWHITE - self._nbBLACK
        return self._nbBLACK - self._nbWHITE


    def heuristique(self, b):
        return self.mobility(b)+self.corners(b)+self.disks(b)
