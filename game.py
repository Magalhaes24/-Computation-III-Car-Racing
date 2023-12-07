# Import necessary libraries and modules
import pygame, random  # Pygame for game development, random for randomness in game events
from icecream import ic  # Icecream library for debugging
from car import Car  # Import Car class from car module
from power_up import Invincibility, Slowing, SpeedBoost, DoubleKilometers, Shrinking  # Import power-up classes


km_records = []  # List to store kilometer records
def game_over_screen(screen, km, callback, kilometer_records):
    # Set up font and colors
    font = pygame.font.SysFont('Arial', 50)
    text_color = (255, 0, 0)  # Red color for the text
    button_color = (0, 255, 0)  # Green color for the button
    button_text_color = (255, 255, 255)  # White color for the button text

    # Create 'Game Over' text
    text = font.render('Game Over', True, text_color)
    text_rect = text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2 - 100))

    # Create 'Kilometers' text
    km_text = font.render(f'Kilometers: {int(km)}', True, text_color)
    km_text_rect = km_text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2))

    # Create 'Main Menu' button
    button_rect = pygame.Rect(screen.get_width() / 2 - 100, screen.get_height() / 2 + 100, 200, 50)
    button_text = font.render('Main Menu', True, button_text_color)
    button_text_rect = button_text.get_rect(center=button_rect.center)


    # Create 'Play Again' button (with additional spacing)
    play_again_button_rect = pygame.Rect(screen.get_width() / 2 - 100, screen.get_height() / 2 + 160, 200, 50)
    play_again_button_text = font.render('Play Again', True, button_text_color)
    play_again_button_text_rect = play_again_button_text.get_rect(center=play_again_button_rect.center)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    running = False
                    callback()  # Call the callback function to go to the main menu
                elif play_again_button_rect.collidepoint(event.pos):
                    running = False
                    car_racing(callback, kilometer_records)  # Call car_racing with the correct argument


        # Drawing
        screen.fill((0, 0, 0))  # Fill the screen with black
        screen.blit(text, text_rect)
        screen.blit(km_text, km_text_rect)  # Display the kilometers
        pygame.draw.rect(screen, button_color, button_rect)
        screen.blit(button_text, button_text_rect)
        pygame.draw.rect(screen, button_color, play_again_button_rect)  # Draw 'Play Again' button
        screen.blit(play_again_button_text, play_again_button_text_rect)  # Draw text on 'Play Again' button

        pygame.display.flip()  # Update the display

def car_racing(callback, kilometer_records):
    pygame.init()
    pygame.mixer.init()

    collision_sound = pygame.mixer.Sound('assets/sound/kachow.mp3')
    background_sound = pygame.mixer.Sound('assets/sound/Route_66.mp3')
    background_sound.play(-1)

    game_over = False  # Initialize the game_over variable

    GREEN = (20, 255, 140)
    GREY = (210, 210, 210)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    PURPLE = (255, 0, 255)
    YELLOW = (255, 255, 0)
    CYAN = (0, 255, 255)
    BLUE = (100, 100, 255)

    speed = 1 # Initial speed of the player's car
    colorList = (RED, GREEN, PURPLE, YELLOW, CYAN, BLUE)
    imgList = ['assets/img/f1.png', 'assets/img/truck.png', 'assets/img/ecar.png', 'assets/img/f4.png'] # List of image filenames for different cars

    SCREENWIDTH = 800
    SCREENHEIGHT = 600

    size = (SCREENWIDTH, SCREENHEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Car Racing")

    clock_start_time = pygame.time.get_ticks()  # Initialize clock start time

    clock_duration = 4000  # Duration for the clock to fill (4 seconds)

    clock_filled = 0  # Current filled state of the clock (0 to 1)
    clock_rect_width = 20  # Width of the clock bar
    clock_rect_height = 100  # Height of the clock bar

    clock_rect_x = SCREENWIDTH - clock_rect_width - 10  # Position the clock on the right side
    clock_rect_y = 50  # Vertical position of the clock

    power_up_collected = False

    # This will be a list that will contain all the sprites we intend to use in our game.
    all_sprites_list = pygame.sprite.Group()

    playerCar = Car('assets/img/car.png', 40, 70, 70)
    playerCar.rect.x = 170
    playerCar.rect.y = SCREENHEIGHT - 100

    car1 = Car('assets/img/f1.png', 55, 110, random.randint(50, 100))
    car1.rect.x = 65
    car1.rect.y = -100

    car2 = Car('assets/img/truck.png', 70, 140, random.randint(50, 100))
    car2.rect.x = 157
    car2.rect.y = -600

    car3 = Car('assets/img/ecar.png', 60, 100, random.randint(50, 100))
    car3.rect.x = 265
    car3.rect.y = -300

    car4 = Car('assets/img/truck.png', 65, 130, random.randint(50, 100))
    car4.rect.x = 360
    car4.rect.y = -900

    # Kilometer counter initialization
    km_counter = 0
    km_font = pygame.font.SysFont('Arial', 30)

    # Add the car to the list of objects
    all_sprites_list.add(playerCar)
    all_sprites_list.add(car1)
    all_sprites_list.add(car2)
    all_sprites_list.add(car3)
    all_sprites_list.add(car4)

    all_coming_cars = pygame.sprite.Group()
    all_coming_cars.add(car1)
    all_coming_cars.add(car2)
    all_coming_cars.add(car3)
    all_coming_cars.add(car4)

    # Create a list to hold all power-ups
    all_power_ups = pygame.sprite.Group()

    # Define road boundaries
    LEFT_ROAD_BOUNDARY_1 = 40
    RIGHT_ROAD_BOUNDARY_1 = 440
    LANE_WIDTH = 100

    def spawn_power_up():
        power_up_type = random.choice([Invincibility, Slowing, SpeedBoost, DoubleKilometers, Shrinking])
        power_up = power_up_type(20)  # Pass only the radius
        power_up.spawn(SCREENWIDTH, SCREENHEIGHT, 400, 40)
        all_power_ups.add(power_up)

        print(f"Power-up {power_up_type.__name__} added at position {power_up.rect.x}, {power_up.rect.y}")

    def control_car(car, keys, left_key, right_key, up_key, down_key, left_boundary, right_boundary):
        if keys[left_key] and car.rect.x > left_boundary:
            car.moveLeft(5)
        if keys[right_key] and car.rect.x + car.width < right_boundary:
            car.moveRight(5)
        if keys[up_key]:
            return 0.05  # Increase speed
        if keys[down_key]:
            return -0.05  # Decrease speed
        return 0

    # Allowing the user to close the window...
    carryOn = True
    clock = pygame.time.Clock()

    while carryOn:


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                carryOn = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    playerCar.moveRight(10)

        keys = pygame.key.get_pressed()

        # Control Player 1 Car
        speed_change = control_car(playerCar, keys, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN,
                                   LEFT_ROAD_BOUNDARY_1, RIGHT_ROAD_BOUNDARY_1)
        speed += speed_change

        # Inside the game loop in car_racing function
        if random.randint(1, 500) == 1:
            spawn_power_up()

        # Move power-ups down the screen
        for power_up in all_power_ups:
            power_up.moveDown(5)  # You can adjust the speed as needed

        # Check for power-up collisions
        power_up_collision_list = pygame.sprite.spritecollide(playerCar, all_power_ups, True)
        for power_up in power_up_collision_list:
            power_up_collected = True
            power_up.affect_player(playerCar)
            power_up.affect_traffic(all_coming_cars)
            print(f"Added the {power_up.__class__.__name__} effect to the player")
            collision_sound.play()
            clock_start_time = pygame.time.get_ticks()

        # Game Logic
        for car in all_coming_cars:
            car.moveForward(speed)
            if car.rect.y > SCREENHEIGHT:
                car.changeSpeed(random.randint(50, 100))
                car.changeImage(random.choice(imgList))  # Change the image
                car.rect.y = -200

            car_collision_list = pygame.sprite.spritecollide(playerCar, all_coming_cars, False)
            for car in car_collision_list:
                if not playerCar.invincible:  # Check if player is not invincible
                    car.kill()
                    print("Car crash!")
                    game_over = True

        if not playerCar.Shrinking:
            # Resize the car back to its original size
            original_width, original_height = playerCar.width, playerCar.height
            playerCar.image = pygame.transform.scale(playerCar.image, (original_width, original_height))
            playerCar.rect = playerCar.image.get_rect(center=playerCar.rect.center)

        if game_over:
            background_sound.stop()
            kilometer_records.append(int(km_counter))  # Add km_counter to the list
            game_over_screen(screen, km_counter, callback, kilometer_records)
            break

        all_sprites_list.update()

        # Update the kilometer counter
        km_increment = speed / 20
        if playerCar.double_km_active:
            km_increment *= 2 # Double the kilometers if the power-up is active
        km_counter += km_increment

        # Drawing on Screen
        screen.fill(GREEN)

        # Draw The Road
        pygame.draw.rect(screen, GREY, [40, 0, 400, SCREENHEIGHT])
        # Draw Line painting on the road
        pygame.draw.line(screen, WHITE, [140, 0], [140, SCREENHEIGHT], 5)
        # Draw Line painting on the road
        pygame.draw.line(screen, WHITE, [240, 0], [240, SCREENHEIGHT], 5)
        # Draw Line painting on the road
        pygame.draw.line(screen, WHITE, [340, 0], [340, SCREENHEIGHT], 5)

        # Now let's draw all the sprites in one go. (For now we only have 1 sprite!)
        all_sprites_list.draw(screen)

        # Draw power-ups
        all_power_ups.draw(screen)

        # Display the kilometer counter
        if playerCar.double_km_active:
            km_text = km_font.render(f"Kilometers: {int(km_counter)} x {int(km_increment * 20)}", True, WHITE)
        else:
            km_text = km_font.render(f"Kilometers: {int(km_counter)}", True, WHITE)

        screen.blit(km_text, (10, 10))  # Position the text on the screen

        if power_up_collected:
            elapsed_time = pygame.time.get_ticks() - clock_start_time
            clock_filled = min(elapsed_time / clock_duration, 1)  # Calculate the fill percentage

            if elapsed_time >= clock_duration:
                playerCar.invincible = False
                playerCar.double_km_active = False
                playerCar.Shrinking = False
                power_up_collected = False
                playerCar.changeImage('assets/img/car.png')

            # Draw the background of the clock bar
            pygame.draw.rect(screen, GREY, [clock_rect_x, clock_rect_y, clock_rect_width, clock_rect_height])

            # Draw the filled part of the clock bar
            filled_height = clock_filled * clock_rect_height
            pygame.draw.rect(screen, RED,
                             [clock_rect_x, clock_rect_y + clock_rect_height - filled_height, clock_rect_width,
                              filled_height])

        # Refresh Screen
        pygame.display.flip()

        # Number of frames per second e.g. 60
        clock.tick(60)

    pygame.quit()
