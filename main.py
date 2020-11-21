from chess import *
from premade_players import *

# Init chess game 
game = ChessGame()

# Set game parameters, white player, black player, max rounds
# Player is a object that has function move(board, color) where board is a 
# ChessBoard object. To get matrix value simply use board[row][col]. To print
# board into console use board.draw()
game.new_game(RandomPlayer(), RandomPlayer(), 500)

# The result of the game, tuple of poitns for white and points for black
# ChessGame.game(draw = False) -> if draw is True print chessboard every move
result = game.game(True)
print(result)