class HumanPlayer:

    def __init__(self):
        print("""
            You've loaded human, player. If you want to move, first select a 
            piece with "s <column as a letter> <row as a number>" example for
            white "s e 2", then move it by "m <column as a letter> <row as a
            number>.
        """)

    def move(self, board, color):
        selected = None
        selected_moves = []

        board.draw()

        while True:
            player_input = input(f"Move for {'white' if color == 'w' else 'black'}: ")
            words = player_input.split()
            
            if len(words) < 3 or len(words[2]) > 1 or len(words[1]) > 1:
                print("Invalid syntax")
                continue
            
            words[0] = words[0].upper()
            words[1] = words[1].upper()

            if not words[1] in "ABCDEFGH" or not words[2] in "12345678":
                print("Column has to be a letter a-h, row needs to be a number 1 - 8")
                continue

            if words[0] == "S":
                selected = ((ord(words[1]) - ord("A")), int(words[2]) - 1)
                selected_moves = board.possible_moves(*selected)
                board.draw_possible_moves(*selected)
            elif words[0] == "M" and selected:
                res = ((ord(words[1]) - ord("A")), int(words[2]) - 1)
                if board.is_legal_move(selected, res, color):
                    return selected, res
                else:
                    print("Illegal move")

class RandomPlayer:
    
    def __init__(self):
        pass
    
    def move(self, board, color):

        all_moves = []

        for y in range(8):
            for x in range(8):
                piece = board.get((x, y))
                if piece == " ":
                    continue
                if piece[0] == color:
                    moves = board.possible_moves(x, y)
                    for move in moves:
                        all_moves.append(((x, y), move))

        return random.choice(all_moves)