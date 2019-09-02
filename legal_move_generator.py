def main():
    print(fen_to_board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq -"))


# def generator(fen_board, x, y):
#
#
# def pseudo_legal_generator(board, x, y):
#
#
# def square_is_under_attack(x, y):
#
#
# def piece_moves(piece):


def is_square_inside_board(x, y):  # remove LBYL?
    answer = 0 <= x < 8 and 0 <= y < 8
    return answer


def fen_to_board(fen):
    answer = []
    info_list = fen.split(" ")
    board_state = info_list[0].split("/")
    final_board = [[] for i in range(8)]
    for i in range(len(board_state)):
        for j in range(len(board_state[i])):
            if board_state[i][j].isnumeric():
                for k in range(int(board_state[i][j])):
                    final_board[i].append("empty")
            else:
                final_board[i].append(board_state[i][j])
    answer.append(final_board)
    answer.append(info_list[1])
    answer.append(info_list[2])
    if len(info_list[3]) > 1:  # converts notation to list index using magic numbers
        info_list[3] = ord(info_list[3][0]) - 96 + info_list[3][1]
    answer.append(info_list[3])
    return answer


class Board:
    board = []
    player_to_move = ""
    castling_rights = []
    en_passant_target = []

    def __init__(self, fen):
        info = fen_to_board(fen)
        board = info[0]
        player_to_move = info[1]
        castling_rights = info[2]
        en_passant_target = info[3]

    # def is_piece_in_square(self, x, y): #remove LBYL?
    #
    # def get_piece_in_square(self, x, y):


if __name__ == '__main__':
    main()
