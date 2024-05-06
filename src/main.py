import pygame
from GUI_constants import *
from game_screen import display_game_screen
from game_screen import game_action
from menu_screen import display_menu
from menu_screen import bot_button_rect, multiplayer_button_rect
from player import Player
from p2p_node import P2PNode
from random_player import RandomPlayer

import numpy as np
from place_ships_screen import display_place_ships_screen

def draw_grid(screen, grid, type):
    if type == "primary":
        block_size = PRIMARY_CELL_SIZE
        x_offset = PRIMARY_GRID_X
        y_offset = PRIMARY_GRID_Y
        color_default = WHITE
        color_ship = BLUE
        color_hit = YELLOW
        color_sunk = GREEN
        color_miss = BLUE
    else:
        block_size = SECONDARY_CELL_SIZE
        x_offset = SECONDARY_GRID_X
        y_offset = SECONDARY_GRID_Y
        color_default = WHITE
        color_ship = GREEN
        color_hit = YELLOW
        color_sunk = RED
        color_miss = BLUE



p1 = Player("Player 1")
for ship in p1.get_ships_list():
    while not p1.place_ship(ship, np.random.randint(0, 10), np.random.randint(0, 10), np.random.choice(['horizontal', 'vertical'])):
        pass

            # color the cell according to the states cell
            if game[x][y] == 0:
                pygame.draw.rect(screen, WHITE, rect)
            if game[x][y] == 1:
                pygame.draw.rect(screen, BLUE, rect)
            if game[x][y] == 2:
                pygame.draw.rect(screen, RED, rect)
            if game[x][y] == 3:
                pygame.draw.rect(screen, GREEN, rect)

p2 = Player("Player 2")
for ship in p2.get_ships_list():
    while not p2.place_ship(ship, np.random.randint(0, 10), np.random.randint(0, 10), np.random.choice(['horizontal', 'vertical'])):
        pass


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
    return min(x, GRID_SIZE), min(y, GRID_SIZE), type


my_ip = "172.16.18.98"
bot_ip = my_ip # "192.168.178.32"


my_player = Player("Player1")
my_node = P2PNode(my_ip, 65433)
my_player.node = my_node
my_node.player = my_player
my_node.connect_to(bot_ip)

bot_player = RandomPlayer("Player2")
bot_node = P2PNode(bot_ip)
bot_player.node = bot_node
bot_node.player = bot_player
bot_node.connect_to(my_ip, 65433)


print("Placing ships randomly...")
for ship in my_player.get_ships_list():
    while not my_player.place_ship(ship, np.random.randint(0, 10), np.random.randint(0, 10),
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

# initial screen-state
current_state = "menu"


# Main loop
running = True
while running:
    # fill the window white
    screen.fill(WHITE)

    if current_state == "menu":
        display_menu(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # if button press is mouse click
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if bot_button_rect.collidepoint(event.pos):
                    # current_state = "place_ships"
                    current_state = "game"
                    print("Start Bot Game")
                if multiplayer_button_rect.collidepoint(event.pos):
                    # current_state = "place_ships"
                    current_state = "game"
                    print("Start Multiplayer Game")
    elif current_state == "place_ships":
        display_place_ships_screen(screen, p1)
    elif current_state == "game":
        display_game_screen(screen, p1)
        # get key press events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # if button press is mouse click
            elif event.type == pygame.MOUSEBUTTONDOWN:
                game_action(event.button, p1, p2)
    # elif current_state == "game_over":
    #     display_game_over(screen)

    # refresh the display
    pygame.display.flip()

# Quit pygame
pygame.quit()
