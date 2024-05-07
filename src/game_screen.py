import pygame
from grid_logic import draw_grid, draw_legend, get_cell
from GUI_constants import *

# Define button properties
pygame.font.init()
button_font = pygame.font.SysFont(None, 24)
menu_text = button_font.render("Main Menu", True, WHITE)
menu_button_rect = pygame.Rect(MENU_BUTTON_X, MENU_BUTTON_Y, MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT)
menu_text_rect = menu_text.get_rect(center=menu_button_rect.center)

def display_game_screen(screen, p1):
    draw_grid(screen, p1.enemy_grid, "primary")
    draw_grid(screen, p1.grid, "secondary")
    # draw legend
    draw_legend(screen, "hits")
    # Draw the button
    pygame.draw.rect(screen, BLACK, menu_button_rect)
    screen.blit(menu_text, menu_text_rect)

def game_action(eventButton, game_type, player, enemy_player):
    # get position of the mouse on the screen
    pos = pygame.mouse.get_pos()
    if eventButton == 1:
        # convert the screen position to grid position
        x, y, type = get_cell(pos[0], pos[1])

        # if the position is on the primary grid, attack the enemy
        if type == "primary":
            # but only if you are on turn and have not attacked this position before
            if player.on_turn and player.enemy_grid[x][y] == 0:
                if game_type == "bot":
                    player.attack_bot(enemy_player, x, y)
                elif game_type == "multiplayer":
                    player.node.send_message("action;attack;" + str(x) + ";" + str(y))
        # if the position is on the main menu button, return to the main menu
        elif menu_button_rect.collidepoint(pos):
            return "menu"
    return None