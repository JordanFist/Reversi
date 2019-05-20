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
    _last_duration = 0

    UNKNOWN_MAX = inf
    UNKNOWN_MIN = -inf

    _turn = 0
    _visited_nodes = 0

    def __init__(self):

        self._board = Reversi.Board(10)
        self._remaining_turns = 96
        self._remaining_time = 300
        self._max_time = self._remaining_time/self._remaining_turns
        self._dict = {}
        self._openings = Openings(10)

        self._static_values=[
        [10,-3,2,1,0.8,0.8,1,2,-3,10],
        [-3,-5,-0.450,-0.500,-0.500,-0.500,-0.500,-0.450,-5,-3],
        [1,-0.45,0.030,20,10,10,20,30,-0.45,1],
        [1,-0.45,0.030,0.020,0.010,0.010,0.020,0.030,-0.45,1],
        [0.8,-0.5,0.01,0.01,0.05,0.05,0.01,0.01,-0.5,0.8],
        [0.8,-0.5,0.01,0.01,0.05,0.05,0.01,0.01,-0.5,0.8],
        [1,-0.45,0.030,0.020,0.010,0.010,0.020,0.030,-0.45,1],
        [1,-0.45,0.030,20,10,10,20,30,-0.45,1],
        [-3,-5,-0.450,-0.500,-0.500,-0.500,-0.500,-0.450,-5,-3],
        [10,-3,2,1,0.8,0.8,1,2,-3,10]
        ]


    def getPlayerName(self):
        return "Stockfish"

    def getPlayerMove(self):

        duration = 0
        depth = self._initial_depth
        expo = 0
        estimated_duration = 0

        openingMove = self._openings.getOpeningMove(self._board)
        if (openingMove != None):
            self._board.push(openingMove)
            move = (openingMove[1], openingMove[2])
            return move

        while (depth < 4):
            start = time.time()
            best = self.search(self._board, depth)
            end = time.time()
            duration += end-start
            depth += 1
            expo = math.log(duration, depth)
            estimated_duration = duration + depth**(expo+0.5)

        self.update_time(duration)

        self._board.push(best)
        move = (best[1],best[2])
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
            result += 1
        if board[0][corner] == self._player:
            result += 1
        if board[corner][0] == self._player:
            result += 1
        if board[corner][corner] == self._player:
            result += 1

        return result/4

    def mobility(self, b):
        moves = b.legal_moves()
        m=len(moves)
        if m == 1 and moves[1:] == [-1,-1]:
            return 0
        s=0
        for move in moves:
            b.push(move)
            tmp_moves=b.legal_moves()
            n=len(tmp_moves)
            if n == 1 and tmp_moves[1:] == [-1,-1]:
                s+=0
            else:
                s+=n
            b.pop()
        n=s/m
        return (m-n)/(m+n)

    def position(self, b):
        s1 =0
        s2=0
        for i in range(b._boardsize):
            for j in range(b._boardsize):
                if b._board[i][j] == b._nextPlayer:
                    s1+= self._static_values[i][j]
                elif b._board[i][j] == b._flip(b._nextPlayer):
                    s2+=1
        if (s1+s2)<0 and s2<0:
            return 1
        return (s1-s2)/(s1+s2)


        def disks(self, b):
            player = b._nextPlayer
            if player is b._WHITE:
                return b._nbWHITE - b._nbBLACK
            return b._nbBLACK - b._nbWHITE

        def heuristics(self, b):
            value = 10*self.mobility(b)+50*self.corners(b)+6*self.position(b)
            return value

    """def edge_stability(self,b):
        edges=[]
        def get_edges():
            #the northen edge
            edges.append([[0,i] for i in range(b._boardsize)])
            #the eastern edge
            edges.append( [[i, b._boardsize] for i in range(b._boardsize)])
            #the southern edge
            edges.append([[b._boardsize,i] for i in range(b._boardsize)])
            print(edges[2])
            #the western edge
            edges.append([[i, 0] for i in range(b._boardsize)])


        def is_corner(pos):
            if pos[0]==0 and (pos[1] == 0 or pos[1] == b._boardsize):
                return True
            if pos[b._boardsize]==0 and (pos[1] == 0 or pos[1] == b._boardsize):
                return True
            return False

        def probability(edge, pos):
            if is_corner(pos):
                return 0
            moves = legal_moves()
            for move in moves:
                if move[1:] in edge[0]:
                    return 1
            #all positions of the board
            positions =[ [[j,i] for i in range(b._boardsize)] for j in range(b._boardsize)]
            radius = b._boardsize/5
            #tmp has all neighboring positions even those outside the board
            tmp=[]
            for i in range(-radius, radius+1):
                for j in range(-radius, radius+1):
                    if not (i==0 and j==0):
                        tmp.append([pos[0]+i, pos[1]+j])
            #neighboring positions withing the board
            neighbords = [square for square in tmp if square in positions]
            s = 0
            for sqr in neighbors:
                if b._board[sqr[0], sqr[1]] == b._flip():
                    s+=1
            return s/( (2*radius+1) * (radius+1) -1 )


        def partial_edge_stability(edge):
                if is_filled(edge):
                    return sum( val for val in _static_edge_values)
                max_stability = -inf
                l=b.legal_moves()
                moves = [move for move in l if (move in edge[0] or move[1:] == [-1,-1]]
                if moves==[] and is_empty(edge):
                    return 0.5
                for move in moves:
                    b.push(move)
                    current_stability= probability(edge, move[1:])*partial_edge_stability(edge)

                #curr_stability = probability(edge, pos)
        def static_value(edge_index):
            edge= edges

        def get_edges():
            edges=[]
            #the northen edge
            edges.append([ [[0,i] for i in range(b._boardsize)], b._board[0]])
            for i in range(b._boardsize):
                #print(lesedges[0])
                #print(edges[0][0][i] + " " + )
            #the eastern edge
            l=[b._board[i][-1] for i in range(b._boardsize)]
            edges.append( [[[i, b._boardsize] for i in range(b._boardsize)], l])
            print(edges[1])
            #the southern edge
            edges.append([ [[b._boardsize,i] for i in range(b._boardsize)], b._board[-1]])
            print(edges[2])
            #the western edge
            l=[]
            for i in range(b._boardsize):
                l.append(b._board[i][0])
            edges.append( [[[i, 0] for i in range(b._boardsize)], l])
            print(edges)

        def is_empty(edge):
            for c in get_edge(edge):
                if c != b.board._EMPTY:
                    return False
            return True
        def is_filled(edge):
            for c in get_edge(edge):
                if c == b.board._EMPTY:
                    return False
            return True
        get_edges()
        return 1"""
