def main():
    test = Board("rnbqkbnr/p7/1P6/8/8/8/8/8 w KQkq -")
    print(test.board)
    print(pseudo_legal_generator(test, 0, 1))


# def generator(fen_board, x, y):
#
#
def pseudo_legal_generator(board, x, y):
    board = board
    piece = board.get_piece_in_square(x, y)
    answer = []
    enemy = "rnbqkp"
    if board.player_to_move == "w":
        enemy = enemy.upper()
    if piece == "p":
        if is_square_inside_board(x, y+1) and board.board[y+1][x] == "empty":
            if y == 1:
                if board.board[y+2][x] == "empty":
                    answer.append(str(x) + str(y+1))
                    answer.append(str(x) + str(y+2))
                else:
                    answer.append(str(x) + str(y+1))
            else:
                answer.append(str(x) + str(y+1))
        if is_square_inside_board(x-1, y+1) and board.board[y+1][x-1] in enemy:
            answer.append(str(x-1) + str(y+1))
        if is_square_inside_board(x+1, y+1) and board.board[y+1][x+1] in enemy:
            answer.append(str(x+1) + str(y+1))
    return answer

# def piece_moves(board, x, y): # why
#     answer = []


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
        info_list[3] = ord(info_list[3][0]) - a_char_ord_constant + info_list[3][1]
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

    # def is_piece_in_square(self, x, y): #remove LBYL?
    #
    def get_piece_in_square(self, x, y):
        return self.board[y][x]

    def square_is_under_attack(self, x, y):
        enemy = "rnbqkp"
        if self.player_to_move == "w":
            enemy = enemy.upper()
            # checks for existing en passants and black pawn attacks
            if str(x) + str(y-1) == self.en_passant_target:
                if is_square_inside_board(x+1, y) and self.board[y][x+1] == enemy[5]:
                    return True
                if is_square_inside_board(x-1, y) and self.board[y][x-1] == enemy[5]:
                    return True
            # this checks for generic black pawn attacks
            else:
                if is_square_inside_board(x+1, y+1) and self.board[y+1][x + 1] == enemy[5]:
                    return True
                if is_square_inside_board(x-1, y+1) and self.board[y+1][x - 1] == enemy[5]:
                    return True
        else:
            # checks for existing en passants and white pawn attacks
            if str(x) + str(y+1) == self.en_passant_target:
                if is_square_inside_board(x+1, y) and self.board[y][x+1] == enemy[5]:
                    return True
                if is_square_inside_board(x-1, y) and self.board[y][x-1] == enemy[5]:
                    return True
            # checks for generic white pawn attacks
            else:
                if is_square_inside_board(x+1, y-1) and self.board[y-1][x + 1] == enemy[5]:
                    return True
                if is_square_inside_board(x-1, y-1) and self.board[y-1][x - 1] == enemy[5]:
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
        cursor_x = x+1
        cursor_y = y+1
        while is_square_inside_board(cursor_x, cursor_y):
            if self.board[cursor_y][cursor_x] == "empty":
                cursor_x += 1
                cursor_y += 1
            elif self.board[cursor_y][cursor_x] == enemy[2] or self.board[cursor_y][cursor_x] == enemy[3]:
                return True
            else:
                cursor_x = -1
        # this checks for bishops and queens in the direction of the second quadrant
        cursor_x = x-1
        cursor_y = y+1
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
        if is_square_inside_board(x+1, y+2) and self.board[y+2][x+1] == enemy[1]:
            return True
        elif is_square_inside_board(x+2, y+1) and self.board[y+1][x+2] == enemy[1]:
            return True
        elif is_square_inside_board(x-1, y+2) and self.board[y+2][x-1] == enemy[1]:
            return True
        elif is_square_inside_board(x-2, y+1) and self.board[y+1][x-2] == enemy[1]:
            return True
        elif is_square_inside_board(x-2, y-1) and self.board[y-1][x-2] == enemy[1]:
            return True
        elif is_square_inside_board(x-1, y-2) and self.board[y-2][x-1] == enemy[1]:
            return True
        elif is_square_inside_board(x+1, y-2) and self.board[y-2][x+1] == enemy[1]:
            return True
        elif is_square_inside_board(x+2, y-1) and self.board[y-1][x+2] == enemy[1]:
            return True
        # king attack checks
        if is_square_inside_board(x+1, y+1) and self.board[y+1][x+1] == enemy[4]:
            return True
        elif is_square_inside_board(x+1, y) and self.board[y][x+1] == enemy[4]:
            return True
        elif is_square_inside_board(x+1, y-1) and self.board[y-1][x+1] == enemy[4]:
            return True
        elif is_square_inside_board(x, y+1) and self.board[y+1][x] == enemy[4]:
            return True
        elif is_square_inside_board(x, y-1) and self.board[y-1][x] == enemy[4]:
            return True
        elif is_square_inside_board(x-1, y+1) and self.board[y+1][x-1] == enemy[4]:
            return True
        elif is_square_inside_board(x-1, y) and self.board[y][x-1] == enemy[4]:
            return True
        elif is_square_inside_board(x-1, y-1) and self.board[y-1][x-1] == enemy[4]:
            return True
        # if it hasn't returned by now, the square is not under attack
        return False

if __name__ == '__main__':
    main()
