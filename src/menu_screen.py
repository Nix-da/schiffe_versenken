import pygame
from GUI_constants import *

pygame.font.init()
window_size = (WINDOW_SIZE_X, WINDOW_SIZE_Y)

# Define button properties
button_font = pygame.font.SysFont(None, 24)
text = button_font.render("Start Game", True, WHITE)
text_rect = text.get_rect(center=(window_size[0] // 2, window_size[1] // 2))
button_rect = pygame.Rect(150, 100, 250, 50)

button_rect.center = text_rect.center


def draw_button(screen):
    pygame.draw.rect(screen, BLACK, button_rect)
    screen.blit(text, text_rect)


def display_menu(screen):
    draw_button(screen)