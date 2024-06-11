import numpy as np
import pygame
import requests
from GUI_constants import *
from game_screen import display_game_screen, game_action, menu_button_rect
from menu_screen import display_menu
from menu_screen import bot_button_rect, multiplayer_button_rect
from player import Player
from p2p_node import P2PNode, get_my_ip
from random_player import RandomPlayer
from game_over_screen import display_game_over_screen, game_over_action
from place_ships_screen import display_place_ships_screen, place_ship_action, vertical_button_rect, \
    placement_orientation, start_game_button_rect, random_button_rect
from multiplayer_connect_screen import display_multiplayer_connect_screen, multiplayer_connect_action
from flask_server import app, get_skill_message

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


def back_to_menu():
    global current_state
    current_state = "menu"

def start_bot_game():
    global current_state, game_type, my_player, enemy_player
    current_state = "place_ships"
    game_type = "bot"
    print("Start Bot Game")

    my_player = Player("Player")
    enemy_player = RandomPlayer("Bot")


def start_multiplayer_game():
    global current_state
    current_state = "multiplayer connect"


def multiplayer_connect(ip):
    global current_state, game_type, my_player, enemy_player, my_ip, enemy_ip
    current_state = "place_ships"
    game_type = "multiplayer"
    print("Start Multiplayer Game")

    my_ip = get_my_ip()
    enemy_ip = ip

    my_player = Player("Player")
    my_node = P2PNode(my_ip)
    my_player.node = my_node
    my_node.player = my_player
    my_node.connect_to(enemy_ip)
    enemy_player = Player("Opponent")


def start_game_phase():
    global current_state, my_player
    if my_player.all_ships_placed():
        current_state = "game"

def place_ships_random():
    global my_player
    while not my_player.all_ships_placed():
        my_player.place_ship(my_player.get_not_placed_ship_list()[0], np.random.randint(0, 9),
                             np.random.randint(0, 9), np.random.choice(["horizontal", "vertical"]))


# Main loop
running = True
while running:
    voice_action = get_skill_message()
    overwrite_click = False
    if voice_action is not None:
        print(voice_action)

    # fill the window white
    screen.fill(WHITE)

    if current_state == "menu":
        if voice_action is not None and voice_action == "bot modus":
            start_bot_game()
        elif voice_action is not None and voice_action == "multiplayer modus":
            start_multiplayer_game()

        display_menu(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # if button press is mouse click
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if bot_button_rect.collidepoint(event.pos):
                    start_bot_game()

                if multiplayer_button_rect.collidepoint(event.pos) or voice_action == "multiplayer modus":
                    start_multiplayer_game()

    if current_state == "multiplayer connect":
        if voice_action is not None and voice_action.startswith("connect to"):
            multiplayer_connect(voice_action.split(" ")[-1])

        display_multiplayer_connect_screen(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if multiplayer_connect_action(event) is not None:
                multiplayer_connect(multiplayer_connect_action(event))

    if current_state == "place_ships":
        if voice_action is not None and voice_action == "random place ships":
            place_ships_random()
        elif voice_action is not None and voice_action == "restart":
            back_to_menu()
        elif voice_action is not None and voice_action == "start game":
            start_game_phase()

        display_place_ships_screen(screen, my_player,
                                   [ship.__class__.__name__ for ship in my_player.get_not_placed_ship_list()])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # if button press is mouse click
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    place_ship_action(event.button, my_player)
                if vertical_button_rect.collidepoint(event.pos):
                    placement_orientation = "horizontal" if placement_orientation == "vertical" else "vertical"
                if random_button_rect.collidepoint(event.pos):
                    place_ships_random()
                if start_game_button_rect.collidepoint(event.pos):
                    start_game_phase()
                if menu_button_rect.collidepoint(event.pos):
                    back_to_menu()

    if current_state == "game":
        if voice_action is not None and voice_action == "restart":
            back_to_menu()

        display_game_screen(screen, my_player)
        # get key press events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # if button press is mouse click
            elif event.type == pygame.MOUSEBUTTONDOWN:
                game_action(event.button, game_type, my_player, enemy_player)

                if menu_button_rect.collidepoint(event.pos):
                    back_to_menu()
        if my_player.game_over:
            current_state = "game_over"

    elif current_state == "game_over":
        if voice_action is not None and voice_action == "restart":
            back_to_menu()

        display_game_over_screen(screen, my_player.game_over)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # if button press is mouse click
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game_over_action(event.button) == "menu":
                    back_to_menu()

    # refresh the display
    pygame.display.flip()

# Quit pygame
pygame.quit()
