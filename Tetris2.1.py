import pygame
import sys
import random
import time
from pygame.locals import *

#global variables
FPS = 25
display_width = 640
display_height = 480
box_size = 20
play_width = 10
play_height = 20
blank = '.'

Xmargin = int((display_width - play_width * box_size) / 2)
Ymargin = display_height - (play_height * box_size) - 5
template_width = 5
template_height = 5

# Colours

WHITE       = (255, 255, 255)
GREY        = (185, 185, 185)
BLACK       = (  0,   0,   0)
RED         = (155,   0,   0)
LIGHTRED    = (175,  20,  20)
GREEN       = (  0, 155,   0)
LIGHTGREEN  = ( 20, 175,  20)
CYAN        = (  0, 255, 255)
LIGHTCYAN   = (180, 255, 255)
BLUE        = (  0,   0, 155)
LIGHTBLUE   = ( 20,  20, 175)
ORANGE      = (255, 140,   0)
LIGHTORANGE = (255, 165,   0)
YELLOW      = (155, 155,   0)
LIGHTYELLOW = (175, 175,  20)
PURPLE      = (160,  32, 240)
LIGHTPURPLE = (186,  85, 211)

border_colour = WHITE
BGcolour = BLACK

colours = [CYAN, BLUE, ORANGE, YELLOW, GREEN, PURPLE, RED]
light_colours = [LIGHTCYAN, LIGHTBLUE, LIGHTORANGE,  LIGHTYELLOW, LIGHTGREEN, LIGHTPURPLE, LIGHTRED]
assert len(colours) == len(light_colours)

S_template = [['.....',
               '.....',
               '..OO.',
               '.OO..',
               '.....'],
              ['.....',
               '..O..',
               '..OO.',
               '...O.',
               '.....']]

Z_template = [['.....',
               '.....',
               '.OO..',
               '..OO.',
               '.....'],
              ['.....',
               '..O..',
               '.OO..',
               '.O...',
               '.....']]

I_template = [['..O..',
               '..O..',
               '..O..',
               '..O..',
               '.....'],
              ['.....',
               '.....',
               'OOOO.',
               '.....',
               '.....']]

J_template = [['.....',
               '.O...',
               '.OOO.',
               '.....',
               '.....'],
              ['.....',
               '..OO.',
               '..O..',
               '..O..',
               '.....'],
              ['.....',
               '.....',
               '.OOO.',
               '...O.',
               '.....'],
              ['.....',
               '..O..',
               '..O..',
               '.OO..',
               '.....']]

L_template = [['.....',
               '...O.',
               '.OOO.',
               '.....',
               '.....'],
              ['.....',
               '..O..',
               '..O..',
               '..OO.',
               '.....'],
              ['.....',
               '.....',
               '.OOO.',
               '.O...',
               '.....'],
              ['.....',
               '.OO..',
               '..O..',
               '..O..',
               '.....']]

O_template = [['.....',
               '.....',
               '.OO..',
               '.OO..',
               '.....']]

T_template = [['.....',
               '..O..',
               '.OOO.',
               '.....',
               '.....'],
              ['.....',
               '..O..',
               '..OO.',
               '..O..',
               '.....'],
              ['.....',
               '.....',
               '.OOO.',
               '..O..',
               '.....'],
              ['.....',
               '..O..',
               '.OO..',
               '..O..',
               '.....']]

all_pieces = {'I': I_template,
          'J': J_template,
          'L': L_template,
          'O': O_template,
          'S': S_template,
          'T': T_template,
          'Z': Z_template}

def get_new_piece():
    shape =  random.choice(list(all_pieces.keys()))
    list_keys = list(all_pieces.keys())
    new_piece = {'shape': shape,
                 'rotation': random.randint(0, len(all_pieces[shape]) - 1),
                 'x':int(play_width / 2) - int(template_width / 2),
                 'y': -2,
                 'colour': list_keys.index(shape) }
    return new_piece

def create_board(): #create a list of 10 by 20 '.'
    board = []
    for i in  range(play_width):
        board.append([blank] * play_height)
    return board

def draw_board(board):
    pygame.draw.rect(game_win, border_colour,(Xmargin - 3, Ymargin - 7, (play_width * box_size) + 8, (play_height * box_size) + 8), 5) #create a white box
    pygame.draw.rect(game_win, BGcolour, (Xmargin, Ymargin, box_size * play_width, box_size * play_height)) #black box inside the white one
    # create the grid using board[x][y] as the colour
    for x in range(play_width):
        for y in range (play_height):
            draw_box(x, y, board[x][y])

def convert_to_pixel(boxx, boxy): # convert play coordinates (on the grid 10 x 20) to pixel location
    return Xmargin + (boxx * box_size), Ymargin + (boxy * box_size)

def draw_box(boxx, boxy, colour, pixelx=None, pixely=None):
    # when board[x][y] is put in as colour all the '.' will be black
    if colour == blank:
        return
    if pixelx == None and pixely == None:
        pixelx, pixely = convert_to_pixel(boxx, boxy)
    pygame.draw.rect(game_win, colours[colour], (pixelx + 1, pixely + 1, box_size - 1, box_size - 1))
    pygame.draw.rect(game_win, light_colours[colour],
                     (pixelx + 1, pixely + 1, box_size - 4, box_size - 4))

def draw_piece(piece, pixelx=None, pixely=None):
    shape_to_draw = all_pieces[piece['shape']][piece['rotation']]
    if pixelx == None and pixely == None:
        pixelx, pixely = convert_to_pixel(piece['x'],piece['y'])
    for x in range(template_width):
        for y in range(template_height):
            if shape_to_draw[y][x] != blank:
                draw_box(None, None, piece['colour'], pixelx + (x * box_size), pixely + (y * box_size))


def add_to_board(board, piece):
    for x in range(template_width):
        for y in range(template_height):
            if all_pieces[piece['shape']][piece['rotation']][y][x] != blank:
                board[x + piece['x']][y + piece['y']] = piece['colour']

def on_board(x, y):
    return x >= 0 and x < play_width and y < play_height

def valid_position(board, piece, adjX=0, adjY=0):
    for x in range(template_width):
        for y in range(template_height):
            isAboveBoard = y + piece['y'] + adjY < 0
            if isAboveBoard or all_pieces[piece['shape']][piece['rotation']][y][x] == blank:
                
                continue
            if not on_board(x + piece['x'] + adjX, y + piece['y'] + adjY):
                return False
            if board[x + piece['x'] + adjX][y + piece['y'] + adjY] != blank:
                return False
    return True

def complete_line(board, y): #return true if a line is complete
    for x in range(play_width):
        if board[x][y] == blank:
            return False
    return True


def remove_complete_lines(board):
    numCompleteLines = 0
    y = play_height - 1
    while y >= 0:
        if complete_line(board, y):
            for pulldowny in range(y, 0, -1): #itterate through from y to 0 in incriments of -1
                for x in range(play_width):
                    board[x][pulldowny] = board[x][pulldowny -1]
            #set top line to blank
            for x in range(play_width):
                board[x][0] = blank
            numCompleteLines += 1
        else:
            y -= 1
    return numCompleteLines


def fall_frequency(score):
    level = int(score / 10) +1
    fall_freq = 0.27 - (level * 0.02)
    return level, fall_freq

def draw_next_piece(piece):
    label = basic_font.render('Next piece: ', True, WHITE)
    rect = label.get_rect()
    rect.topleft = (display_width - 120, 80)
    game_win.blit(label, rect)
    draw_piece(piece, pixelx=display_width - 120, pixely=100)

def print_score(score, level):
    score_surf = basic_font.render('Score: ' + str(score), True, WHITE)
    score_rect = score_surf.get_rect()
    score_rect.topleft = (0, 0)
    level_surf = basic_font.render('Level: ' + str(level), True, WHITE)
    level_rect = level_surf.get_rect()
    level_rect.topleft = (0, 20)
    game_win.blit(score_surf, score_rect)
    game_win.blit(level_surf, level_rect)




def check_for_quit():
    for event in pygame.event.get(QUIT):
        pygame.quit()
        sys.exit()
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            pygame.quit()
            sys.exit()

def main():
    global  game_win, basic_font, big_font
    pygame.init()
    game_win = pygame.display.set_mode((display_width, display_height))
    FPSclock = pygame.time.Clock()
    pygame.display.set_caption('Tetris')
    basic_font = pygame.font.SysFont('comicsansms', 18)
    big_font = pygame.font.SysFont('comicsansms', 100)
    score = 0
    complete_line = 0
    game_running = True
    last_fall_time = time.time()
    level, fall_freq = fall_frequency(score)
    board = create_board()
    falling_piece = get_new_piece()
    next_piece = get_new_piece()

    while game_running:
        check_for_quit()
        if falling_piece == None:
            falling_piece = next_piece
            next_piece = get_new_piece()
            last_fall_time = time.time()

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_RIGHT and valid_position(board, falling_piece, adjX=1):
                    falling_piece['x'] += 1

                if event.key == K_LEFT and valid_position(board, falling_piece, adjX=-1):
                    falling_piece['x'] -= 1
                if event.key == K_UP:
                    falling_piece['rotation'] = (falling_piece['rotation'] + 1) % len(all_pieces[falling_piece['shape']])
                    if not valid_position(board, falling_piece):
                        falling_piece['rotation'] = (falling_piece['rotation'] - 1) % len(all_pieces[falling_piece['shape']])
                if event.key == K_DOWN and valid_position(board, falling_piece, adjY=1):
                    falling_piece['y'] +=1

        if time.time() - last_fall_time > fall_freq:
            if not valid_position(board, falling_piece, adjY=1):
                add_to_board(board, falling_piece)
                complete_line += remove_complete_lines(board)
                level, fall_freq = fall_frequency(complete_line)
                falling_piece = None
            else:
                falling_piece['y'] += 1
                last_fall_time = time.time()
        game_win.fill(BGcolour)
        draw_board(board)

        if falling_piece != None:
            draw_piece(falling_piece)
        draw_next_piece(next_piece)
        print_score(score, level)
        pygame.display.update()
        FPSclock.tick(FPS)



main()
