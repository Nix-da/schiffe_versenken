import pygame
import numpy as np
from GUI_constants import *


def draw_grid(screen, game, type):
    if type == "primary":
        block_size = PRIMARY_CELL_SIZE
        x_offset = PRIMARY_GRID_X
        y_offset = PRIMARY_GRID_Y
    else:
        block_size = SECONDARY_CELL_SIZE
        x_offset = SECONDARY_GRID_X
        y_offset = SECONDARY_GRID_Y

    GRID_SIZE = 10

    # generate a 10x10 grid
    for x in range(GRID_SIZE):
        x_position = x * block_size + x_offset
        for y in range(GRID_SIZE):
            y_position = y * block_size + y_offset
            rect = pygame.Rect(x_position, y_position, block_size, block_size)

            # color the cell according to the states cell
            if game[x][y] == 0:
                pygame.draw.rect(screen, WHITE, rect)
            if game[x][y] == 1:
                pygame.draw.rect(screen, BLUE, rect)
            if game[x][y] == 2:
                pygame.draw.rect(screen, RED, rect)
            if game[x][y] == 3:
                pygame.draw.rect(screen, GREEN, rect)

            pygame.draw.rect(screen, BLACK, rect, 1)

    # make the outline bold
    rect = pygame.Rect(x_offset, y_offset, block_size * GRID_SIZE, block_size * GRID_SIZE)
    pygame.draw.rect(screen, BLACK, rect, 3)


def get_cell(x, y):
    type = None
    if PRIMARY_GRID_X <= x <= PRIMARY_GRID_X + PRIMARY_CELL_SIZE * GRID_SIZE:
        if PRIMARY_GRID_Y <= y <= PRIMARY_GRID_Y + PRIMARY_CELL_SIZE * GRID_SIZE:
            type = "primary"
    if SECONDARY_GRID_X <= x <= SECONDARY_GRID_X + SECONDARY_CELL_SIZE * GRID_SIZE:
        if SECONDARY_GRID_Y <= y <= SECONDARY_GRID_Y + SECONDARY_CELL_SIZE * GRID_SIZE:
            type = "secondary"

    if type == "primary":
        block_size = PRIMARY_CELL_SIZE
        x_offset = PRIMARY_GRID_X
        y_offset = PRIMARY_GRID_Y
    elif type == "secondary":
        block_size = SECONDARY_CELL_SIZE
        x_offset = SECONDARY_GRID_X
        y_offset = SECONDARY_GRID_Y
    else:
        return 0, 0, None

    x = (x - x_offset) // block_size
    y = (y - y_offset) // block_size
    return x, y, type


# Initialize the pygame
pygame.init()

# Set the dimensions of the window
window_size = (WINDOW_SIZE_X, WINDOW_SIZE_Y)
screen = pygame.display.set_mode(window_size)
# fill the window with the color white
screen.fill(WHITE)

# Set the window name
pygame.display.set_caption('Schiffe versenken')

# Set the window icon
icon = pygame.image.load('./assets/icon.png')
pygame.display.set_icon(icon)

t1 = np.zeros((10, 10))
t2 = np.zeros((10, 10))

# Main loop
running = True
while running:
    # fill the window white
    screen.fill(WHITE)
    # draw two grids

    draw_grid(screen, t1, "primary")
    draw_grid(screen, t2, "secondary")

    # get key press events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if event.button == 1:
                x, y, type = get_cell(pos[0], pos[1])
                print(get_cell(pos[0], pos[1]))
                if type == "primary":
                    t1[x][y] = (t1[x][y] + 1) % 4
                if type == "secondary":
                    t = t1
                    t1 = t2
                    t2 = t

    # refresh the display
    pygame.display.flip()

# Quit pygame
pygame.quit()
