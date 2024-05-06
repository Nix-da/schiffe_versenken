import pygame
from grid_logic import draw_grid, draw_legend, get_cell


def display_game_screen(screen, p1):
    draw_grid(screen, p1.enemy_grid, "primary")
    draw_grid(screen, p1.grid, "secondary")
    # draw legend
    draw_legend(screen, "hits")


def game_action(eventButton, game_type, player, enemy_player):
    # get position of the mouse on the screen
    pos = pygame.mouse.get_pos()
    if eventButton == 1:
        # convert the screen position to grid position
        x, y, type = get_cell(pos[0], pos[1])

        # if the position is on the primary grid, attack the enemy
        if type == "primary":
            if game_type == "bot":
                player.attack_bot(enemy_player, x, y)
            elif game_type == "multiplayer":
                player.node.send_message("action;attack" + str(x) + str(y))
