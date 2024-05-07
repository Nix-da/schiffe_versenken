import pygame
from GUI_constants import *
from ships import Battleship, Cruiser, Destroyer, Submarine
from grid_logic import draw_grid, draw_legend, get_cell
from player import Player

pygame.font.init()
window_size = (WINDOW_SIZE_X, WINDOW_SIZE_Y)

# Define button properties
button_font = pygame.font.SysFont(None, 24)

random_text = button_font.render("Random Placement", True, WHITE)
random_button_rect = pygame.Rect(150, 100, 200, 50)
# random_text_rect = random_text.get_rect(center=(window_size[0] // 2, 150 + window_size[1] // 2))
random_text_rect = random_text.get_rect(center=(window_size[0] - 370, 150 + window_size[1] // 2))

start_game_text = button_font.render("Start Game", True, WHITE)
start_game_button_rect = pygame.Rect(150, 100, 200, 50)
start_game_text_rect = start_game_text.get_rect(center=(window_size[0] - 130, 150 + window_size[1] // 2))

random_button_rect.center = random_text_rect.center
start_game_button_rect.center = start_game_text_rect.center


def draw_button(screen):
    pygame.draw.rect(screen, BLACK, random_button_rect)
    screen.blit(random_text, random_text_rect)

    pygame.draw.rect(screen, BLACK, start_game_button_rect)
    screen.blit(start_game_text, start_game_text_rect)


def display_place_ships_screen(screen, player, ships):
    draw_grid(screen, player.grid, "primary")
    draw_legend(screen, "Your Ships", ships)
    draw_button(screen)
    # draw legend
    # draw_legend(screen, "place your ships")


def place_ship_action(eventButton, player):
    # get position of the mouse on the screen
    pos = pygame.mouse.get_pos()
    if eventButton == 1:
        # convert the screen position to grid position
        x, y, type = get_cell(pos[0], pos[1])
        print(get_cell(pos[0], pos[1]))

        # if the position is on the primary grid, attack the enemy
        # if type == "primary":
