import pygame
from GUI_constants import *
from ships import Battleship, Cruiser, Destroyer, Submarine

enemy_ships_sunk = []


def draw_legend(screen, legendTitle, ships_array=None):
    if ships_array is None:
        ships_array = enemy_ships_sunk
    legend_font = pygame.font.SysFont(None, 24)
    legend_text = legend_font.render(legendTitle, True, BLACK)
    screen.blit(legend_text, (LEGEND_X + 20, LEGEND_Y))

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

    for ship_name, ship_count in ships_data:
        ship_class = ship_classes[ship_name]
        ship = ship_class()
        length = ship.get_length()

        # Check if the ship class is present in the input ships_array
        if ship_name in ships_array:
            color = GREEN  # Color green if present
            green_count[ship_name] = min(ships_array.count(ship_name), ship_count)
        else:
            color = BLACK  # Otherwise, color black

        # for _ in range(ship_count):
        for _ in range(green_count[ship_name]):
            legend_x_offset = LEGEND_X + 20
            for _ in range(length):
                pygame.draw.rect(screen, color, (legend_x_offset, legend_y_offset, LEGEND_CELL_SIZE, LEGEND_CELL_SIZE))
                legend_x_offset += LEGEND_CELL_SIZE + 5
            legend_y_offset += 30


def mark_as_hit_in_legend(ship):
    enemy_ships_sunk.append(ship)


def draw_grid(screen, game, type):
    if type == "primary":
        block_size = PRIMARY_CELL_SIZE
        x_offset = PRIMARY_GRID_X
        y_offset = PRIMARY_GRID_Y
        DEFAULT_COLOR = WHITE
        SHIP_COLOR = BLUE
        MISS_COLOR = GRAY
        HIT_COLOR = RED
        SUNK_COLOR = GREEN
    else:
        block_size = SECONDARY_CELL_SIZE
        x_offset = SECONDARY_GRID_X
        y_offset = SECONDARY_GRID_Y
        DEFAULT_COLOR = WHITE
        SHIP_COLOR = BLUE
        MISS_COLOR = GRAY
        HIT_COLOR = YELLOW
        SUNK_COLOR = RED

    # generate a 10x10 grid
    for x in range(GRID_SIZE):
        x_position = x * block_size + x_offset
        for y in range(GRID_SIZE):
            y_position = y * block_size + y_offset
            rect = pygame.Rect(x_position, y_position, block_size, block_size)

            # color the cell according to the states cell
            if game[x][y] == 0:
                pygame.draw.rect(screen, DEFAULT_COLOR, rect)
            if game[x][y] == 1:
                pygame.draw.rect(screen, SHIP_COLOR, rect)
            if game[x][y] == 2:
                pygame.draw.rect(screen, HIT_COLOR, rect)
            if game[x][y] == 3:
                pygame.draw.rect(screen, SUNK_COLOR, rect)
            if game[x][y] == 4:
                pygame.draw.rect(screen, MISS_COLOR, rect)

            pygame.draw.rect(screen, BLACK, rect, 1)

    # make the outline bold
    rect = pygame.Rect(x_offset, y_offset, block_size * GRID_SIZE, block_size * GRID_SIZE)
    pygame.draw.rect(screen, BLACK, rect, 3)

    if type == "primary":
        font = pygame.font.SysFont(None, 24)
        # Write numbers
        for x in range(GRID_SIZE):
            x_position = x * block_size + x_offset + block_size // 2
            text = font.render(str(x + 1), True, BLACK)
            text_rect = text.get_rect(center=(x_position, y_offset // 2 + (PRIMARY_GRID_Y // 2 - 12)))
            screen.blit(text, text_rect)

        # Write letters
        for y in range(GRID_SIZE):
            y_position = y * block_size + y_offset + block_size // 2
            text = font.render(chr(y + 65), True, BLACK)
            text_rect = text.get_rect(center=(x_offset // 2 + (PRIMARY_GRID_X // 2 - 12), y_position))
            screen.blit(text, text_rect)


def get_cell(x, y):
    type = None
    if PRIMARY_GRID_X <= x <= PRIMARY_GRID_X + PRIMARY_CELL_SIZE * GRID_SIZE:
        if PRIMARY_GRID_Y <= y <= PRIMARY_GRID_Y + PRIMARY_CELL_SIZE * GRID_SIZE:
            type = "primary"
    if SECONDARY_GRID_X <= x <= SECONDARY_GRID_X + SECONDARY_CELL_SIZE * GRID_SIZE:
        if SECONDARY_GRID_Y <= y <= SECONDARY_GRID_Y + SECONDARY_CELL_SIZE * GRID_SIZE:
            type = "secondary"
    if LEGEND_X + 20 <= x <= LEGEND_X + (LEGEND_CELL_SIZE + 5) * 5 + 20:
        if LEGEND_Y + 30 <= y <= LEGEND_Y + (LEGEND_CELL_SIZE + 10) * 10 + 30:
            type = "legend"

    if type == "primary":
        x_block_size = PRIMARY_CELL_SIZE
        y_block_size = PRIMARY_CELL_SIZE
        x_offset = PRIMARY_GRID_X
        y_offset = PRIMARY_GRID_Y
    elif type == "secondary":
        x_block_size = SECONDARY_CELL_SIZE
        y_block_size = SECONDARY_CELL_SIZE
        x_offset = SECONDARY_GRID_X
        y_offset = SECONDARY_GRID_Y
    elif type == "legend":
        x_block_size = LEGEND_CELL_SIZE + 5
        y_block_size = LEGEND_CELL_SIZE + 10
        x_offset = LEGEND_X + 20
        y_offset = LEGEND_Y + 30
    else:
        return 0, 0, None


    x = (x - x_offset) // x_block_size
    y = (y - y_offset) // y_block_size
    return x, y, type
