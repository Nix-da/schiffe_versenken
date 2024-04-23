import pygame
import numpy as np
from GUI_constants import *
from player import Player
from server import Server
from client import Client
import socket
import threading


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


def get_my_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


s = Server(get_my_ip(), 12345)
c = Client(get_my_ip(), 12345)
c.send_message("Hello World")
s.send_message("Hello World")



p1 = Player("Player 1")
for ship in p1.get_ships_list():
    while not p1.place_ship(ship, np.random.randint(0, 10), np.random.randint(0, 10),
                            np.random.choice(['horizontal', 'vertical'])):
        pass

p2 = Player("Player 2")
for ship in p2.get_ships_list():
    while not p2.place_ship(ship, np.random.randint(0, 10), np.random.randint(0, 10),
                            np.random.choice(['horizontal', 'vertical'])):
        pass

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

primary_own = 1  # 0 = own field on top, 1 = enemy field on top
state = 0  # 0 = placing ships, 1 = attacking, 2 = game over

# Main loop
running = True
while running:
    # fill the window white
    screen.fill(WHITE)
    # draw two grids

    if primary_own == 0:
        draw_grid(screen, p1.grid, "primary")
        draw_grid(screen, p1.enemy_grid, "secondary")
    else:
        draw_grid(screen, p1.enemy_grid, "primary")
        draw_grid(screen, p1.grid, "secondary")

    # get key press events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if button press is mouse click
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # get position of the mouse on the screen
            pos = pygame.mouse.get_pos()
            if event.button == 1:
                # convert the screen position to grid position
                x, y, type = get_cell(pos[0], pos[1])
                print(get_cell(pos[0], pos[1]))

                # if the position is on the primary grid, attack the enemy
                if type == "primary":
                    p1.attack(p2, x, y)
                # if the position is on the secondary grid, toggle the grids
                if type == "secondary":
                    primary_own = not primary_own
                    print("Toggle primary and secondary grid")

    # refresh the display
    pygame.display.flip()

# Quit pygame
pygame.quit()