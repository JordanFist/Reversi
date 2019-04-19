import Reversi
import time
from random import randint,choice
from numpy import inf


def get_winner(b):
    '''Fonction qui évalue la victoire (ou non) en tant que X. Renvoie 1 pour victoire, 0 pour 
    égalité et -1 pour défaite. '''
    score = b.get_nb_pieces()
    if score[0] > score[1]:
        return b._WHITE
    elif score[1] > score[0]:
        return b._BLACK
    else:
        return 0

def random_move(b):
    return choice(b.legal_moves())
    
def random_match(b):
    if b.is_game_over():
        print(b)
        print(get_winner(b))
        return

    print(b)
    print(b.heuristique(b._nextPlayer))
    b.push(random_move(b))
    random_match(b)
    b.pop()
    

def every_match(b):
    '''Effectue un déroulement aléatoire du jeu de morpion.'''
    #print("----------")
    #print(b)
    if b.is_game_over():
        #pieces = b.get_nb_pieces()
        #print(pieces)
        get_winner(b)
        return

    for move in b.legal_moves():
        b.push(move)
        every_match(b)
        b.pop()

def min_max(b, alpha, beta):

    if b.is_game_over():
        return get_winner(b)

    best = inf
    for i in b.legal_moves():
        b.push(i)
        best = min(best, max_min(b, alpha, beta))
        beta = min(best, beta)
        b.pop()
        if beta <= alpha:
            break;
    print(b)
    return best

def max_min(b, alpha, beta):

    if b.is_game_over():
        return get_winner(b)

    best = -inf
    for i in b.legal_moves():
        b.push(i)
        best = max(best, min_max(b, alpha, beta))
        alpha = max(best, alpha)
        b.pop()
        if beta <= alpha:
            break;
    print(b)
    return best
        
        
start = time.time()
b = Reversi.Board(4)

#random_match(b)
min_max(b, -inf, inf)
end = time.time()
print(end-start)
