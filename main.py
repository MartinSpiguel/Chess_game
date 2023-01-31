#Import modules
import pygame
import chess_engine

#Initialize pygame
pygame.init()

#Define constants
WIDTH = HEIGHT = 600
DIM = 8
SQ_SIZE = WIDTH // DIM
FPS = 60

#Colors
DARK_BROWN = (75,54,33)
BEIGE = (245,245,220)
GREEN = (0,255,0)

#Load imgs
pieces = {
    'wp' : pygame.transform.scale(pygame.image.load('img/wp.png'), (SQ_SIZE, SQ_SIZE)),
    'bp' : pygame.transform.scale(pygame.image.load('img/bp.png'), (SQ_SIZE, SQ_SIZE)),
    'wr' : pygame.transform.scale(pygame.image.load('img/wr.png'), (SQ_SIZE, SQ_SIZE)),
    'br' : pygame.transform.scale(pygame.image.load('img/br.png'), (SQ_SIZE, SQ_SIZE)),
    'wn' : pygame.transform.scale(pygame.image.load('img/wn.png'), (SQ_SIZE, SQ_SIZE)),
    'bn' : pygame.transform.scale(pygame.image.load('img/bn.png'), (SQ_SIZE, SQ_SIZE)),
    'wb' : pygame.transform.scale(pygame.image.load('img/wb.png'), (SQ_SIZE, SQ_SIZE)),
    'bb' : pygame.transform.scale(pygame.image.load('img/bb.png'), (SQ_SIZE, SQ_SIZE)),
    'wk' : pygame.transform.scale(pygame.image.load('img/wk.png'), (SQ_SIZE, SQ_SIZE)),
    'bk' : pygame.transform.scale(pygame.image.load('img/bk.png'), (SQ_SIZE, SQ_SIZE)),
    'wq' : pygame.transform.scale(pygame.image.load('img/wq.png'), (SQ_SIZE, SQ_SIZE)),
    'bq' : pygame.transform.scale(pygame.image.load('img/bq.png'), (SQ_SIZE, SQ_SIZE))
}

#Draw the window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Chess')

def draw_board(screen):
    for f in range(0,DIM):
        for c in range(0,DIM):
            cell_num = (f+c)%2
            if cell_num == 0:
                pygame.draw.rect(screen, BEIGE, (SQ_SIZE*f, SQ_SIZE*c, SQ_SIZE, SQ_SIZE))
            else:
                pygame.draw.rect(screen, DARK_BROWN, (SQ_SIZE*f, SQ_SIZE*c, SQ_SIZE, SQ_SIZE))

def draw_pieces(board):
    for r in range(0,8):
        for s in range(0,8):
            if board[r][s] == 'wp':
                screen.blit(pieces['wp'], (SQ_SIZE*s, SQ_SIZE*r))
            elif board[r][s] == 'bp':
                screen.blit(pieces['bp'], (SQ_SIZE*s, SQ_SIZE*r))
            elif board[r][s] == 'wk':
                screen.blit(pieces['wk'], (SQ_SIZE*s, SQ_SIZE*r))
            elif board[r][s] == 'bk':
                screen.blit(pieces['bk'], (SQ_SIZE*s, SQ_SIZE*r))
            elif board[r][s] == 'br':
               screen.blit(pieces['br'], (SQ_SIZE*s, SQ_SIZE*r))
            elif board[r][s] == 'wr':
               screen.blit(pieces['wr'], (SQ_SIZE*s, SQ_SIZE*r))
            elif board[r][s] == 'bn':
                screen.blit(pieces['bn'], (SQ_SIZE*s, SQ_SIZE*r))
            elif board[r][s] == 'wn':
                screen.blit(pieces['wn'], (SQ_SIZE*s, SQ_SIZE*r))
            elif board[r][s] == 'bb':
                screen.blit(pieces['bb'], (SQ_SIZE*s, SQ_SIZE*r))
            elif board[r][s] == 'wb':
                screen.blit(pieces['wb'], (SQ_SIZE*s, SQ_SIZE*r))
            elif board[r][s] == 'bq':
                screen.blit(pieces['bq'], (SQ_SIZE*s, SQ_SIZE*r))
            elif board[r][s] == 'wq':
                screen.blit(pieces['wq'], (SQ_SIZE*s, SQ_SIZE*r))


def main():
    run = True
    clock = pygame.time.Clock()
    #Define board object
    board = chess_engine.Board()
    counter = 0
    game = []
    legal_moves = board.get_valid_moves()
    move_made = False
    legal_moves_marker = False
    while run:
        clock.tick(FPS) #Handle fps
        #Braks the loop if the user presses the exit button
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            #Draws the moves
            if event.type == pygame.MOUSEBUTTONDOWN:
                loc = pygame.mouse.get_pos()
                row = loc[1]//SQ_SIZE
                col = loc[0]//SQ_SIZE
                if counter % 2 == 0:
                    start_square = (row, col)
                    legal_moves_marker = True
                    print(legal_moves, legal_moves_marker)
                else:
                    end_square = (row, col)
                    move = chess_engine.Move(start_square, end_square, board.board)
                    legal_moves_marker = False
                    if move in legal_moves:
                        board.make_move(move)
                        move_made = True
                        game.append(move.get_chess_notation(move.end_row, move.end_col))
                        print(board.white_to_move, game)
                        
                    #board.make_move(move)
                    #game.append(move.get_chess_notation(move.end_row, move.end_col))
                    #print(board.white_to_move, game)
                counter += 1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_u:
                    board.undo_move(board.moves[-1])
                    move_made = True
                    game.pop()
                    print(board.white_to_move, game)

        if move_made:
            legal_moves = board.get_valid_moves()
            move_made = False

        draw_board(screen)
        draw_pieces(board.board)
        if legal_moves_marker:
            for move in legal_moves:
                if (move.start_row, move.start_col) == (row, col):
                    coor = (move.end_row*SQ_SIZE, move.end_col*SQ_SIZE)
                    surf = pygame.Surface((SQ_SIZE, SQ_SIZE))
                    surf.set_alpha(80)
                    pygame.draw.rect(surf, GREEN, pygame.Rect((0, 0), (SQ_SIZE, SQ_SIZE)))
                    screen.blit(surf, (coor[1], coor[0]))
                
        pygame.display.update()


#Run main function
if __name__ == '__main__':
    main()




