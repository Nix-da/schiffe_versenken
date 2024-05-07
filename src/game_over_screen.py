import pygame
from GUI_constants import *

pygame.font.init()
window_size = (WINDOW_SIZE_X, WINDOW_SIZE_Y)

# Define button properties
button_font = pygame.font.SysFont(None, 24)

menu_text = button_font.render("Main Menu", True, WHITE)
menu_button_rect = pygame.Rect(150, 100, 200, 50)
menu_text_rect = menu_text.get_rect(center=(window_size[0] // 2, window_size[1] // 2 + 50))

menu_button_rect.center = menu_text_rect.center


def draw_elements(screen, game_over_text):
    # Define the result text
    result_text = button_font.render(game_over_text, True, BLACK)
    result_text_rect = result_text.get_rect(center=(window_size[0] // 2, window_size[1] // 2 - 50))
    # Draw the result text
    screen.blit(result_text, result_text_rect)

    # Draw the button
    pygame.draw.rect(screen, BLACK, menu_button_rect)
    screen.blit(menu_text, menu_text_rect)


def display_game_over_screen(screen, game_over_text):
    draw_elements(screen, game_over_text)


def game_over_action(eventButton):
    if eventButton == 1:
        if menu_button_rect.collidepoint(pygame.mouse.get_pos()):
            return "menu"
    return None
