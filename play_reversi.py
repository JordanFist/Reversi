from Reversi import Board
from Stockfish import Stockfish
from AlphaZero import AlphaZero

BOARD_SIZE = 4

def match_vs_player(board, stockfish):
    round = 0 #round = 1 pour que le joueur joue en premier
    while not (board.is_game_over()):
        print(board)
        if (round % 2 == 0):
            board.push(stockfish.return_best_move(board))
            round += 1
        else:
            print("x")
            x = input()
            print("y")
            y = input()
            move = [2, int(x), int(y)] # 2 remplacé par 1 pour que le joueur joue en premier
            board.push(move)
            round += 1

    print(board.get_winner())

# stockfish joue en premier
def match(board, stockfish, alphazero):
    while not (board.is_game_over()):
        print(board)
        if board._nextPlayer == board._BLACK:
            board.push(stockfish.return_best_move(board))
        else:
            board.push(alphazero.return_best_move(board))

    board.get_winner()

board = Board(BOARD_SIZE)
stockfish = Stockfish()
alphazero = AlphaZero()
match(board, stockfish, stockfish)

