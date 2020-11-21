import math
import random

def dxdy_generator(x, y, dx, dy, size, max_range=math.inf, included=False):
    if not included:
        x += dx
        y += dy
    counter = 0
    while in_range(0, size, x, y) and counter < max_range:
        yield x, y
        x += dx
        y += dy
        counter+=1

def in_range(min_value, max_value, *values):
    return all([min_value <= val < max_value for val in values])

def row_to_str(start, values, sep="|"):
    res = f" {start} {sep}"

    for value in values:
        cell = f"{value}"
        cell += " " * (3 - len(cell))
        res += cell+sep
    return res

def row_barrier(number):
    if number == 0:
        return ""
    return "+---" * number + "+"

class Matrix:
    def __init__(self, size, def_value=0):
        self.size = size
        self.values = [[def_value for x in range(size)] for y in range(size)]
        self.def_value = def_value

    def copy(self):
        res = Matrix(self.size, self.def_value)
        for y in range(self.size):
            for x in range(self.size):
                res[y][x] = self.values[y][x]
        return res

    def fill(self, value, left=0, top=0, right=-1, bottom=-1):
        if right < 0:
            right = self.size
        if bottom < 0:
            bottom = self.size

        for y in range(top, bottom):
            for x in range(left, right):
                self.values[y][x] = value

    def __iter__(self):
        for y in range(self.size):
            yield self.values[y]

    def __getitem__(self, index):
        return self.values[index]

    def __str__(self):
        return "\n".join([str(x) for x in self.values])

    def get_line_to_edge(self, x, y, dx, dy):
        current = (x, y)
        res = []
        while in_range(0, self.size, *current):
            res.append(values[current[1]][current[0]])
            current = (current[0] + dx, current[1] + dy)
        return res

    def get(self, point):
        return self.values[point[1]][point[0]]

    def set(self, point, value):
        self.values[point[1]][point[0]] = value

class ChessBoard:

    def __init__(self):
        self.matrix = Matrix(8, " ")
        self.fill = self.matrix.fill
        self.get = self.matrix.get
        self.set = self.matrix.set

        self.pieces_values = {
            "p": 1,
            "b": 3,
            "h": 3,
            "r": 5,
            "q": 9,
            "k": 20
        }

    def reset(self):
        self.matrix.fill(" ")
        self.matrix.fill("w_p", 0, 1, 8, 2)
        self.matrix[0][0] = "w_r"
        self.matrix[0][7] = "w_r"
        self.matrix[0][1] = "w_h"
        self.matrix[0][6] = "w_h"
        self.matrix[0][2] = "w_b"
        self.matrix[0][5] = "w_b"
        self.matrix[0][3] = "w_q"
        self.matrix[0][4] = "w_k"

        self.matrix.fill("b_p", 0, 6, 8, 7)
        self.matrix[7][0] = "b_r"
        self.matrix[7][7] = "b_r"
        self.matrix[7][1] = "b_h"
        self.matrix[7][6] = "b_h"
        self.matrix[7][2] = "b_b"
        self.matrix[7][5] = "b_b"
        self.matrix[7][3] = "b_q"
        self.matrix[7][4] = "b_k"
        
    def draw(self, state=None):

        if not state:
            state = self.matrix

        size = state.size
        barrier = "   " + row_barrier(size)
        print(row_to_str(" ", [f" {chr(ord('A') + x)} " for x in range(size)], " "))
        print(barrier)
        for y in range(size):
            print(row_to_str(size - y, state[size - y - 1]))
            print(barrier)
    
    def possible_moves(self, x, y):
        board = self.matrix
        piece_whole = board[y][x]
        
        if piece_whole == " ":
            return None
        
        color = piece_whole[0]
        piece = piece_whole[2]
        res = set()

        lines = []
        
        if piece == "p":
            y_direction = 1 if color == "w" else -1
            speed = 2 if (color == "w" and y == 1) or (color == "b" and y == 6) else 1
            
            for move in dxdy_generator(x, y, 0, y_direction, 8, speed):
                piece_on_board = board.get(move)
                if piece_on_board == " ":
                    res.add(move)
                else:
                    break

            move = (x - 1, y + y_direction)
            if in_range(0, 8, *move) and board.get(move) != " " and board.get(move)[0] != color:
                res.add(move)

            move = (x + 1, y + y_direction)
            if in_range(0, 8, *move) and board.get(move) != " " and board.get(move)[0] != color:
                res.add(move)
        
        if piece == "r":
            lines = [
                dxdy_generator(x, y, -1, 0, 8),
                dxdy_generator(x, y, 1, 0, 8),
                dxdy_generator(x, y, 0, -1, 8),
                dxdy_generator(x, y, 0, 1, 8)
            ]
        elif piece == "b":
            lines = [
                dxdy_generator(x, y, -1, -1, 8),
                dxdy_generator(x, y, 1, 1, 8),
                dxdy_generator(x, y, -1, 1, 8),
                dxdy_generator(x, y, 1, -1, 8)
            ]
        elif piece == "q":
            lines = [
                dxdy_generator(x, y, -1, 0, 8),
                dxdy_generator(x, y, 1, 0, 8),
                dxdy_generator(x, y, 0, -1, 8),
                dxdy_generator(x, y, 0, 1, 8),
                dxdy_generator(x, y, -1, -1, 8),
                dxdy_generator(x, y, 1, 1, 8),
                dxdy_generator(x, y, -1, 1, 8),
                dxdy_generator(x, y, 1, -1, 8)
            ]
        elif piece == "k":
            lines = [
                dxdy_generator(x, y, -1, 0, 8, 1),
                dxdy_generator(x, y, 1, 0, 8, 1),
                dxdy_generator(x, y, 0, -1, 8, 1),
                dxdy_generator(x, y, 0, 1, 8, 1),
                dxdy_generator(x, y, -1, -1, 8, 1),
                dxdy_generator(x, y, 1, 1, 8, 1),
                dxdy_generator(x, y, -1, 1, 8, 1),
                dxdy_generator(x, y, 1, -1, 8, 1)
            ]
        elif piece == "h":
            lines = [
                dxdy_generator(x, y, -2, -1, 8, 1),
                dxdy_generator(x, y, -2, 1, 8, 1),
                dxdy_generator(x, y, 2, -1, 8, 1),
                dxdy_generator(x, y, 2, 1, 8, 1),
                dxdy_generator(x, y, -1, -2, 8, 1),
                dxdy_generator(x, y, -1, 2, 8, 1),
                dxdy_generator(x, y, 1, -2, 8, 1),
                dxdy_generator(x, y, 1, 2, 8, 1)
            ]

        for line in lines:
            for move in line:
                piece_on_board = board.get(move)
                if piece_on_board == " ":
                    res.add(move)
                else:
                    if piece_on_board[0] != color:
                        res.add(move)
                    break
        return res

    def draw_possible_moves(self, x, y):
        matrix_copy = self.matrix.copy()
        moves = self.possible_moves(x, y)

        
        if moves:
            for move in moves:
                matrix_copy[move[1]][move[0]] = " X "     
        self.draw(matrix_copy)

    def is_legal_move(self, move_from, move_to, color):
        if not in_range(0, 8, *[*move_from, *move_to]):
            return False

        piece_from = self.matrix.get(move_from)
        
        if piece_from == " ":
            return False
        if piece_from[0] != color:
            return False

        return move_to in self.possible_moves(*move_from)

    def is_there_move(self, color):
        for y in range(8):
            for x in range(8):
                piece = self.get((x, y))
                if piece == " ":
                    continue
                if piece[0] == color:
                    if len(self.possible_moves(x, y)) > 0:
                        return True
        return False

    def move(self, move_from, move_to, color):
        if not self.is_legal_move(move_from, move_to, color):
            return None
        
        self.matrix[move_to[1]][move_to[0]] = self.matrix.get(move_from)
        self.matrix[move_from[1]][move_from[0]] = " "

        return True

    def get_pieces_value(self):
        res_w = 0
        res_b = 0

        for y in range(8):
            for x in range(8):
                piece = self.get((x, y))
                if piece == " ":
                    continue

                value = self.pieces_values[piece[2]]

                if piece[0] == "w":
                    res_w += value
                if piece[0] == "b":
                    res_b += value

        return res_w, res_b

    def __iter__(self):
        for y in self.board:
            yield y
    
    def __getitem__(self, row):
        return self.board[row]

class ChessGame:

    def __init__(self):
        self.board = ChessBoard()
        self.new_game(None, None)

    def new_game(self, player_w, player_b, max_moves = 500):
        self.board.reset()
        self.player_w = player_w
        self.player_b = player_b
        self.move_counter = 0
        self.max_moves = max_moves
    
    def game(self, draw = None):
        game_running = True
        
        color = "w"

        val_a, val_b = self.board.get_pieces_value()

        while game_running:
            val_a, val_b = self.board.get_pieces_value()

            if val_a * val_b == 0:
                print(f"One of the players has lost all his pieces")
                break

            if not self.board.is_there_move(color):
                print(f"Player playing {'white' if color == 'w' else 'black'} has" + \
                " nowhere to move")
                break
            
            if self.move_counter >= self.max_moves:
                print(f"The max number of moves was hit")
                break

            current_player = self.player_w if self.move_counter % 2 == 0 else self.player_b
            
            move_from, move_to = current_player.move(self.board, color)

            if not self.board.move(move_from, move_to, color):
                print(f"Player playing {'white' if color == 'w' else 'black'} made \
                an illegal move")

            if draw:
                draw(self.board)
            
            self.move_counter += 1
            color = "w" if self.move_counter % 2 == 0 else "b"

        if val_a > val_b:
            return 2, 0
        elif val_a < val_b:
            return 0, 2
        else:
            return 1, 1

game = ChessGame()
game.new_game(RandomPlayer(), RandomPlayer())
result = game.game(True)
print(result)