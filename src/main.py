import pygame

# Initialize the pygame
pygame.init()

# Set the dimensions of the window
window_size = (500, 600)
screen = pygame.display.set_mode(window_size)

# Set the window name
pygame.display.set_caption('Schiffe versenken')

# Set the window icon
icon = pygame.image.load('./assets/icon.png')
pygame.display.set_icon(icon)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# Quit pygame
pygame.quit()