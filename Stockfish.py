import Reversi
import time
import math
from random import randint,choice
from numpy import inf
import re
from Openings import Openings
from playerInterface import *


class Stockfish(PlayerInterface):

    _initial_depth = 1
    _max_duration = 6

    UNKNOWN_MAX = inf
    UNKNOWN_MIN = -inf

    _turn = 0
    _visited_nodes = 0

    def __init__(self):

        self._board = Reversi.Board(10)
        self._remaining_turns = 48
        self._remaining_time = 290
        self._max_time = self._remaining_time/self._remaining_turns
        self._dict = {}
        self._openings = Openings(10)

        self._static_edge_values=[[700, 1200, 1000, 1000, 1000, 1000, 1000, 1000, 1200, 700],
                           [700, 200, 200, 200, 200, 200, 200, 200, 200, 700],
                           [700, -25, 75, 50, 50, 50, 50, 75, -25, 700]]

    def getPlayerName(self):
        return "Stockfish"

    def getPlayerMove(self):

        duration = 0
        depth = self._initial_depth
        estimated_duration = 0.01 # pour la premiere estimation on met une valeur approxime

        openingMove = self._openings.getOpeningMove(self._board)
        if (openingMove != None):
            self._board.push(openingMove)
            move = (openingMove[1], openingMove[2])
            self._turn += 1
            return move

        
        while estimated_duration < self._max_duration and depth <= 20: #s'il arrive a 20 c'est parce que le jeu est termine et il cherche rien
            start = time.time()
            best = self.search(self._board, depth)
            self._best_move = best
            end = time.time()
            duration += end-start
            #print(duration, estimated_duration)
            depth += 1
            base = duration**(1/depth)
            coef = duration/estimated_duration
            estimated_duration = duration + coef*base**depth

        self._turn += 1
        if self._turn >= 30:
            if self._turn >= 48:
                self._max_duration = self._remaining_time/2
            else:
                self._max_duration = self._remaining_time/(48-self._turn)

            print("max maintenant est " + str(self._max_duration))

        self.update_time(duration)
        print("depth: " + str(depth-1) + " en " + str(duration))
        self._board.push(best)
        move = (best[1],best[2])
        print("total time: " + str(300-self._remaining_time))
        return move

    def playOpponentMove(self, x,y):
        assert(self._board.is_valid_move(self._opponent, x, y))
        print("Opponent played ", (x,y))
        self._board.push([self._opponent, x, y])

    def newGame(self, color):
        self._player = color
        self._opponent = 1 if color == 2 else 2

    def endGame(self, winner):
        if self._player == winner:
            print("Stockfish won't be stopped!!!")
        else:
            print("...")


    def update_time(self, duration):
        self._remaining_time -= duration
        self._remaining_turns -= 1
        self._max_time = self._remaining_time/self._remaining_turns


    def store_value(self, b, value):
        key = re.sub('\ |\[|\]|\,', '', str(b._board))
        self._dict[key] = value

    def load_value(self, b):
        key = re.sub('\ |\[|\]|\,', '', str(b._board))
        if key in self._dict:
            return self._dict[key]
        else:
            if self._player == b._nextPlayer: # c'est max qui joue
                return self.UNKNOWN_MAX
            else:
                return self.UNKNOWN_MIN


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
        return result

    def search(self, b, depth):

        alpha = -inf
        beta = inf
        best = alpha

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

        if b.is_game_over() or depth == 0:
            value = self.heuristics(b)
            self.store_value(b, value)
            return value

        best = inf

        moves = b.legal_moves()
        ordered_moves = self.order_moves(b, moves)

        for i in ordered_moves:
            b.push(i[0])
            best = min(best, self.max_min(b, alpha, beta, depth-1))
            self._visited_nodes += 1
            beta = min(best, beta)
            b.pop()

            if beta <= alpha:
                break

        self.store_value(b, best)
        return best

    def max_min(self, b, alpha, beta, depth):

        if b.is_game_over() or depth == 0:
            value = self.heuristics(b)
            self.store_value(b, value)
            return value

        best = -inf

        moves = b.legal_moves()
        ordered_moves = self.order_moves(b, moves)

        for i in ordered_moves:
            b.push(i[0])
            best = max(best, self.min_max(b, alpha, beta, depth-1))
            alpha = max(best, alpha)
            self._visited_nodes += 1
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


    # def edge_stability(self,b):

    #     def is_corner(pos):
    #         if pos[0]==0 and (pos[1] == 0 or pos[1] == b._boardsize):
    #             return True
    #         if pos[b._boardsize]==0 and (pos[1] == 0 or pos[1] == b._boardsize):
    #             return True
    #         return False

    #     def probability(edge, pos):
    #         if is_corner(pos):
    #             return 0
    #         moves = legal_moves()
    #         for move in moves:
    #             if move[1:] in edge[0]:
    #                 return 1
    #         #all positions of the board
    #         positions =[ [[j,i] for i in range(b._boardsize)] for j in range(b._boardsize)]
    #         radius = b._boardsize/5
    #         #tmp has all neighboring positions even those outside the board
    #         tmp=[]
    #         for i in range(-radius, radius+1):
    #             for j in range(-radius, radius+1):
    #                 if not (i==0 and j==0):
    #                     tmp.append([pos[0]+i, pos[1]+j])
    #         #neighboring positions withing the board
    #         neighbords = [square for square in tmp if square in positions]
    #         s = 0
    #         for sqr in neighbors:
    #             if b._board[sqr[0], sqr[1]] == b._flip():
    #                 s+=1
    #         return s/( (2*radius+1) * (radius+1) -1 )


    #     def partial_edge_stability(edge, no_move=False):
    #             if is_filled(edge):
    #                 return sum( val for val in _static_edge_values)
    #             max_stability = -inf
    #             l=b.legal_moves()
    #             if l[0][1:] == [-1,-1]:
    #                 b.push(l[0])
    #                 curr_stability = partial_edge_stability(edge, no_move=True)
    #             moves = [move for move in  if move in edge[0]
    #             curr_stability = probability(edge, pos)
    #     def get_edges():
    #         print("################# GET EDGES##################")
    #         edges=[]
    #         #the northen edge
    #         edges.append([ [[0,i] for i in range(b._boardsize)], b._board[0]])
    #         #print("#")
    #         #print(b._board)
    #         #print(edges[0])
    #         #print("#")
    #         #the eastern edge
    #         l=[]
    #         for i in range(b._boardsize):
    #             l.append(b._board[i][-1])
    #         edges.append( [[[i, b._boardsize] for i in range(b._boardsize)], l])
    #         #print(edges[1])
    #         #the southern edge
    #         edges.append([ [[b._boardsize,i] for i in range(b._boardsize)], b._board[-1]])
    #         #print(edges[2])
    #         #the western edge
    #         l=[]
    #         for i in range(b._boardsize):
    #             l.append(b._board[i][0])
    #         edges.append( [[[i, 0] for i in range(b._boardsize)], l])
    #         #print(edges)
    #         print("################# GET EDGES##################")

    #     def is_filled(edge):
    #         for c in get_edge(edge):
    #             if c == b.board._EMPTY:
    #                 return False
    #         return True

    #     get_edges()
    #     return 1


    def disks(self, b):
        player = b._nextPlayer
        if player is b._WHITE:
            return b._nbWHITE - b._nbBLACK
        return b._nbBLACK - b._nbWHITE

    def heuristics(self, b):
        value = self.mobility(b)+self.corners(b)+5*self.disks(b)#+self.edge_stability(b)
        return value
