import pygame
from GUI_constants import *
from ships import Battleship, Cruiser, Destroyer, Submarine


enemy_ships_sunk = []

def draw_legend(screen, legendTitle):
    legend_font = pygame.font.SysFont(None, 24)
    legend_text = legend_font.render(legendTitle, True, BLACK)
    screen.blit(legend_text, (LEGEND_X, LEGEND_Y))

    legend_y_offset = LEGEND_Y + 30

    # Define ship names and corresponding classes
    ship_classes = {
        "Battleship": Battleship,
        "Cruiser": Cruiser,
        "Destroyer": Destroyer,
        "Submarine": Submarine
    }

    # Specify how often certain ship class should be displayed in legend
    ships_data = [("Battleship", 1), ("Cruiser", 2), ("Destroyer", 3), ("Submarine", 4)]

    green_count = {ship_name: 0 for ship_name, _ in ships_data}

    black_count = {ship_name: ship_count for ship_name, ship_count in ships_data}

    for ship_name, ship_count in ships_data:
        ship_class = ship_classes[ship_name]
        ship = ship_class()
        length = ship.get_length()

        # Check if the ship class is present in enemy_ships_sunk
        if ship_name in enemy_ships_sunk:
            green_count[ship_name] = min(enemy_ships_sunk.count(ship_name), ship_count)
            black_count[ship_name] -= green_count[ship_name]

        # total count of legend items for a certain ship class
        total_count = green_count[ship_name] + black_count[ship_name]

        for _ in range(total_count):
            # Determine the color of ships in legend based on the count
            color = GREEN if _ < green_count[ship_name] else BLACK

            legend_x_offset = LEGEND_X + 20
            for _ in range(length):
                pygame.draw.rect(screen, color, (legend_x_offset, legend_y_offset, LEGEND_CELL_SIZE, LEGEND_CELL_SIZE))
                legend_x_offset += LEGEND_CELL_SIZE + 5
            legend_y_offset += 30


def mark_as_hit_in_legend(enemy_ship):
    enemy_ships_sunk.append(enemy_ship)
    print(enemy_ships_sunk)


def draw_grid(screen, game, type):
    if type == "primary":
        block_size = PRIMARY_CELL_SIZE
        x_offset = PRIMARY_GRID_X
        y_offset = PRIMARY_GRID_Y
    else:
        block_size = SECONDARY_CELL_SIZE
        x_offset = SECONDARY_GRID_X
        y_offset = SECONDARY_GRID_Y

    GRID_SIZE = 10

    # generate a 10x10 grid
    for x in range(GRID_SIZE):
        x_position = x * block_size + x_offset
        for y in range(GRID_SIZE):
            y_position = y * block_size + y_offset
            rect = pygame.Rect(x_position, y_position, block_size, block_size)

            # color the cell according to the states cell
            if game[x][y] == 0:
                pygame.draw.rect(screen, WHITE, rect)
            if game[x][y] == 1:
                pygame.draw.rect(screen, BLUE, rect)
            if game[x][y] == 2:
                pygame.draw.rect(screen, RED, rect)
            if game[x][y] == 3:
                pygame.draw.rect(screen, GREEN, rect)

            pygame.draw.rect(screen, BLACK, rect, 1)

    # make the outline bold
    rect = pygame.Rect(x_offset, y_offset, block_size * GRID_SIZE, block_size * GRID_SIZE)
    pygame.draw.rect(screen, BLACK, rect, 3)

def get_cell(x, y):
    type = None
    if PRIMARY_GRID_X <= x <= PRIMARY_GRID_X + PRIMARY_CELL_SIZE * GRID_SIZE:
        if PRIMARY_GRID_Y <= y <= PRIMARY_GRID_Y + PRIMARY_CELL_SIZE * GRID_SIZE:
            type = "primary"
    if SECONDARY_GRID_X <= x <= SECONDARY_GRID_X + SECONDARY_CELL_SIZE * GRID_SIZE:
        if SECONDARY_GRID_Y <= y <= SECONDARY_GRID_Y + SECONDARY_CELL_SIZE * GRID_SIZE:
            type = "secondary"

    if type == "primary":
        block_size = PRIMARY_CELL_SIZE
        x_offset = PRIMARY_GRID_X
        y_offset = PRIMARY_GRID_Y
    elif type == "secondary":
        block_size = SECONDARY_CELL_SIZE
        x_offset = SECONDARY_GRID_X
        y_offset = SECONDARY_GRID_Y
    else:
        return 0, 0, None

    x = (x - x_offset) // block_size
    y = (y - y_offset) // block_size
    return x, y, type


