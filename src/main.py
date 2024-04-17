import pygame

def draw_grid(screen, size=30, x_offset=50, y_offset=50):
    # Set the size of the grid block
    block_size = size
    grid_size = 10

    # generate a 10x10 grid
    for x in range(x_offset, x_offset + grid_size * block_size, block_size):
        for y in range(y_offset, y_offset + grid_size * block_size, block_size):
            rect = pygame.Rect(x, y, block_size, block_size)
            pygame.draw.rect(screen, (0.5, 0.5, 0.5), rect, 1)

    # make the outline bold
    rect = pygame.Rect(x_offset, y_offset, block_size * grid_size, block_size * grid_size)
    pygame.draw.rect(screen, (0.5, 0.5, 0.5), rect, 3)


# Initialize the pygame
pygame.init()

# Set the dimensions of the window
window_size = (500, 600)
screen = pygame.display.set_mode(window_size)
screen.fill((255, 255, 255))

# Set the window name
pygame.display.set_caption('Schiffe versenken')

# Set the window icon
icon = pygame.image.load('./assets/icon.png')
pygame.display.set_icon(icon)

# Main loop
running = True
while running:
    screen.fill((255, 255, 255))
    draw_grid(screen)
    draw_grid(screen, 15, 125, 380)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()

# Quit pygame
pygame.quit()