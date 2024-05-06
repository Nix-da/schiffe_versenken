import pygame
from GUI_constants import *
from ships import Battleship, Cruiser, Destroyer, Submarine
from grid_logic import draw_grid, draw_legend, get_cell
from player import Player

primary_own = 0

def display_place_ships_screen(screen, p1):
    # draw two grids
    #if primary_own == 0:
        draw_grid(screen, p1.grid, "primary")
       # draw_grid(screen, p1.enemy_grid, "secondary")
    # else:
    #     draw_grid(screen, p1.enemy_grid, "primary")
    #     draw_grid(screen, p1.grid, "secondary")

    # draw legend
    #draw_legend(screen, "place your ships")


def place_ship(eventButton, p1, p2):
    # get position of the mouse on the screen
    pos = pygame.mouse.get_pos()
    if eventButton == 1:
        # convert the screen position to grid position
        x, y, type = get_cell(pos[0], pos[1])
        print(get_cell(pos[0], pos[1]))

        # if the position is on the primary grid, attack the enemy
        if type == "primary":
            p1.attack(p2, x, y)