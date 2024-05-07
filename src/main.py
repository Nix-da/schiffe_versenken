import pygame
from GUI_constants import *
from game_screen import display_game_screen
from game_screen import game_action
from menu_screen import display_menu
from menu_screen import bot_button_rect, multiplayer_button_rect
from player import Player
from p2p_node import P2PNode, get_my_ip
from random_player import RandomPlayer
import numpy as np
from place_ships_screen import display_place_ships_screen
from multiplayer_connect_screen import display_multiplayer_connect_screen, multiplayer_connect_action


my_player = None
enemy_player = None

my_ip = get_my_ip()
enemy_ip = None


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
game_type = "bot"

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
                    game_type = "bot"
                    print("Start Bot Game")

                    my_player = Player("Player")
                    enemy_player = RandomPlayer("Bot")

                if multiplayer_button_rect.collidepoint(event.pos):
                    current_state = "multiplayer connect"

    if current_state == "multiplayer connect":
        display_multiplayer_connect_screen(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if multiplayer_connect_action(event) is not None:
                current_state = "place_ships"
                current_state = "game"
                game_type = "multiplayer"
                print("Start Multiplayer Game")

                my_ip = get_my_ip()
                enemy_ip = multiplayer_connect_action(event)

                my_player = Player("Player")
                my_node = P2PNode(my_ip)
                my_player.node = my_node
                my_node.player = my_player
                my_node.connect_to(enemy_ip)

                enemy_player = Player("Opponent")
                enemy_node = P2PNode(enemy_ip)
                enemy_player.node = enemy_node
                enemy_node.player = enemy_player
                enemy_node.connect_to(my_ip)

    if current_state == "place_ships":
        display_place_ships_screen(screen, my_player)

    if current_state == "game":
        display_game_screen(screen, my_player)
        # get key press events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # if button press is mouse click
            elif event.type == pygame.MOUSEBUTTONDOWN:
                game_action(event.button, game_type, my_player, enemy_player)
    # elif current_state == "game_over":
    #     display_game_over(screen)

    # refresh the display
    pygame.display.flip()

# Quit pygame
pygame.quit()
