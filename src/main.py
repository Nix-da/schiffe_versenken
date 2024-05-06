import pygame
from GUI_constants import *
from game_screen import display_game_screen
from game_screen import game_action
from menu_screen import display_menu
from menu_screen import bot_button_rect, multiplayer_button_rect
from player import Player
import numpy as np
from place_ships_screen import display_place_ships_screen



p1 = Player("Player 1")
for ship in p1.get_ships_list():
    while not p1.place_ship(ship, np.random.randint(0, 10), np.random.randint(0, 10), np.random.choice(['horizontal', 'vertical'])):
        pass


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
