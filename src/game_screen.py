import pygame
from grid_logic import draw_grid, draw_legend, get_cell

def display_game_screen(screen, p1):
    draw_grid(screen, p1.enemy_grid, "primary")
    draw_grid(screen, p1.grid, "secondary")
    # draw legend
    draw_legend(screen, "hits")


def game_action(eventButton, p1, p2):
    # get position of the mouse on the screen
    pos = pygame.mouse.get_pos()
    if eventButton == 1:
        # convert the screen position to grid position
        x, y, type = get_cell(pos[0], pos[1])
        print(get_cell(pos[0], pos[1]))

        # if the position is on the primary grid, attack the enemy
        if type == "primary":
            p1.attack(p2, x, y)

