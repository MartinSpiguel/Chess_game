

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
        self.wk_position = (7, 4)
        self.bk_position = (0, 4)
        

    '''
    Takes a move and changes the state of the board making the move
    '''
    def make_move(self, move):
        self.board[move.start_row][move.start_col] = '--' #Changes the board state
        self.board[move.end_row][move.end_col] = move.piece_moved #Changes the board state
        self.white_to_move = not self.white_to_move #Changes the turn
        #Pawn promotion
        if move.end_row == 0 and move.piece_moved == 'wp':
            self.board[move.end_row][move.end_col] = 'wq'
        if move.end_row == 7 and move.piece_moved == 'bp':
            self.board[move.end_row][move.end_col] = 'bq'
        #Update kings position
        if move.piece_moved == 'wk':
            self.wk_position = (move.end_row, move.end_col)
            print(self.wk_position)
        if move.piece_moved == 'bk':
            self.bk_position = (move.end_row, move.end_col)
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
    Gets all the legal moves considering checks
    '''
    def get_valid_moves(self):
        #Generate all legal moves
        legal_moves = self.get_legal_moves()
        #For each move make the move
        for i in range(len(legal_moves)-1, -1, -1):
            move = legal_moves[i]
            self.make_move(move)
            #Generate all legal moves for the oponent
            oponents_moves = self.get_legal_moves()
            #See if any of them atack our king
            self.white_to_move = not self.white_to_move
            if self.in_check():
                legal_moves.remove(legal_moves[i]) #Remove move
            self.white_to_move = not self.white_to_move
            self.undo_move(move)
        return legal_moves        

    '''
    Determin if a player is in check
    '''
    def in_check(self):
        if self.white_to_move:
            return self.square_under_attack(self.wk_position[0], self.wk_position[1])
        else:
            return self.square_under_attack(self.bk_position[0], self.bk_position[1])

    '''
    Determin if oponent can atack the square r, c
    '''
    def square_under_attack(self, r, c):
        self.white_to_move = not self.white_to_move
        oponents_move = self.get_legal_moves()
        self.white_to_move = not self.white_to_move
        for move in oponents_move:
            if move.end_row == r and move.end_col == c:
                return True
        return False

    '''
    Gets all the legal moves
    '''
    def get_legal_moves(self):
        legal_moves = []
        for r in range(0, 8):
            for c in range(0, 8):
                color = self.board[r][c][0]
                if (color == 'w' and self.white_to_move) or (color == 'b' and not self.white_to_move):
                    piece = self.board[r][c][1]
                    if piece == 'p':
                        self.get_pawn_moves(r, c, legal_moves)
                    if piece == 'k':
                        self.get_king_moves(r, c, legal_moves)
                    if piece == 'r':
                        self.get_rook_moves(r, c, legal_moves)
                    if piece == 'b':
                        self.get_bishop_moves(r, c, legal_moves)
                    if piece == 'q':
                        self.get_queen_moves(r, c, legal_moves)
                    if piece == 'n':
                        self.get_knight_moves(r, c, legal_moves)
        return legal_moves

    def get_pawn_moves(self, row, col, legal_moves):
        if self.white_to_move:
            if self.board[row-1][col] == '--':
                legal_moves.append(Move((row, col), (row-1, col), self.board))
            if row == 6 and self.board[row-2][col] == '--' and self.board[row-1][col] == '--':
                legal_moves.append(Move((row, col), (row-2, col), self.board))
            try:
                if self.board[row-1][col-1] != '--' and self.board[row-1][col-1][0] != 'w':
                    legal_moves.append(Move((row, col), (row-1, col-1), self.board))
                if self.board[row-1][col+1] != '--' and self.board[row-1][col+1][0] != 'w':
                    legal_moves.append(Move((row, col), (row-1, col+1), self.board))
            except:
                pass
        else:
            if self.board[row+1][col] == '--':
                legal_moves.append(Move((row, col), (row+1, col), self.board))
            if row == 1 and self.board[row+2][col] == '--' and self.board[row+1][col] == '--':
                legal_moves.append(Move((row, col), (row+2, col), self.board))
            try:
                if self.board[row+1][col-1] != '--' and self.board[row+1][col-1][0] != 'b':
                    legal_moves.append(Move((row, col), (row+1, col-1), self.board))
                if self.board[row+1][col+1] != '--' and self.board[row+1][col+1][0] != 'w':
                    legal_moves.append(Move((row, col), (row+1, col+1), self.board))
            except:
                pass

    def get_king_moves(self, row, col, legal_moves):
        king_moves = ((-1, -1), (1, 1), (0, 1), (1, 0), (0, -1), (-1, 0), (1, -1), (-1, 1))
        ally_color = 'w' if self.white_to_move else 'b'
        for i in range(8):
            end_row = row + king_moves[i][0]
            end_col = col + king_moves[i][1]
            if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] != ally_color:
                    legal_moves.append(Move((row, col), (end_row, end_col), self.board))

    def get_rook_moves(self, row, col, legal_moves):
        directions = ((-1, 0), (0, 1), (1, 0), (0, -1))
        ally_color = 'w' if self.white_to_move else 'b'
        for i in range(4):
            for j in range(1, 8):
                end_row = row + directions[i][0] * j
                end_col = col + directions[i][1] * j
                if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                    end_piece = self.board[end_row][end_col]
                    if end_piece == '--':
                        legal_moves.append(Move((row, col), (end_row, end_col), self.board))
                    else:
                        if end_piece[0] == ally_color:
                            break
                        elif end_piece[0] != ally_color:
                            legal_moves.append(Move((row, col), (end_row, end_col), self.board))
                            break
                else: 
                    break

    def get_bishop_moves(self, row, col, legal_moves):
        directions = ((-1, 1), (1, 1), (1, -1), (-1, -1))
        ally_color = 'w' if self.white_to_move else 'b'
        for i in range(4):
            for j in range(1, 8):
                end_row = row + directions[i][0] * j
                end_col = col + directions[i][1] * j
                if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                    end_piece = self.board[end_row][end_col]
                    if end_piece == '--':
                        legal_moves.append(Move((row, col), (end_row, end_col), self.board))
                    else:
                        if end_piece[0] == ally_color:
                            break
                        elif end_piece[0] != ally_color:
                            legal_moves.append(Move((row, col), (end_row, end_col), self.board))
                            break
                else: 
                    break

    def get_queen_moves(self, row, col, legal_moves):
        directions = ((-1, 0), (0, 1), (1, 0), (0, -1), (-1, 1), (1, 1), (1, -1), (-1, -1))
        ally_color = 'w' if self.white_to_move else 'b'
        for i in range(8):
            for j in range(1, 8):
                end_row = row + directions[i][0] * j
                end_col = col + directions[i][1] * j
                if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                    end_piece = self.board[end_row][end_col]
                    if end_piece == '--':
                        legal_moves.append(Move((row, col), (end_row, end_col), self.board))
                    else:
                        if end_piece[0] == ally_color:
                            break
                        elif end_piece[0] != ally_color:
                            legal_moves.append(Move((row, col), (end_row, end_col), self.board))
                            break
                else: 
                    break

    def get_knight_moves(self, row, col, legal_moves):
        knight_moves = ((1, 2), (1, -2), (-1, -2), (-1, 2), (2, 1), (2, -1), (-2, -1), (-2, 1))
        ally_color = 'w' if self.white_to_move else 'b'
        for i in range(8):
            end_row = row + knight_moves[i][0]
            end_col = col + knight_moves[i][1]
            if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] != ally_color:
                    legal_moves.append(Move((row, col), (end_row, end_col), self.board))
            

    
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
        self.move_id = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col

    '''
    Overwrites equal instances
    '''
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.move_id == other.move_id
        return False

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

    



