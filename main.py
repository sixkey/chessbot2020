from chess import ChessGame
from players import RandomPlayer

# Init "chess" game 
# In this simplified version of chess, you are trying to acquire pieces of your 
# oponent, there isn't any check or mate. You can capture king just like any
# other piece. The game ends the moment any player looses all his pieces, 
# current player can't move or the max number of rounds was hit. After the 
# game is ended, the values of pieces are summed up and the player with higher
# total of piece value wins, here are the values of the pieces

# Pawn      - x_p - 1
# Bishup    - x_b - 3
# Knight    - x_h - 3
# Rook      - x_r - 5
# Queen     - x_q - 9
# King      - x_k - 20

# Pieces move like in normal chess, but there isn't en passant or castling

game = ChessGame()

# Set game parameters, white player, black player, max rounds

# Player is a object that has function move(board, color) where board is a 
# ChessBoard object. To get matrix value simply use board[row][col]. To print
# board into console use board.draw(). Color is "w" for white "b" for black.

# Player's move function needs to return from which tile where in form of  
# Tuple[Tile, Tile] where Tile = Tuple[x,y], x = int, y = int. 
# Example ((4, 1), (4, 3)) is e2 -> e4. 

# Note, if you draw the board, it is vertically flipped, that means [0, 0] is 
# in the bottom left

# Note2, if you want to test your player, I would recommend running it against
# a random player and see how many times you beat him.

# Note3, do it from scratch, the imports you can use are:
# math, random, typing, numpy, pprint

# Note4, don't use game databases 

player_white, palyer_black = RandomPlayer(), RandomPlayer()
game.new_game(player_white, palyer_black, 500)

# The result of the game, tuple of poitns for white and points for black
# ChessGame.game(draw = None) -> draw can be a fuction that gets board
result = game.game(lambda x: x.draw())
print(result)