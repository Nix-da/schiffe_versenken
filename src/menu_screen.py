import pygame
from GUI_constants import *

pygame.font.init()
window_size = (WINDOW_SIZE_X, WINDOW_SIZE_Y)

# Define button properties
button_font = pygame.font.SysFont(None, 24)

bot_text = button_font.render("Start Bot Game", True, WHITE)
bot_button_rect = pygame.Rect(150, 100, 250, 50)
bot_text_rect = bot_text.get_rect(center=(window_size[0] // 2, window_size[1] // 2))

multiplayer_text = button_font.render("Start Multiplayer Game", True, WHITE)
multiplayer_button_rect = pygame.Rect(150, 100, 250, 50)
multiplayer_text_rect = multiplayer_text.get_rect(center=(window_size[0] // 2, 75 + window_size[1] // 2))

bot_button_rect.center = bot_text_rect.center
multiplayer_button_rect.center = multiplayer_text_rect.center


def draw_button(screen):
    pygame.draw.rect(screen, BLACK, bot_button_rect)
    screen.blit(bot_text, bot_text_rect)

    pygame.draw.rect(screen, BLACK, multiplayer_button_rect)
    screen.blit(multiplayer_text, multiplayer_text_rect)


def display_menu(screen):
    draw_button(screen)
