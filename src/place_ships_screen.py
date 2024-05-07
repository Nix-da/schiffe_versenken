import pygame
from GUI_constants import *
from ships import Battleship, Cruiser, Destroyer, Submarine
from grid_logic import draw_grid, draw_legend, get_cell
from player import Player

selected_ship = None
selected_ship_index = None
placement_orientation = "horizontal"

pygame.font.init()
window_size = (WINDOW_SIZE_X, WINDOW_SIZE_Y)

# Define button properties
button_font = pygame.font.SysFont(None, 24)

menu_text = button_font.render("Main Menu", True, WHITE)
menu_button_rect = pygame.Rect(MENU_BUTTON_X, MENU_BUTTON_Y, MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT)
menu_text_rect = menu_text.get_rect(center=menu_button_rect.center)

random_text = button_font.render("Random Placement", True, WHITE)
random_button_rect = pygame.Rect(150, 100, 200, 50)
random_text_rect = random_text.get_rect(center=(window_size[0] - 400, 150 + window_size[1] // 2))

start_game_text = button_font.render("Start Game", True, WHITE)
start_game_button_rect = pygame.Rect(150, 100, 200, 50)
start_game_text_rect = start_game_text.get_rect(center=(window_size[0] - 150, 150 + window_size[1] // 2))

label_font = pygame.font.SysFont(None, 24)
label_text = label_font.render("Select placement:", True, BLACK)
label_text_rect = label_text.get_rect(center=(LEGEND_X - 70, LEGEND_Y - 40))

vertical_text = button_font.render("horizontal", True, WHITE)
vertical_button_rect = pygame.Rect(LEGEND_X, LEGEND_Y, 100, 25)
vertical_text_rect = vertical_text.get_rect(center=(LEGEND_X + 70, LEGEND_Y - 20))

horizontal_text = button_font.render("vertical", True, WHITE)
horizontal_button_rect = pygame.Rect(LEGEND_X, LEGEND_Y, 100, 25)
horizontal_text_rect = horizontal_text.get_rect(center=(LEGEND_X + 70, LEGEND_Y - 50))

horizontal_button_rect.center = horizontal_text_rect.center
vertical_button_rect.center = vertical_text_rect.center
random_button_rect.center = random_text_rect.center
start_game_button_rect.center = start_game_text_rect.center


def draw_button(screen):
    pygame.draw.rect(screen, BLACK, random_button_rect)
    screen.blit(random_text, random_text_rect)

    pygame.draw.rect(screen, BLACK, start_game_button_rect)
    screen.blit(start_game_text, start_game_text_rect)


    pygame.draw.rect(screen, BLACK, menu_button_rect)
    screen.blit(menu_text, menu_text_rect)


def display_place_ships_screen(screen, player, ships):
    draw_grid(screen, player.grid, "primary")
    draw_legend(screen, "Your Ships", ships, selected_ship_index)
    draw_button(screen)

    # Update button text and color based on placement_orientation
    if placement_orientation == "vertical":
        pygame.draw.rect(screen, BLACK, vertical_button_rect)
        pygame.draw.rect(screen, GRAY, horizontal_button_rect)
        vertical_text = button_font.render("vertical", True, WHITE)
        horizontal_text = button_font.render("horizontal", True, LIGHT_GRAY)
    else:
        pygame.draw.rect(screen, GRAY, vertical_button_rect)
        pygame.draw.rect(screen, BLACK, horizontal_button_rect)
        vertical_text = button_font.render("vertical", True, LIGHT_GRAY)
        horizontal_text = button_font.render("horizontal", True, WHITE)

    horizontal_text_rect.left = horizontal_button_rect.left + 5
    vertical_text_rect.left = vertical_button_rect.left + 5

    screen.blit(vertical_text, vertical_text_rect)
    screen.blit(horizontal_text, horizontal_text_rect)

    screen.blit(label_text, label_text_rect)


def place_ship_action(eventButton, player):
    global selected_ship_index, selected_ship, placement_orientation
    pos = pygame.mouse.get_pos()
    if eventButton == 1:
        x, y, type = get_cell(pos[0], pos[1])
        if type == "legend":
            selected_ship = player.get_not_placed_ship_list()[y]
            selected_ship_index = y
        elif type == "primary":
            if selected_ship is not None:
                if player.place_ship(selected_ship, y, x,
                                     "vertical" if placement_orientation == "horizontal" else "horizontal"):
                    selected_ship = None
                    selected_ship_index = None
            else:
                if player.get_coordinate_ship(x, y):
                    player.unplace_ship(player.get_coordinate_ship(x, y))
        elif vertical_button_rect.collidepoint(pos):
            placement_orientation = "vertical"
        elif horizontal_button_rect.collidepoint(pos):
            placement_orientation = "horizontal"
