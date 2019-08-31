def main():


def generator(fen_board, x, y):


def pseudo_legal_generator(board, x, y):


def square_is_under_attack(x, y):


def piece_moves(piece):


def is_square_inside_board(x, y): #remove LBYL?
    answer = 0 <= x < 8 and 0 <= y < 8
    return answer

def fen_to_board(fen):
    answer = []

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

    def is_piece_in_square(self, x, y): #remove LBYL?

    def get_piece_in_square(self, x, y):

if __name__ == '__main__':
    main()