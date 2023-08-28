# -*- coding: utf-8 -*-
"""
Created on Fri Aug 25 09:45:48 2023

@author: paulf
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Aug 25 00:38:16 2023

@author: paulf
"""

import pygame
import random
import textwrap
import time

# New function to handle the start screen
def start_screen():
    intro_text = """A technology stack is a set of technologies that are stacked together to build any application.
    It is also known as a technology infrastructure or solutions stack and has become essential for
    building easy-to-maintain, scalable web applications. A technology stack determines the type
    of applications you can build, the level of customizations you can perform, and the resources
    you need to develop your application. It includes all of the hardware and software systems
    that are needed to develop and run a single website, web integration or mobile application."""
    
    max_width = 700  # Maximum width allowed for the text on the start screen
    words = intro_text.split(' ')
    lines = []
    line = ""
    for word in words:
        test_line = line + word + " "
        test_surface = font.render(test_line, True, BLACK)
        if test_surface.get_width() < max_width:
            line += word + " "
        else:
            lines.append(line)
            line = word + " "
    lines.append(line)  # Add the last line

    button_rect = pygame.Rect(350, 450, 100, 50)  # Position and size of the start button
    button_color = GREEN  # Green color for the button

    running = True
    while running:
        screen.fill(WHITE)  # White background

        # Render the title
        title_font = pygame.font.SysFont('Arial', 36)
        title_surface = title_font.render("Technology Stack Puzzle", True, BLACK)
        screen.blit(title_surface, (200, 100))


        # Render the introductory text line by line
        for i, line_text in enumerate(lines):
            intro_surface = font.render(line_text, True, BLACK)
            screen.blit(intro_surface, (50, 150 + 20 * i))  # Render each line 20 pixels apart

        # Draw the start button
        pygame.draw.rect(screen, button_color, button_rect)
        start_text = font.render("Start", True, BLACK)
        screen.blit(start_text, (370, 465))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return False  # Exit the entire game
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):  # Click on the start button
                    return True  # Exit start screen to proceed to the main game

        pygame.display.flip()

# Initialize Pygame
pygame.init()

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Create a window
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Technology Stack Puzzle')

# Define fonts
font = pygame.font.SysFont('Arial', 20)
large_bold_font = pygame.font.SysFont('Arial', 30, bold=True) # Large bold font for objective

# Technology stacks
stacks = ["TensorFlow", "Rasa", "Scikit-Learn", "NLTK", "OpenCV"]

# Objectives and corresponding technology stacks
objectives_and_stacks = [
    ("Build a facial recognition system", "TensorFlow"),
    ("Create a chatbot using natural language processing", "Rasa"),
    ("Develop a recommendation engine for e-commerce", "Scikit-Learn"),
    ("Perform sentiment analysis on social media data", "NLTK"),
    ("Implement real-time object detection", "OpenCV")
]

# Explanations for the correct technology stacks
explanations = {
    "TensorFlow": "TensorFlow is suitable for building facial recognition systems due to its powerful deep learning capabilities.",
    "Rasa": "Rasa is designed for creating conversational AI, making it ideal for natural language processing and chatbot development.",
    "Scikit-Learn": "Scikit-Learn provides simple tools for data mining and data analysis, suitable for recommendation engines.",
    "NLTK": "The Natural Language Toolkit (NLTK) is perfect for sentiment analysis as it provides tools for handling human language data.",
    "OpenCV": "OpenCV is used for real-time object detection due to its comprehensive computer vision libraries and real-time capabilities."
}

# Shuffle the objectives
random.shuffle(objectives_and_stacks)

# Current objective, correct stack, and colors for the shapes
current_index = 0
colors = [BLUE] * 5
explanation_text = ""
next_question = False

# Call the start screen function before entering the main game loop
if not start_screen():
    pygame.quit()
    exit()

# Game loop
start_time = time.time()
running = True
while running:
    # Get the current objective and correct stack
    current_objective, correct_stack = objectives_and_stacks[current_index]

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not next_question:
            x, y = pygame.mouse.get_pos()
            for i, stack in enumerate(stacks):
                if 10 + 150 * i < x < 10 + 150 * i + 140 and 250 < y < 350:
                    if stack == correct_stack:
                        colors[i] = GREEN
                        explanation_text = explanations[correct_stack]
                        next_question = True
                        question_start_time = time.time() # Record the time when the correct answer is found
                    else:
                        colors[i] = RED

    # Clear the screen
    screen.fill(WHITE)

    # Draw the timer
    elapsed_time = int(time.time() - start_time)
    timer_text = font.render(f"Time: {elapsed_time} seconds", True, BLACK)
    screen.blit(timer_text, (650, 10))

    # Draw the objective
    objective_text = large_bold_font.render("Objective: " + current_objective, True, BLACK)
    screen.blit(objective_text, (10, 50)) # Position adjusted to avoid overlap

    # Draw the technology stack header
    header_text = font.render("Choose the Appropriate Technology Stack:", True, BLACK)
    screen.blit(header_text, (10, 150))

    # Draw the technology stack shapes
    for i, stack in enumerate(stacks):
        pygame.draw.rect(screen, colors[i], (10 + 150 * i, 250, 140, 100))
        stack_text = font.render(stack, True, WHITE)
        text_width, _ = font.size(stack) # Get the width of the text
        screen.blit(stack_text, (10 + 150 * i + (140 - text_width) // 2, 275)) # Center the text

    # Draw the explanation with line wrapping
    wrapped_explanation = textwrap.wrap(explanation_text, 60) # Wrap the explanation text into a list of lines
    for i, line in enumerate(wrapped_explanation):
        explanation_surface = font.render(line, True, BLACK)
        screen.blit(explanation_surface, (10, 450 + 20 * i)) # Position adjusted to fit within the screen


    # Update the display
    pygame.display.flip()

    # Handle the delay and transition to the next question
    if next_question and time.time() - question_start_time > 5:
        current_index += 1
        if current_index < len(objectives_and_stacks):
            colors = [BLUE] * 5
            explanation_text = ""
            next_question = False
        else:
            running = False

# Quit Pygame
pygame.quit()
