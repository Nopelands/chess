def is_square_inside_board(x, y):
    answer = 0 <= x < 8 and 0 <= y < 8
    return answer


def fen_to_board(fen):
    answer = []
    info_list = fen.split(" ")
    board_state = info_list[0].split("/")
    final_board = [[] for i in range(8)]
    for i in range(len(board_state)):  # places pieces and fills empty spaces when a number is found
        for j in range(len(board_state[i])):
            if board_state[i][j].isnumeric():
                for k in range(int(board_state[i][j])):
                    final_board[i].append("empty")
            else:
                final_board[i].append(board_state[i][j])
    answer.append(final_board)
    answer.append(info_list[1])
    answer.append(info_list[2])
    a_char_ord_constant = 97
    if len(info_list[3]) > 1:  # converts notation to xy coordinates
        info_list[3] = str(ord(info_list[3][0]) - a_char_ord_constant) + info_list[3][1]
    answer.append(info_list[3])
    return answer


class Board:
    board = []  # coordinates work in y x notation
    player_to_move = ""
    castling_rights = []
    en_passant_target = []

    def __init__(self, fen):
        info = fen_to_board(fen)
        self.board = info[0]
        self.player_to_move = info[1]
        self.castling_rights = info[2]
        self.en_passant_target = info[3]

    def get_king_square(self):
        king = "k"
        if self.player_to_move == "b":
            king = king.upper()
        for j in range(8):
            for i in range(8):
                if self.board[j][i] == king:
                    return str(i) + str(j)

    def board_read(self, x, y):
        return self.board[y][x]

    def board_write(self, x, y, input):
        self.board[y][x] = input

    def square_is_under_attack(self, x, y):
        enemy = "rnbqkp"
        if self.player_to_move == "w":
            enemy = enemy.upper()
            # checks for existing en passants and black pawn attacks
            if str(x) + str(y - 1) == self.en_passant_target:
                if is_square_inside_board(x + 1, y) and self.board[y][x + 1] == enemy[5]:
                    return True
                if is_square_inside_board(x - 1, y) and self.board[y][x - 1] == enemy[5]:
                    return True
            # this checks for generic black pawn attacks
            else:
                if is_square_inside_board(x + 1, y + 1) and self.board[y + 1][x + 1] == enemy[5]:
                    return True
                if is_square_inside_board(x - 1, y + 1) and self.board[y + 1][x - 1] == enemy[5]:
                    return True
        else:
            # checks for existing en passants and white pawn attacks
            if str(x) + str(y + 1) == self.en_passant_target:
                if is_square_inside_board(x + 1, y) and self.board[y][x + 1] == enemy[5]:
                    return True
                if is_square_inside_board(x - 1, y) and self.board[y][x - 1] == enemy[5]:
                    return True
            # checks for generic white pawn attacks
            else:
                if is_square_inside_board(x + 1, y - 1) and self.board[y - 1][x + 1] == enemy[5]:
                    return True
                if is_square_inside_board(x - 1, y - 1) and self.board[y - 1][x - 1] == enemy[5]:
                    return True
        # this checks for rooks and queens with sight to the left of x
        cursor = x - 1
        while is_square_inside_board(cursor, y):
            if self.board[y][cursor] == "empty":
                cursor = cursor - 1
            elif self.board[y][cursor] == enemy[0] or self.board[y][cursor] == enemy[3]:
                return True
            else:
                cursor = -1
        # this checks for rooks and queens with sight to the right of x
        cursor = x + 1
        while is_square_inside_board(cursor, y):
            if self.board[y][cursor] == "empty":
                cursor = cursor + 1
            elif self.board[y][cursor] == enemy[0] or self.board[y][cursor] == enemy[3]:
                return True
            else:
                cursor = -1
        # this checks for rooks and queens with sight upwards of y
        cursor = y - 1
        while is_square_inside_board(x, cursor):
            if self.board[cursor][x] == "empty":
                cursor = cursor - 1
            elif self.board[cursor][x] == enemy[0] or self.board[cursor][x] == enemy[3]:
                return True
            else:
                cursor = -1
        # this checks for rooks and queens with sight downwards of y
        cursor = y + 1
        while is_square_inside_board(cursor, y):
            if self.board[cursor][x] == "empty":
                cursor = cursor + 1
            elif self.board[cursor][x] == enemy[0] or self.board[cursor][x] == enemy[3]:
                return True
            else:
                cursor = -1
        # this checks for bishops and queens in the direction of the first quadrant
        cursor_x = x + 1
        cursor_y = y + 1
        while is_square_inside_board(cursor_x, cursor_y):
            if self.board[cursor_y][cursor_x] == "empty":
                cursor_x += 1
                cursor_y += 1
            elif self.board[cursor_y][cursor_x] == enemy[2] or self.board[cursor_y][cursor_x] == enemy[3]:
                return True
            else:
                cursor_x = -1
        # this checks for bishops and queens in the direction of the second quadrant
        cursor_x = x - 1
        cursor_y = y + 1
        while is_square_inside_board(cursor_x, cursor_y):
            if self.board[cursor_y][cursor_x] == "empty":
                cursor_x -= 1
                cursor_y += 1
            elif self.board[cursor_y][cursor_x] == enemy[2] or self.board[cursor_y][cursor_x] == enemy[3]:
                return True
            else:
                cursor_x = -1
        # this checks for bishops and queens in the direction of the third quadrant
        cursor_x = x - 1
        cursor_y = y - 1
        while is_square_inside_board(cursor_x, cursor_y):
            if self.board[cursor_y][cursor_x] == "empty":
                cursor_x -= 1
                cursor_y -= 1
            elif self.board[cursor_y][cursor_x] == enemy[2] or self.board[cursor_y][cursor_x] == enemy[3]:
                return True
            else:
                cursor_x = -1
        # this checks for bishops and queen in the direction of the fourth quadrant
        cursor_x = x + 1
        cursor_y = y - 1
        while is_square_inside_board(cursor_x, cursor_y):
            if self.board[cursor_y][cursor_x] == "empty":
                cursor_x += 1
                cursor_y -= 1
            elif self.board[cursor_y][cursor_x] == enemy[2] or self.board[cursor_y][cursor_x] == enemy[3]:
                return True
            else:
                cursor_x = -1
        # knight attack checks
        if is_square_inside_board(x + 1, y + 2) and self.board[y + 2][x + 1] == enemy[1]:
            return True
        elif is_square_inside_board(x + 2, y + 1) and self.board[y + 1][x + 2] == enemy[1]:
            return True
        elif is_square_inside_board(x - 1, y + 2) and self.board[y + 2][x - 1] == enemy[1]:
            return True
        elif is_square_inside_board(x - 2, y + 1) and self.board[y + 1][x - 2] == enemy[1]:
            return True
        elif is_square_inside_board(x - 2, y - 1) and self.board[y - 1][x - 2] == enemy[1]:
            return True
        elif is_square_inside_board(x - 1, y - 2) and self.board[y - 2][x - 1] == enemy[1]:
            return True
        elif is_square_inside_board(x + 1, y - 2) and self.board[y - 2][x + 1] == enemy[1]:
            return True
        elif is_square_inside_board(x + 2, y - 1) and self.board[y - 1][x + 2] == enemy[1]:
            return True
        # king attack checks
        if is_square_inside_board(x + 1, y + 1) and self.board[y + 1][x + 1] == enemy[4]:
            return True
        elif is_square_inside_board(x + 1, y) and self.board[y][x + 1] == enemy[4]:
            return True
        elif is_square_inside_board(x + 1, y - 1) and self.board[y - 1][x + 1] == enemy[4]:
            return True
        elif is_square_inside_board(x, y + 1) and self.board[y + 1][x] == enemy[4]:
            return True
        elif is_square_inside_board(x, y - 1) and self.board[y - 1][x] == enemy[4]:
            return True
        elif is_square_inside_board(x - 1, y + 1) and self.board[y + 1][x - 1] == enemy[4]:
            return True
        elif is_square_inside_board(x - 1, y) and self.board[y][x - 1] == enemy[4]:
            return True
        elif is_square_inside_board(x - 1, y - 1) and self.board[y - 1][x - 1] == enemy[4]:
            return True
        # if it hasn't returned by now, the square is not under attack
        return False

    def print_board(self, moves=None):

        temp_board = self.board
        for i in range(8):
            for j in range(8):
                if temp_board[i][j] == "p":
                    temp_board[i][j] = "♙"
                elif temp_board[i][j] == "P":
                    temp_board[i][j] = "♟"
                elif temp_board[i][j] == "r":
                    temp_board[i][j] = "♖"
                elif temp_board[i][j] == "R":
                    temp_board[i][j] = "♜"
                elif temp_board[i][j] == "n":
                    temp_board[i][j] = "♘"
                elif temp_board[i][j] == "N":
                    temp_board[i][j] = "♞"
                elif temp_board[i][j] == "b":
                    temp_board[i][j] = "♗"
                elif temp_board[i][j] == "B":
                    temp_board[i][j] = "♝"
                elif temp_board[i][j] == "q":
                    temp_board[i][j] = "♕"
                elif temp_board[i][j] == "Q":
                    temp_board[i][j] = "♛"
                elif temp_board[i][j] == "k":
                    temp_board[i][j] = "♔"
                elif temp_board[i][j] == "K":
                    temp_board[i][j] = "♚"
                else:
                    temp_board[i][j] = "☐"
        if moves is not None:
            for i in moves:
                if temp_board[int(i[1])][int(i[0])] == "☐":
                    temp_board[int(i[1])][int(i[0])] = "☒"
                else:
                    temp_board[int(i[1])][int(i[0])] = "☠"
        temp_board.reverse()
        for i in temp_board:
            line = ""
            for j in i:
                line += j
            print(line)
