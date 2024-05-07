import pygame
from GUI_constants import *
from p2p_node import get_my_ip

pygame.font.init()
window_size = (WINDOW_SIZE_X, WINDOW_SIZE_Y)

# Define button properties
button_font = pygame.font.SysFont(None, 32)
input_font = pygame.font.SysFont(None, 24)
input_box = pygame.Rect(100, 200, 140, 32)
color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')
color = color_inactive
active = False
text = ''
connect_button_rect = pygame.Rect(100, 300, 140, 32)

placeholder_text = "Enter opponent's IP..."


def draw_elements(screen):
    # Draw IP label
    ip_label = button_font.render("Your IP: " + get_my_ip(), True, (0, 0, 0))
    screen.blit(ip_label, (100, 100))

    # Draw input box
    if active or text != '':
        txt_surface = input_font.render(text, True, color)
    else:
        txt_surface = input_font.render(placeholder_text, True, pygame.Color('lightgray'))
    width = max(200, txt_surface.get_width() + 10)
    input_box.w = width
    screen.blit(txt_surface, (input_box.x + 5, input_box.y + 10))
    pygame.draw.rect(screen, color, input_box, 2)

    # Draw connect button
    pygame.draw.rect(screen, (0, 0, 0), connect_button_rect)
    connect_button = button_font.render("Connect", True, (255, 255, 255))
    screen.blit(connect_button, (connect_button_rect.x + 5, connect_button_rect.y + 5))


def display_multiplayer_connect_screen(screen):
    draw_elements(screen)


def multiplayer_connect_action(event):
    global active, text, color
    if event.type == pygame.MOUSEBUTTONDOWN:
        if connect_button_rect.collidepoint(event.pos):
            return text
        if input_box.collidepoint(event.pos):
            active = not active
            if text == placeholder_text:
                text = ''
        else:
            active = False
        color = color_active if active else color_inactive
    elif event.type == pygame.KEYDOWN:
        if event.unicode in '0123456789.':
            if active:
                if event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode
    return None
