# Import 'pygame' library to build the game
import pygame
# Import 'icecream' library for debuging purposes
from icecream import ic
import sys
# Import the 'game' and 'multiplayer' files to load the games
from game import car_racing
from game import km_records
from game_multiplayer import multiplayer_car_racing


# Function to display the main interface of the game
def interface():
    # Initialize Pygame and its mixer
    pygame.init()
    pygame.mixer.init()

    pygame.display.set_caption("Main Menu")

    # Load and play background music
    pygame.mixer.music.load('assets/sound/Life_Is_A_Highway.mp3')
    pygame.mixer.music.play(-1)

    # Set resolution and create a window
    res = (720, 720)
    screen = pygame.display.set_mode(res)

    # Define color presets for easy use
    white, yellow, red, green, blue = (255, 255, 255), (255, 255, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255)
    color_light, color_dark, black = (170, 170, 170), (100, 100, 100), (0, 0, 0)

    # Load fonts
    corbelfont, comicsansfont = pygame.font.SysFont('Corbel', 35), pygame.font.SysFont('Comic Sans MS', 50)

    # Center the title text
    title_text = comicsansfont.render('Computation III - Project', True, yellow)
    title_text_rect = title_text.get_rect(center=(res[0] / 2, 60))

    # Create buttons for different game options
    button_texts = ['Car Racing', 'Local Racing', 'Leaderboard', 'Credits', 'Quit']
    buttons = []
    button_y_start = 200
    button_spacing = 70

    # Loop to create buttons with specified texts
    for i, text in enumerate(button_texts):
        text_surface = corbelfont.render(text, True, white)
        x, y, w, h = 260, button_y_start + i * button_spacing, 200, 50
        buttons.append((text_surface, x, y, w, h))

    # Main event loop
    while True:
        mouse = pygame.mouse.get_pos()
        screen.fill(black)

        # Display the title
        screen.blit(title_text, title_text_rect.topleft)

        # Draw buttons and handle hover effect
        for text_surface, x, y, w, h in buttons:
            rect = pygame.Rect(x, y, w, h)
            if rect.collidepoint(mouse):
                pygame.draw.rect(screen, color_light, rect)
            else:
                pygame.draw.rect(screen, color_dark, rect)
            screen.blit(text_surface, (x + 10, y + 10))

        # Event handling for button clicks
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                # Determine which button is clicked and call the corresponding function
                for idx, (_, x, y, w, h) in enumerate(buttons):
                    if x <= mouse[0] <= x + w and y <= mouse[1] <= y + h:
                        if idx == 0:
                            pygame.mixer.music.stop()
                            car_racing(interface, km_records)
                        elif idx == 1:
                            pygame.mixer.music.stop()
                            multiplayer_car_racing(interface, km_records)
                        elif idx == 2:
                            display_kilometer_records(screen, km_records)
                        elif idx == 3:
                            credits_()
                        elif idx == 4:
                            pygame.quit()

        # Update the display
        pygame.display.update()


# Function to display the credits
def credits_():
    # Initialize Pygame and set up the screen
    pygame.init()
    res = (720, 720)
    screen = pygame.display.set_mode(res)

    # Define colors
    white, yellow, red, green, blue, color_light, color_dark, black = (255, 255, 255), (255, 255, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255), (170, 170, 170), (100, 100, 100), (0, 0, 0)

    # Define fonts
    corbelfont = pygame.font.SysFont('Corbel', 35)
    comicsansfont = pygame.font.SysFont('Comic Sans MS', 25)

    # List of credit lines and render them
    credit_lines = [
        'Davide Farinati, dfarinati@novaims.unl.pt',
        'Joao Fonseca, jfonseca@novaims.unl.pt',
        'Liah Rosenfeld, lrosenfeld@novaims.unl.pt',
        'Francisco Magalhães, 20221883@novaims.unl.pt',
        'Gonçalo Farinha, 20221871@novaims.unl.pt',
        'Martim Pires, 20221939@novaims.unl.pt'
    ]
    credit_texts = [comicsansfont.render(line, True, yellow) for line in credit_lines]

    # Create title and back button
    title_text = corbelfont.render('Credits', True, white)
    back_text = corbelfont.render('Back', True, blue)
    back_button = pygame.Rect(280, 650, 160, 50)  # Adjust size and position as needed

    # Main loop for the credits screen
    while True:
        mouse = pygame.mouse.get_pos()
        screen.fill(black)

        # Display the credits title
        screen.blit(title_text, (310, 20))  # Center the title

        # Display each credit line
        for i, text in enumerate(credit_texts):
            screen.blit(text, (screen.get_width() / 2 - text.get_width() / 2, 100 + i * 40))

        # Interactive back button
        if back_button.collidepoint(mouse):
            pygame.draw.rect(screen, color_light, back_button)
        else:
            pygame.draw.rect(screen, color_dark, back_button)
        screen.blit(back_text, (300, 660))  # Adjust position to center the text in the button

        # Event handling for the back button
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN and back_button.collidepoint(mouse):
                return  # Return to the previous menu

        # Update the display
        pygame.display.update()


# Function to display kilometer records
def display_kilometer_records(screen, km_records):
    running = True
    font = pygame.font.SysFont('Arial', 30)
    back_font = pygame.font.SysFont('Corbel', 35)
    back_text = back_font.render('Back', True, (255, 255, 255))
    back_button = pygame.Rect(50, 620, 100, 50)  # Back button dimensions and positions
    button_color = (100, 100, 100)  # Normal button color
    button_hover_color = (170, 170, 170)  # Button color when hovered
    res = (720, 720)

    # Define color presets for easy use
    white, yellow, red, green, blue = (255, 255, 255), (255, 255, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255)

    comicsansfont = pygame.font.SysFont('Comic Sans MS', 25)

    # Center the title text
    title_text = comicsansfont.render('Leaderboard', True, yellow)
    title_text_rect = title_text.get_rect(center=(res[0] / 2, 60))

    # Sort the kilometer records in descending order
    sorted_records = sorted(km_records, reverse=True)

    # Loop to display kilometer records and back button
    while running:
        screen.fill((0, 0, 0))

        # Display the title
        screen.blit(title_text, title_text_rect.topleft)

        # Display sorted kilometer records
        y_offset = 100
        for record in sorted_records:
            record_text = font.render(f"Kilometer Record: {record}", True, (255, 255, 255))
            screen.blit(record_text, (100, y_offset))
            y_offset += 40

        # Interactive back button
        mouse_pos = pygame.mouse.get_pos()
        if back_button.collidepoint(mouse_pos):
            current_button_color = button_hover_color
        else:
            current_button_color = button_color

        # Draw back button
        pygame.draw.rect(screen, current_button_color, back_button)  # Draw button with current color
        screen.blit(back_text, (60, 625))  # Position the text in the button

        # Event handling for the back button
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(mouse_pos):
                    running = False

        # Update the display
        pygame.display.update()
