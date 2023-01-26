

#Define clases
class Board:
    '''
    Initial state of the board
    '''
    def __init__(self):
        self.board = [
            ['br', 'bn', 'bb', 'bq', 'bk', 'bb', 'bn', 'br'],
            ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
            ['wr', 'wn', 'wb', 'wq', 'wk', 'wb', 'wn', 'wr'],
        ]
        self.white_to_move = True
        self.moves = []
        self.in_check = False
        #For check we can check if in the next move one player can capture the other players king (if the square with the king is in the legal moves list)

    '''
    Takes a move and changes the state of the board making the move
    '''
    def make_move(self, move):
        self.board[move.start_row][move.start_col] = '--' #Changes the board state
        self.board[move.end_row][move.end_col] = move.piece_moved #Changes the board state
        self.white_to_move = not self.white_to_move #Changes the turn
        if move.end_row == 0 and move.piece_moved == 'wp':
            self.board[move.end_row][move.end_col] = 'wq'
        if move.end_row == 7 and move.piece_moved == 'bp':
            self.board[move.end_row][move.end_col] = 'bq'
        self.moves.append(move)
        
    '''
    Undo the last move
    '''
    def undo_move(self, move):
        self.board[move.start_row][move.start_col] = move.piece_moved #Changes the board state
        self.board[move.end_row][move.end_col] = move.piece_captured #Changes the board state
        self.white_to_move = not self.white_to_move #Changes the turn
        self.moves.pop()

    '''
    Gets all the legal moves
    '''
    def get_legal_moves(self, row, col):
        legal_moves = []
        piece = self.board[row][col]
        color = piece[0]
        if color == 'w' and not self.white_to_move:
            return legal_moves
        if color == 'b' and self.white_to_move:
            return legal_moves

        if piece == 'wp':
            if self.board[row-1][col] == '--':
                legal_moves.append((row-1, col))
            if row == 6 and self.board[row-2][col] == '--':
                legal_moves.append((row-2, col))
            try:
                if self.board[row-1][col-1] != '--':
                    legal_moves.append((row-1, col-1))
                if self.board[row-1][col+1] != '--':
                    legal_moves.append((row-1, col+1))
            except:
                pass
            
        if piece == 'bp':
            if self.board[row+1][col] == '--':
                legal_moves.append((row+1, col))
            if row == 1 and self.board[row+2][col] == '--':
                legal_moves.append((row+2, col))
            try:
                if self.board[row+1][col-1] != '--':
                    legal_moves.append((row+1, col-1))
                if self.board[row+1][col+1] != '--':
                    legal_moves.append((row+1, col+1))
            except:
                pass

        if 'k' in piece:
            king_moves = ((-1, -1), (1, 1), (0, 1), (1, 0), (0, -1), (-1, 0), (1, -1), (-1, 1))
            ally_color = 'w' if self.white_to_move else 'b'
            for i in range(8):
                end_row = row + king_moves[i][0]
                end_col = col + king_moves[i][1]
                if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                    end_piece = self.board[end_row][end_col]
                    if end_piece[0] != ally_color:
                        legal_moves.append((end_row, end_col))

        if 'r' in piece:
            directions = ((-1, 0), (0, 1), (1, 0), (0, -1))
            ally_color = 'w' if self.white_to_move else 'b'
            for i in range(4):
                for j in range(1, 8):
                    end_row = row + directions[i][0] * j
                    end_col = col + directions[i][1] * j
                    if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                        end_piece = self.board[end_row][end_col]
                        if end_piece == '--':
                            legal_moves.append((end_row, end_col))
                        else:
                            if end_piece[0] == ally_color:
                                break
                            elif end_piece[0] != ally_color:
                                legal_moves.append((end_row, end_col))
                                break
                    else: 
                        break

        if piece[1] == 'b':
            directions = ((-1, 1), (1, 1), (1, -1), (-1, -1))
            ally_color = 'w' if self.white_to_move else 'b'
            for i in range(4):
                for j in range(1, 8):
                    end_row = row + directions[i][0] * j
                    end_col = col + directions[i][1] * j
                    if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                        end_piece = self.board[end_row][end_col]
                        if end_piece == '--':
                            legal_moves.append((end_row, end_col))
                        else:
                            if end_piece[0] == ally_color:
                                break
                            elif end_piece[0] != ally_color:
                                legal_moves.append((end_row, end_col))
                                break
                    else: 
                        break

        if 'q' in piece:
            directions = ((-1, 0), (0, 1), (1, 0), (0, -1), (-1, 1), (1, 1), (1, -1), (-1, -1))
            ally_color = 'w' if self.white_to_move else 'b'
            for i in range(8):
                for j in range(1, 8):
                    end_row = row + directions[i][0] * j
                    end_col = col + directions[i][1] * j
                    if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                        end_piece = self.board[end_row][end_col]
                        if end_piece == '--':
                            legal_moves.append((end_row, end_col))
                        else:
                            if end_piece[0] == ally_color:
                                break
                            elif end_piece[0] != ally_color:
                                legal_moves.append((end_row, end_col))
                                break
                    else: 
                        break

        if 'n' in piece:
            knight_moves = ((1, 2), (1, -2), (-1, -2), (-1, 2), (2, 1), (2, -1), (-2, -1), (-2, 1))
            ally_color = 'w' if self.white_to_move else 'b'
            for i in range(8):
                end_row = row + knight_moves[i][0]
                end_col = col + knight_moves[i][1]
                if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                    end_piece = self.board[end_row][end_col]
                    if end_piece[0] != ally_color:
                        legal_moves.append((end_row, end_col))
            
        return legal_moves

    
class Move():
    ranks_to_rows = {'1':7, '2':6, '3':5, '4':4,
                    '5':3, '6':2, '7':1, '8':0}
    rows_to_ranks = {v:k for k,v in ranks_to_rows.items()}

    files_to_cols = {'a':0, 'b':1, 'c':2, 'd':3,
                    'e':4, 'f':5, 'g':6, 'h':7}
    cols_to_files = {v:k for k,v in files_to_cols.items()}

    '''
    Initial state of a move
    '''
    def __init__(self, start_square, end_square, board):
        self.start_row = start_square[0]
        self.start_col = start_square[1]
        self.end_row = end_square[0]
        self.end_col = end_square[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]

    '''
    Gets the actual chess notation
    '''
    def get_chess_notation(self, row, col):
        line = self.cols_to_files[col]
        rank = self.rows_to_ranks[row]
        if self.piece_captured != '--':
            return self.piece_moved + 'x' + line + rank
        else:
            return self.piece_moved + line + rank

    



