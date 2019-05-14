from Reversi import Board
import time
import math
from random import randint,choice
from numpy import inf
import re


class Stockfish2:
    
    _initial_depth = 2
    _last_duration = 0
    
    UNKNOWN_MAX = -10000
    UNKNOWN_MIN = 10000

    _turn = 0
    _visited_nodes = 0
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
        #print("guardando " + str(value) + " em " + key)
        self._dict[key] = value
        
    def load_value(self, b):
        key = re.sub('\ |\[|\]|\,', '', str(b._board))
        if key in self._dict:
            #print("li " + str(self._dict[key]) + " em " + key)
            return self._dict[key]
        else:
            if self._player == b._nextPlayer: # c'est max qui joue
                #print("li " + str(self.UNKNOWN_MIN) + " em " + key)
                return self.UNKNOWN_MIN
            else:
                #print("li " + str(self.UNKNOWN_MAX) + " em " + key)
                return self.UNKNOWN_MAX
        
    def getPlayerMove(self, b):

        duration = 0
        depth = self._initial_depth
        expo = 0
        estimated_duration = 0
        
        while (depth < 4):
            start = time.time()
            best = self.search(b, depth)
            end = time.time()
            duration += end-start
            depth += 1
            expo = math.log(duration, depth)
            estimated_duration = duration + depth**(expo+0.5)

        #print("Stockfish2: " + str(round(50-self._remaining_turns)) + " - " + str(duration)+ "s")

        self.update_time(duration)
        return best


    def order_moves(self, b, before):

        self._visited_nodes += 1
        moves = []
        for i in before: # for each move
            b.push(i) # we make the move
            value = self.load_value(b) # we load its value
            moves.append((i, value)) # we add it to a new list with the move and its value
            b.pop() # we go back to the previous state of the board

        rev = b._nextPlayer == self._player # if it's our turn (maxmin), we want it ordered descendingly
        result = sorted(moves, key=lambda x: x[1], reverse=rev) 
        #result = moves
        return result
        
    def search(self, b, depth):
        
        alpha = -inf
        beta = inf
        best = alpha
        #print("turn " + str(self._turn))
        self._turn += 1
        
        moves = b.legal_moves()
        ordered_moves = self.order_moves(b, moves)    
        
        for i in ordered_moves:
            b.push(i[0])
            best = max(best, self.min_max(b, alpha, beta, depth-1))
            if (best > alpha):
                move = i[0]
            alpha = max(best, alpha)
            b.pop()
            if beta <= alpha:
                break

        self.store_value(b, best)
        return move


    def min_max(self, b, alpha, beta, depth):

        #print("min")
        if b.is_game_over() or depth == 0:
            value = -self.heuristics(b)
            self.store_value(b, value)
            return value
                
        best = inf

        moves = b.legal_moves()
        ordered_moves = self.order_moves(b, moves)    
        
        for i in ordered_moves:
            b.push(i[0])
            best = min(best, self.max_min(b, alpha, beta, depth-1))
            beta = min(best, beta)
            b.pop()
                    
            if beta <= alpha:
                break

        self.store_value(b, best)
        return best

    def max_min(self, b, alpha, beta, depth):

        #print("max")
        if b.is_game_over() or depth == 0:
            value = self.heuristics(b)
            self.store_value(b, value)
            return value

        best = -inf

        moves = b.legal_moves()
        ordered_moves = self.order_moves(b, moves)    
        
        for i in ordered_moves:
            b.push(i[0])
            best = max(best, self.min_max(b, alpha, beta, depth))
            alpha = max(best, alpha)
            b.pop()
            
            if beta <= alpha:
                break

        self.store_value(b, best)
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
        return len(b.legal_moves()*2)

    def disks(self, b):
        player = b._nextPlayer
        if player is b._WHITE:
            return b._nbWHITE - b._nbBLACK
        return b._nbBLACK - b._nbWHITE

    def heuristics(self, b):
        value = self.mobility(b)+self.corners(b)+self.disks(b)
        #self.store_value(b, value)
        return value
