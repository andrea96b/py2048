# Example file showing a circle moving on screen
import pygame
import numpy
from Game2048 import Game2048
from Game2048 import Moves


# create a font object.
# 1st parameter is the font file
# which is present in pygame.
# 2nd parameter is size of the font
FONT = None
FONT_SIZE = 32
# define the RGB value for white,
#  green, blue colour .
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 128)
BLACK = (0, 0, 0)
SCREEN_X = 720
SCREEN_Y = 720
BOX_SIZE = 60
SCREEN = None
GAME_MAT = None
CLOCK = None


def get_colour_from_pow_of_two(num : int):
    colors = [
        "orange",
        "orange1",
        "orange2",
        "orange3",
        "orange4",
        "orangered",
        "orangered1",
        "orangered2",
        "orangered3",
        "orangered4"
    ]
    if num == 0:
        return pygame.color.THECOLORS['grey50']
    else:
        index = int(numpy.log2(num))
        if index > 10:
            index = 9
        return pygame.color.THECOLORS[colors[index]]

def draw_box(num: int, x: int, y: int):
    pygame.draw.rect(SCREEN, get_colour_from_pow_of_two(num), pygame.Rect(x-(BOX_SIZE/2), y-(BOX_SIZE/2), BOX_SIZE, BOX_SIZE))
    if num > 0:
        # create a text surface object,
        # on which text is drawn on it.
        text_obj = FONT.render(str(num), True, BLACK)
        
        # create a rectangular object for the
        # text surface object
        text_rect = text_obj.get_rect()
        # set the center of the rectangular object.
        text_rect.center = (x, y)
        SCREEN.blit(text_obj, text_rect)

def show_points():
    text_obj = FONT.render(f'Points: {str(GAME_MAT.points)}', True, BLACK)
    # create a rectangular object for the
    # text surface object
    text_rect = text_obj.get_rect()
    # set the center of the rectangular object.
    text_rect.center = (SCREEN_X//4, SCREEN_Y//4)
    SCREEN.blit(text_obj, text_rect)

def show_end_game():
    text_obj = FONT.render(f'Game End')
    # create a rectangular object for the
    # text surface object
    text_rect = text_obj.get_rect()
    # set the center of the rectangular object.
    text_rect.center = (SCREEN_X*0.5, SCREEN_Y*0.9)
    SCREEN.blit(text_obj, text_rect)

def draw_game():
    for i in range(0, GAME_MAT.row):
        for j in range(0, GAME_MAT.col):
            draw_box(GAME_MAT.mat[j][i], (SCREEN_X-SCREEN_X*0.7)+(i*(BOX_SIZE+10)),(SCREEN_Y-SCREEN_Y*0.5)+(j*(BOX_SIZE+10)))

def init_and_run_game():
    global GAME_MAT
    global FONT
    global CLOCK
    global SCREEN
    # pygame setup
    pygame.init() 
    FONT = pygame.font.Font(pygame.font.get_default_font(), FONT_SIZE)
    SCREEN = pygame.display.set_mode((720, 720))
    GAME_MAT = Game2048()
    CLOCK = pygame.time.Clock()
    running = True
    continue_game = True
    move = None
    dt = 0
    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    move = Moves.LEFT
                elif event.key ==pygame.K_RIGHT:
                    move = Moves.RIGHT
                elif event.key ==pygame.K_UP:
                    move = Moves.UP
                elif event.key ==pygame.K_DOWN:
                    move = Moves.DOWN
                else:
                    pass

                if move:
                    continue_game = GAME_MAT.execute_move(move)
                if not continue_game:
                    running = False

        # fill the screen with a color to wipe away anything from last frame
        SCREEN.fill("grey")
        draw_game()

        move = None
        show_points()
        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = CLOCK.tick(60) / 1000

    pygame.quit()
    return GAME_MAT.points


if __name__ == '__main__':
    points = init_and_run_game()
    print(f'Total points: {points}')
    points = init_and_run_game()
    print(f'Total points: {points}')