import pygame
from grid_logic import draw_grid, draw_legend, get_cell
from GUI_constants import *

# Define button properties
pygame.font.init()
window_size = (WINDOW_SIZE_X, WINDOW_SIZE_Y)

button_font = pygame.font.SysFont(None, 24)

menu_text = button_font.render("Main Menu", True, WHITE)
menu_button_rect = pygame.Rect(MENU_BUTTON_X, MENU_BUTTON_Y, MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT)
menu_text_rect = menu_text.get_rect(center=menu_button_rect.center)

turn_font = pygame.font.SysFont(None, 24)
turn_text = turn_font.render("Your turn!", True, BLACK)
turn_text_rect = turn_text.get_rect(center=(PRIMARY_GRID_X + GRID_SIZE * PRIMARY_CELL_SIZE // 2, PRIMARY_GRID_Y - 50))


def display_game_screen(screen, player):
    draw_grid(screen, player.enemy_grid, "primary")
    draw_grid(screen, player.grid, "secondary")
    # draw legend
    draw_legend(screen, "hits")
    # Draw the button
    pygame.draw.rect(screen, BLACK, menu_button_rect)
    screen.blit(menu_text, menu_text_rect)

    if player.on_turn:
        screen.blit(turn_text, turn_text_rect)


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
