from Board import Board, is_square_inside_board


def main():
    teste = Board("rnbqkbnr/pppppppp/3P4/8/8/8/PPPPPPPP/RNBQKBNR w KQkq -")
    moves = generator("rnbqkbnr/pppppppp/3P4/8/8/8/PPPPPPPP/RNBQKBNR w KQkq -", 4, 1)
    teste.print_board(moves)


def generator(fen_board, x, y):
    answer = []
    board = Board(fen_board)
    pseudo_legal_moves = pseudo_legal_generator(board, x, y)
    for i in pseudo_legal_moves:
        temp_board = Board(fen_board)
        piece = temp_board.board_read(x, y)
        temp_board.board_write(x, y, "empty")
        temp_board.board_write(int(i[0]), int(i[1]), piece)
        king = temp_board.get_king_square()
        if not temp_board.square_is_under_attack(int(king[0]), int(king[1])):
            answer.append(i)
    if board.board_read(x, y) == "k":
        if "k" in board.castling_rights:
            if board.board_read(5, 0) == "empty" and board.board_read(6, 0) == "empty":
                if (not board.square_is_under_attack(4, 0)) and (not board.square_is_under_attack(5, 0)) and (
                        not board.square_is_under_attack(6, 0)):
                    answer.append("60")
        if "q" in board.castling_rights:
            if board.board_read(1, 0) == "empty" and board.board_read(2, 0) == "empty" and board.board_read(3,
                                                                                                            0) == "empty":
                if (not board.square_is_under_attack(4, 0)) and (not board.square_is_under_attack(3, 0)) and (
                        not board.square_is_under_attack(2, 0)):
                    answer.append("20")
    return answer


def pseudo_legal_generator(board, x, y):
    board = board
    piece = board.board_read(x, y)
    answer = []
    enemy = "rnbqkp"
    if board.player_to_move == "w":
        enemy = enemy.upper()
    if piece == "p":
        # this checks normal pawn movement and 2-square advances
        if is_square_inside_board(x, y + 1) and board.board_read(x, y + 1) == "empty":
            if y == 1:
                if board.board_read(x, y + 2) == "empty":
                    answer.append(str(x) + str(y + 1))
                    answer.append(str(x) + str(y + 2))
                else:
                    answer.append(str(x) + str(y + 1))
            else:
                answer.append(str(x) + str(y + 1))
        # this checks both normal pawn capture and en passant
        if is_square_inside_board(x - 1, y + 1) and (
                board.board_read(x - 1, y + 1) in enemy or str(x - 1) + str(y + 1) == board.en_passant_target):
            answer.append(str(x - 1) + str(y + 1))
        if is_square_inside_board(x + 1, y + 1) and (
                board.board_read(x + 1, y + 1) in enemy or str(x + 1) + str(y + 1) == board.en_passant_target):
            answer.append(str(x + 1) + str(y + 1))
    elif piece == "P":
        # this checks normal pawn movement and 2-square advances
        if is_square_inside_board(x, y - 1) and board.board_read(x, y - 1) == "empty":
            if y == 6:
                if board.board_read(x, y - 2) == "empty":
                    answer.append(str(x) + str(y - 1))
                    answer.append(str(x) + str(y - 2))
                else:
                    answer.append(str(x) + str(y - 1))
            else:
                answer.append(str(x) + str(y - 1))
        # this checks both normal pawn capture and en passant
        if is_square_inside_board(x - 1, y - 1) and (
                board.board_read(x - 1, y - 1) in enemy or str(x - 1) + str(y - 1) == board.en_passant_target):
            answer.append(str(x - 1) + str(y - 1))
        if is_square_inside_board(x + 1, y - 1) and (
                board.board_read(x + 1, y - 1) in enemy or str(x + 1) + str(y - 1) == board.en_passant_target):
            answer.append(str(x + 1) + str(y - 1))
    elif piece.lower() == "r":
        # this checks for rook movement and capture to the left
        cursor = x - 1
        while is_square_inside_board(cursor, y):
            if board.board_read(cursor, y) == "empty":
                answer.append(str(cursor) + str(y))
                cursor -= 1
            elif board.board_read(cursor, y) in enemy:
                answer.append(str(cursor) + str(y))
                cursor = -1
            else:
                cursor = -1
        # this checks for rook movement and capture to the right
        cursor = x + 1
        while is_square_inside_board(cursor, y):
            if board.board_read(cursor, y) == "empty":
                answer.append(str(cursor) + str(y))
                cursor += 1
            elif board.board_read(cursor, y) in enemy:
                answer.append(str(cursor) + str(y))
                cursor = -1
            else:
                cursor = -1
        # this checks for rook movement and capture upwards
        cursor = y + 1
        while is_square_inside_board(x, cursor):
            if board.board_read(x, cursor) == "empty":
                answer.append(str(x) + str(cursor))
                cursor += 1
            elif board.board_read(x, cursor) in enemy:
                answer.append(str(x) + str(cursor))
                cursor = -1
            else:
                cursor = -1
        # this checks for rook movement and capture downwards
        cursor = y - 1
        while is_square_inside_board(x, cursor):
            if board.board_read(x, cursor) == "empty":
                answer.append(str(x) + str(cursor))
                cursor -= 1
            elif board.board_read(x, cursor) in enemy:
                answer.append(str(x) + str(cursor))
                cursor = -1
            else:
                cursor = -1
    elif piece.lower() == "b":
        # this checks for bishop movement in the direction of the first quadrant
        cursor_x = x + 1
        cursor_y = y + 1
        while is_square_inside_board(cursor_x, cursor_y):
            if board.board_read(cursor_x, cursor_y) == "empty":
                answer.append(str(cursor_x) + str(cursor_y))
                cursor_x += 1
                cursor_y += 1
            elif board.board_read(cursor_x, cursor_y) in enemy:
                answer.append(str(cursor_x) + str(cursor_y))
                cursor_x = -1
            else:
                cursor_x = -1
        # this checks for bishop movement in the direction of the second quadrant
        cursor_x = x - 1
        cursor_y = y + 1
        while is_square_inside_board(cursor_x, cursor_y):
            if board.board_read(cursor_x, cursor_y) == "empty":
                answer.append(str(cursor_x) + str(cursor_y))
                cursor_x -= 1
                cursor_y += 1
            elif board.board_read(cursor_x, cursor_y) in enemy:
                answer.append(str(cursor_x) + str(cursor_y))
                cursor_x = -1
            else:
                cursor_x = -1
        # this checks for bishop movement in the direction of the third quadrant
        cursor_x = x - 1
        cursor_y = y - 1
        while is_square_inside_board(cursor_x, cursor_y):
            if board.board_read(cursor_x, cursor_y) == "empty":
                answer.append(str(cursor_x) + str(cursor_y))
                cursor_x -= 1
                cursor_y -= 1
            elif board.board_read(cursor_x, cursor_y) in enemy:
                answer.append(str(cursor_x) + str(cursor_y))
                cursor_x = -1
            else:
                cursor_x = -1
        # this checks for bishop movement in the direction of the fourth quadrant
        cursor_x = x + 1
        cursor_y = y - 1
        while is_square_inside_board(cursor_x, cursor_y):
            if board.board_read(cursor_x, cursor_y) == "empty":
                answer.append(str(cursor_x) + str(cursor_y))
                cursor_x += 1
                cursor_y -= 1
            elif board.board_read(cursor_x, cursor_y) in enemy:
                answer.append(str(cursor_x) + str(cursor_y))
                cursor_x = -1
            else:
                cursor_x = -1
    elif piece.lower() == "q":
        # this checks for queen movement and capture to the left
        cursor = x - 1
        while is_square_inside_board(cursor, y):
            if board.board_read(cursor, y) == "empty":
                answer.append(str(cursor) + str(y))
                cursor -= 1
            elif board.board_read(cursor, y) in enemy:
                answer.append(str(cursor) + str(y))
                cursor = -1
            else:
                cursor = -1
        # this checks for queen movement and capture to the right
        cursor = x + 1
        while is_square_inside_board(cursor, y):
            if board.board_read(cursor, y) == "empty":
                answer.append(str(cursor) + str(y))
                cursor += 1
            elif board.board_read(cursor, y) in enemy:
                answer.append(str(cursor) + str(y))
                cursor = -1
            else:
                cursor = -1
        # this checks for queen movement and capture upwards
        cursor = y + 1
        while is_square_inside_board(x, cursor):
            if board.board_read(x, cursor) == "empty":
                answer.append(str(x) + str(cursor))
                cursor += 1
            elif board.board_read(x, cursor) in enemy:
                answer.append(str(x) + str(cursor))
                cursor = -1
            else:
                cursor = -1
        # this checks for queen movement and capture downwards
        cursor = y - 1
        while is_square_inside_board(x, cursor):
            if board.board_read(x, cursor) == "empty":
                answer.append(str(x) + str(cursor))
                cursor -= 1
            elif board.board_read(x, cursor) in enemy:
                answer.append(str(x) + str(cursor))
                cursor = -1
            else:
                cursor = -1
        # this checks for queen movement in the direction of the first quadrant
        cursor_x = x + 1
        cursor_y = y + 1
        while is_square_inside_board(cursor_x, cursor_y):
            if board.board_read(cursor_x, cursor_y) == "empty":
                answer.append(str(cursor_x) + str(cursor_y))
                cursor_x += 1
                cursor_y += 1
            elif board.board_read(cursor_x, cursor_y) in enemy:
                answer.append(str(cursor_x) + str(cursor_y))
                cursor_x = -1
            else:
                cursor_x = -1
        # this checks for queen movement in the direction of the second quadrant
        cursor_x = x - 1
        cursor_y = y + 1
        while is_square_inside_board(cursor_x, cursor_y):
            if board.board_read(cursor_x, cursor_y) == "empty":
                answer.append(str(cursor_x) + str(cursor_y))
                cursor_x -= 1
                cursor_y += 1
            elif board.board_read(cursor_x, cursor_y) in enemy:
                answer.append(str(cursor_x) + str(cursor_y))
                cursor_x = -1
            else:
                cursor_x = -1
        # this checks for queen movement in the direction of the third quadrant
        cursor_x = x - 1
        cursor_y = y - 1
        while is_square_inside_board(cursor_x, cursor_y):
            if board.board_read(cursor_x, cursor_y) == "empty":
                answer.append(str(cursor_x) + str(cursor_y))
                cursor_x -= 1
                cursor_y -= 1
            elif board.board_read(cursor_x, cursor_y) in enemy:
                answer.append(str(cursor_x) + str(cursor_y))
                cursor_x = -1
            else:
                cursor_x = -1
        # this checks for queen movement in the direction of the fourth quadrant
        cursor_x = x + 1
        cursor_y = y - 1
        while is_square_inside_board(cursor_x, cursor_y):
            if board.board_read(cursor_x, cursor_y) == "empty":
                answer.append(str(cursor_x) + str(cursor_y))
                cursor_x += 1
                cursor_y -= 1
            elif board.board_read(cursor_x, cursor_y) in enemy:
                answer.append(str(cursor_x) + str(cursor_y))
                cursor_x = -1
            else:
                cursor_x = -1
    elif piece.lower() == "n":
        if is_square_inside_board(x + 1, y + 2) and (
                board.board_read(x + 1, y + 2) in enemy or board.board_read(x + 1, y + 2) == "empty"):
            answer.append(str(x + 1) + str(y + 2))
        if is_square_inside_board(x + 2, y + 1) and (
                board.board_read(x + 2, y + 1) in enemy or board.board_read(x + 2, y + 1) == "empty"):
            answer.append(str(x + 2) + str(y + 1))
        if is_square_inside_board(x - 1, y + 2) and (
                board.board_read(x - 1, y + 2) in enemy or board.board_read(x - 1, y + 2) == "empty"):
            answer.append(str(x - 1) + str(y + 2))
        if is_square_inside_board(x - 2, y + 1) and (
                board.board_read(x - 2, y + 1) in enemy or board.board_read(x - 2, y + 1) == "empty"):
            answer.append(str(x - 2) + str(y + 1))
        if is_square_inside_board(x - 2, y - 1) and (
                board.board_read(x - 2, y - 1) in enemy or board.board_read(x - 2, y - 1) == "empty"):
            answer.append(str(x - 2) + str(y - 1))
        if is_square_inside_board(x - 1, y - 2) and (
                board.board_read(x - 1, y - 2) in enemy or board.board_read(x - 1, y - 2) == "empty"):
            answer.append(str(x - 1) + str(y - 2))
        if is_square_inside_board(x + 1, y - 2) and (
                board.board_read(x + 1, y - 2) in enemy or board.board_read(x + 1, y - 2) == "empty"):
            answer.append(str(x + 1) + str(y - 2))
        if is_square_inside_board(x + 2, y - 1) and (
                board.board_read(x + 2, y - 1) in enemy or board.board_read(x + 2, y - 1) == "empty"):
            answer.append(str(x + 2) + str(y - 1))
    elif piece.lower() == "k":
        if is_square_inside_board(x, y + 1) and (
                board.board_read(x, y + 1) in enemy or board.board_read(x, y + 1) == "empty"):
            answer.append(str(x) + str(y + 1))
        if is_square_inside_board(x + 1, y + 1) and (
                board.board_read(x + 1, y + 1) in enemy or board.board_read(x + 1, y + 1) == "empty"):
            answer.append(str(x + 1) + str(y + 1))
        if is_square_inside_board(x + 1, y) and (
                board.board_read(x + 1, y) in enemy or board.board_read(x + 1, y) == "empty"):
            answer.append(str(x + 1) + str(y))
        if is_square_inside_board(x + 1, y - 1) and (
                board.board_read(x + 1, y - 1) in enemy or board.board_read(x + 1, y - 1) == "empty"):
            answer.append(str(x + 1) + str(y - 1))
        if is_square_inside_board(x, y - 1) and (
                board.board_read(x, y - 1) in enemy or board.board_read(x, y - 1) == "empty"):
            answer.append(str(x) + str(y - 1))
        if is_square_inside_board(x - 1, y - 1) and (
                board.board_read(x - 1, y - 1) in enemy or board.board_read(x - 1, y - 1) == "empty"):
            answer.append(str(x - 1) + str(y - 1))
        if is_square_inside_board(x - 1, y) and (
                board.board_read(x - 1, y) in enemy or board.board_read(x - 1, y) == "empty"):
            answer.append(str(x - 1) + str(y))
        if is_square_inside_board(x - 1, y + 1) and (
                board.board_read(x - 1, y + 1) in enemy or board.board_read(x - 1, y + 1) == "empty"):
            answer.append(str(x - 1) + str(y + 1))
    return answer


if __name__ == '__main__':
    main()
