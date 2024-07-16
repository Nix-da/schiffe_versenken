import math
import os

import numpy as np
from dtw import *
import matplotlib.pyplot as plt

import pygame

from src.GUI_constants import WHITE, BLACK, BLUE

# Initialize Pygame
pygame.init()

# Set the dimensions of the window
window_size = (800, 600)
screen = pygame.display.set_mode(window_size)

# Set the window caption
pygame.display.set_caption("Empty Pygame Window")

title_font = pygame.font.SysFont(None, 24)
title_text = title_font.render("", True, BLACK)
title_text_rect = title_text.get_rect(center=(window_size[0] // 2, 10))  # 10 pixels from the top

gesture_recording = False
gesture_coords = []
gesture = "Gesture: "

rect_list = []

# Main loop
running = True
while running:
    # Fill the screen with white color
    screen.fill(WHITE)
    for rect, color in rect_list:
        pygame.draw.rect(screen, color, rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    if pygame.mouse.get_pressed()[0]:
        gesture_recording = True
        gesture = "Gesture: "
        gesture_coords.append(pygame.mouse.get_pos())
    if gesture_recording and not pygame.mouse.get_pressed()[0]:
        angles = []
        for i in range(1, len(gesture_coords)):
            dx = abs(gesture_coords[i][0] - gesture_coords[i - 1][0])
            dy = abs(gesture_coords[i][1] - gesture_coords[i - 1][1])
            angle = math.degrees(math.atan2(dy, dx))
            angles.append(angle)
        angles = [x for x in angles if x != 0]
        min_val = min(angles)
        max_val = max(angles)
        angles = [(angle - min_val) / (max_val - min_val) for angle in angles]  # Shift and scale to 0-1
        angles = [(angle - 0.5) * 2 for angle in angles]  # Shift and scale to -1-1

        print("Gesture recorded.")

        templates = {}
        num = len(angles)
        # quarter circle clockwise
        templates["circle"] = (np.sin(np.linspace(0, np.pi, num=num)))

        # vertical
        templates["vertical"] = (np.ones(num))

        # horizontal
        templates["horizontal"] = (np.full(num, -1))

        min_distance = np.inf
        detected_gesture = None
        for template_name in templates:
            alignment = dtw(angles, templates[template_name], keep_internals=True)
            alignment.plot(type="threeway")
            print(alignment.distance)
            if alignment.distance < min_distance:
                min_distance = alignment.distance
                detected_gesture = template_name
            plt.show()

        # x direction
        x_direction = None
        if gesture_coords[0][0] < gesture_coords[-1][0]:
            x_direction = "left -> right"
        else:
            x_direction = "right -> left"

        # y direction
        y_direction = None
        if gesture_coords[0][1] < gesture_coords[-1][1]:
            y_direction = "top -> bottom"
        else:
            y_direction = "bottom -> top"

        direction = ""
        if detected_gesture == "horizontal":
            direction = x_direction
        elif detected_gesture == "vertical":
            direction = y_direction
        elif detected_gesture == "circle":
            area = 0.0
            n = len(gesture_coords)
            for i in range(n):
                j = (i + 1) % n
                area += gesture_coords[i][0] * gesture_coords[j][1]
                area -= gesture_coords[j][0] * gesture_coords[i][1]
            area /= 2.0
            if area < 0:
                direction = "clockwise"
            else:
                direction = "counterclockwise"

        gesture = "Gesture: " + detected_gesture + " " + direction

        if detected_gesture == "horizontal" and direction == "left -> right":
            start_coord = gesture_coords[0]
            rect_size = (120, 30)
            rect_color = BLUE
            rect = pygame.Rect(start_coord, rect_size)
            rect_list.append((rect, rect_color))

        elif detected_gesture == "vertical" and direction == "top -> bottom":
            start_coord = gesture_coords[0]
            rect_size = (30, 120)
            rect_color = BLUE
            rect = pygame.Rect(start_coord, rect_size)
            rect_list.append((rect, rect_color))

        elif detected_gesture == "horizontal" and direction == "right -> left":
            start_coord = gesture_coords[0]
            rect_list = [rect for rect in rect_list if not rect[0].collidepoint(start_coord)]

        elif detected_gesture == "vertical" and direction == "bottom -> top":
            start_coord = gesture_coords[0]
            rect_list = [rect for rect in rect_list if not rect[0].collidepoint(start_coord)]

        elif detected_gesture == "circle" and direction == "clockwise":
            start_coord = gesture_coords[0]
            for rect, color in rect_list:
                if rect.collidepoint(start_coord):
                    rect_list.remove((rect, color))
                    # Create a new surface with the same size as the rectangle
                    surface = pygame.Surface((rect.width, rect.height))
                    # Draw the rectangle onto the surface
                    pygame.draw.rect(surface, color, pygame.Rect((0, 0), (rect.width, rect.height)))
                    # Rotate the surface
                    rotated_surface = pygame.transform.rotate(surface, 90)
                    # Get the rectangle of the rotated surface
                    rotated_rect = rotated_surface.get_rect()
                    # Update the position of the rotated rectangle to match the original rectangle
                    rotated_rect.topleft = rect.topleft
                    # Add the rotated rectangle and its color to the list
                    rect_list.append((rotated_rect, color))
                    break

        elif detected_gesture == "circle" and direction == "counterclockwise":
            start_coord = gesture_coords[0]
            for rect, color in rect_list:
                if rect.collidepoint(start_coord):
                    rect_list.remove((rect, color))
                    # Create a new surface with the same size as the rectangle
                    surface = pygame.Surface((rect.width, rect.height))
                    # Draw the rectangle onto the surface
                    pygame.draw.rect(surface, color, pygame.Rect((0, 0), (rect.width, rect.height)))
                    # Rotate the surface
                    rotated_surface = pygame.transform.rotate(surface, -90)  # Rotate 90 degrees counterclockwise
                    # Get the rectangle of the rotated surface
                    rotated_rect = rotated_surface.get_rect()
                    # Update the position of the rotated rectangle to match the original rectangle
                    rotated_rect.topleft = rect.topleft
                    # Add the rotated rectangle and its color to the list
                    rect_list.append((rotated_rect, color))
                    break

        gesture_recording = False
        gesture_coords = []


    # Update the title text with the detected gesture
    title_text = title_font.render(gesture, True, BLACK)
    title_text_rect = title_text.get_rect(center=(window_size[0] // 2, 10))

    # Draw the title text
    screen.blit(title_text, title_text_rect)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
