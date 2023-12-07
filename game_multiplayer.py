import pygame, random
from icecream import ic
from car import Car
from power_up import Invincibility, Slowing, SpeedBoost
from main import main

duration = 4000

def game_over_screen(screen, km, callback, winner_name, kilometer_records):
    # Set up font and colors
    font = pygame.font.SysFont('Arial', 50)
    text_color = (255, 0, 0)  # Red color for the text
    button_color = (0, 255, 0)  # Green color for the button
    button_text_color = (255, 255, 255)  # White color for the button text

    # Create 'Game Over' text
    text = font.render('Game Over', True, text_color)
    text_rect = text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2 - 100))

    # Create 'Winner' text
    winner_text = font.render(f'Winner: {winner_name}', True, text_color)
    winner_text_rect = winner_text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2 - 50))

    # Create 'Kilometers' text
    km_text = font.render(f'Kilometers: {int(km)}', True, text_color)
    km_text_rect = km_text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2))

    # Create 'Main Menu' button
    button_rect = pygame.Rect(screen.get_width() / 2 - 100, screen.get_height() / 2 + 100, 200, 50)
    button_text = font.render('Main Menu', True, button_text_color)
    button_text_rect = button_text.get_rect(center=button_rect.center)

    # Create 'Play Again' button
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
                    callback()  # Return to the main menu
                elif play_again_button_rect.collidepoint(event.pos):
                    running = False
                    multiplayer_car_racing(callback, kilometer_records)  # Restart the game


        # Drawing
        screen.fill((0, 0, 0))  # Fill the screen with black
        screen.blit(text, text_rect)
        screen.blit(winner_text, winner_text_rect)  # Display the winner's name
        screen.blit(km_text, km_text_rect)  # Display the kilometers
        pygame.draw.rect(screen, button_color, button_rect)
        screen.blit(button_text, button_text_rect)
        pygame.draw.rect(screen, button_color, play_again_button_rect)
        screen.blit(play_again_button_text, play_again_button_text_rect)

        pygame.display.flip()  # Update the display


def multiplayer_car_racing(callback, kilometer_records):
    pygame.init()
    pygame.mixer.init()

    collision_sound = pygame.mixer.Sound('assets/sound/kachow.mp3')
    background_sound = pygame.mixer.Sound('assets/sound/Route_66.mp3')
    background_sound.play(-1)

    game_over = False  # Initialize the game_over variable

    GREEN = (20, 255, 140)
    GREY = (210, 210 ,210)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    PURPLE = (255, 0, 255)
    YELLOW = (255, 255, 0)
    CYAN = (0, 255, 255)
    BLUE = (100, 100, 255)

    speed = 1
    speed2 = 1
    colorList = (RED, GREEN, PURPLE, YELLOW, CYAN, BLUE)
    imgList = ['assets/img/f1.png', 'assets/img/truck.png', 'assets/img/ecar.png', 'assets/img/f4.png']


    SCREENWIDTH=925
    SCREENHEIGHT=600

    size = (SCREENWIDTH, SCREENHEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Car Racing")

    clock_start_time = pygame.time.get_ticks()  # Initialize clock start time
    clock_start_time2 = pygame.time.get_ticks()  # Initialize clock start time

    clock_duration = 4000  # Duration for the clock to fill (4 seconds)

    clock_filled = 0  # Current filled state of the clock (0 to 1)
    clock_rect_width = 20  # Width of the clock bar
    clock_rect_height = 100  # Height of the clock bar

    # Clock positions for Player 1 and Player 2
    clock_rect_x1 = 50  # Position for Player 1's clock
    clock_rect_y1 = 50
    clock_rect_x2 = SCREENWIDTH - 70  # Position for Player 2's clock
    clock_rect_y2 = 50

    power_up_collected = False
    power_up_collected2 = False

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

    # Initialize the second player car
    playerCar2 = Car('assets/img/car.png', 40, 70, 70)  # Use a different image or color for the second car
    playerCar2.rect.x = 440 + 170  # Place it on the second road
    playerCar2.rect.y = SCREENHEIGHT - 100

    car5 = Car('assets/img/f1.png', 55, 110, random.randint(50,100))
    car5.rect.x = 65 + 440
    car5.rect.y = -100

    car6 = Car('assets/img/truck.png', 70, 140, random.randint(50,100))
    car6.rect.x = 157 + 440
    car6.rect.y = -600

    car7 = Car('assets/img/ecar.png', 60, 100, random.randint(50,100))
    car7.rect.x = 265 + 440
    car7.rect.y = -300

    car8 = Car('assets/img/truck.png', 65, 130, random.randint(50,100))
    car8.rect.x = 360 + 440
    car8.rect.y = -900

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

    # Add the car to the list of objects
    all_sprites_list.add(playerCar2)
    all_sprites_list.add(car5)
    all_sprites_list.add(car6)
    all_sprites_list.add(car7)
    all_sprites_list.add(car8)

    all_coming_cars_2 = pygame.sprite.Group()
    all_coming_cars_2.add(car5)
    all_coming_cars_2.add(car6)
    all_coming_cars_2.add(car7)
    all_coming_cars_2.add(car8)

    # Create a list to hold all power-ups
    all_power_ups = pygame.sprite.Group()
    # Create a second list to hold power-ups for the second road
    all_power_ups_2 = pygame.sprite.Group()

    # Define road boundaries
    LEFT_ROAD_BOUNDARY_1 = 40
    RIGHT_ROAD_BOUNDARY_1 = 440
    LEFT_ROAD_BOUNDARY_2 = 480  # Adjust as per the second road's position
    RIGHT_ROAD_BOUNDARY_2 = SCREENWIDTH - 40

    def spawn_power_up():
        power_up_type = random.choice([Invincibility, Slowing, SpeedBoost])
        power_up = power_up_type(20)  # Pass only the radius

        # Randomly choose the road for the power-up to spawn
        if random.choice([True, False]):
            # Spawn on the left road
            spawn_x = random.randint(LEFT_ROAD_BOUNDARY_1, RIGHT_ROAD_BOUNDARY_1 - power_up.radius * 2)
            power_up.rect.x = spawn_x
            power_up.rect.y = random.randint(-100, -20)  # Adjust y-coordinate as needed
            all_power_ups.add(power_up)
        else:
            # Spawn on the right road
            spawn_x = random.randint(LEFT_ROAD_BOUNDARY_2, RIGHT_ROAD_BOUNDARY_2 - power_up.radius * 2)
            power_up.rect.x = spawn_x
            power_up.rect.y = random.randint(-100, -20)  # Adjust y-coordinate as needed
            all_power_ups_2.add(power_up)

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
    clock=pygame.time.Clock()

    while carryOn:

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                carryOn=False
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_x:
                     playerCar.moveRight(10)

        keys = pygame.key.get_pressed()

        # Control Player 1 Car with arrow keys
        speed_change = control_car(playerCar, keys, pygame.K_a, pygame.K_d, pygame.K_o, pygame.K_l,
                                   LEFT_ROAD_BOUNDARY_1, RIGHT_ROAD_BOUNDARY_1)
        speed += speed_change

        # Control Player 2 Car with WASD keys
        speed_change = control_car(playerCar2, keys, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_o, pygame.K_l,
                                   LEFT_ROAD_BOUNDARY_2, RIGHT_ROAD_BOUNDARY_2)
        speed2 += speed_change

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
            print(f"Added the {power_up.__class__.__name__} effect to the player 1")
            # Play the collision sound effect
            collision_sound.play()
            clock_start_time = pygame.time.get_ticks()

        for power_up2 in all_power_ups_2:
            power_up2.moveDown(5)  # You can adjust the speed as needed

        power_up_collision_list2 = pygame.sprite.spritecollide(playerCar2, all_power_ups_2, True)
        for power_up2 in power_up_collision_list2:
            power_up_collected2 = True
            power_up2.affect_player(playerCar2)
            power_up2.affect_traffic(all_coming_cars_2)
            print(f"Added the {power_up2.__class__.__name__} effect to the player 2")
            # Play the collision sound effect
            collision_sound.play()
            clock_start_time2 = pygame.time.get_ticks()

        player1_collided = False
        player2_collided = False

        #Game Logic
        for car in all_coming_cars:
            car.moveForward(speed)
            if car.rect.y > SCREENHEIGHT:
                car.changeSpeed(random.randint(50,100))
                car.changeImage(random.choice(imgList))  # Change the image
                car.rect.y = -200

            car_collision_list = pygame.sprite.spritecollide(playerCar, all_coming_cars, False)
            for car in car_collision_list:
                if not playerCar.invincible:  # Check if player is not invincible
                    print("Car crash with player 1!")
                    car.kill()
                    player1_collided = True
                    game_over = True

        for car2 in all_coming_cars_2:
            car2.moveForward(speed2)
            if car2.rect.y > SCREENHEIGHT:
                car2.changeSpeed(random.randint(50, 100))
                car2.changeImage(random.choice(imgList))
                car2.rect.y = -200

            car_collision_list2 = pygame.sprite.spritecollide(playerCar2, all_coming_cars_2, False)
            for car2 in car_collision_list2:
                if not playerCar2.invincible:  # Check if playerCar2 is not invincible
                    print("Car crash with player 2!")
                    car2.kill()
                    player2_collided = True
                    game_over = True

        if not playerCar.Shrinking:
            # Resize the car back to its original size
            original_width, original_height = playerCar.width, playerCar.height
            playerCar.image = pygame.transform.scale(playerCar.image, (original_width, original_height))
            playerCar.rect = playerCar.image.get_rect(center=playerCar.rect.center)

        if not playerCar2.Shrinking:
            # Resize the car back to its original size
            original_width, original_height = playerCar2.width, playerCar2.height
            playerCar2.image = pygame.transform.scale(playerCar2.image, (original_width, original_height))
            playerCar2.rect = playerCar2.image.get_rect(center=playerCar2.rect.center)

        # Inside the game loop where game_over is set to True
        if game_over:
            background_sound.stop()
            kilometer_records.append(int(km_counter))  # Add km_counter to the list

            # Determine the winner
            if player1_collided and not player2_collided:
                winner = "Player 2"
            elif not player1_collided and player2_collided:
                winner = "Player 1"
            else:
                winner = "No Winner"  # In case both collided or neither collided

            game_over_screen(screen, km_counter, callback, winner, kilometer_records)
            break

        all_sprites_list.update()

        # Update the kilometer counter
        km_increment = speed / 20
        if playerCar.double_km_active:
            km_increment *= 2  # Double the kilometers if the power-up is active
        if playerCar2.double_km_active:
            km_increment *= 2  # Double the kilometers if the power-up is active
        km_counter += km_increment

        # Update the kilometer counter
        km_counter += speed / 20  # Increment the counter based on the speed

        # Drawing on Screen
        screen.fill(GREEN)

        # Constants for road dimensions
        road_width = 400
        left_margin = 40
        road_marking_width = 5
        road_separator_width = 40  # Width of the space between the two roads

        # Calculate the x position of the second road
        second_road_x = left_margin + road_width + road_separator_width

        # Draw the first road
        pygame.draw.rect(screen, GREY, [left_margin, 0, road_width, SCREENHEIGHT])
        # Draw line painting on the first road
        for i in range(1, 4):
            pygame.draw.line(screen, WHITE, [left_margin + i * road_width // 4, 0],
                             [left_margin + i * road_width // 4, SCREENHEIGHT], road_marking_width)

        # Draw the second road
        pygame.draw.rect(screen, GREY, [second_road_x, 0, road_width, SCREENHEIGHT])
        # Draw line painting on the second road
        for i in range(1, 4):
            pygame.draw.line(screen, WHITE, [second_road_x + i * road_width // 4, 0],
                             [second_road_x + i * road_width // 4, SCREENHEIGHT], road_marking_width)

        # Now let's draw all the sprites in one go. (For now we only have 1 sprite!)
        all_sprites_list.draw(screen)

        # Draw power-ups
        all_power_ups_2.draw(screen)
        all_power_ups.draw(screen)

        # Display the kilometer counter
        if playerCar.double_km_active:
            km_text = km_font.render(f"Kilometers: {int(km_counter)} x {int(km_increment * 20)}", True, WHITE)
        else:
            km_text = km_font.render(f"Kilometers: {int(km_counter)}", True, WHITE)

        if playerCar2.double_km_active:
            km_text = km_font.render(f"Kilometers: {int(km_counter)} x {int(km_increment * 20)}", True, WHITE)
        else:
            km_text = km_font.render(f"Kilometers: {int(km_counter)}", True, WHITE)

        screen.blit(km_text, (10, 10))  # Position the text on the screen

        # Update and draw clock for Player 1
        if power_up_collected:
            elapsed_time = pygame.time.get_ticks() - clock_start_time
            clock_filled = min(elapsed_time / clock_duration, 1)

            if elapsed_time >= clock_duration:
                # Reset power-up effects for Player 1
                playerCar.invincible = False
                playerCar.double_km_active = False
                playerCar.Shooting = False  # if 'Shooting' is a power-up effect
                power_up_collected = False
                playerCar.changeImage('assets/img/car.png')  # Reset image if changed by power-up

            # Draw Player 1's clock
            pygame.draw.rect(screen, GREY, [clock_rect_x1, clock_rect_y1, clock_rect_width, clock_rect_height])
            filled_height = clock_filled * clock_rect_height
            pygame.draw.rect(screen, RED,
                             [clock_rect_x1, clock_rect_y1 + clock_rect_height - filled_height, clock_rect_width,
                              filled_height])

        # Update and draw clock for Player 2
        if power_up_collected2:
            elapsed_time2 = pygame.time.get_ticks() - clock_start_time2
            clock_filled2 = min(elapsed_time2 / clock_duration, 1)

            if elapsed_time2 >= clock_duration:
                # Reset power-up effects for Player 2
                playerCar2.invincible = False
                playerCar2.double_km_active = False
                playerCar2.Shooting = False  # if 'Shooting' is a power-up effect
                power_up_collected2 = False
                playerCar2.changeImage('assets/img/car.png')  # Reset image if changed by power-up

            # Draw Player 2's clock
            pygame.draw.rect(screen, GREY, [clock_rect_x2, clock_rect_y2, clock_rect_width, clock_rect_height])
            filled_height2 = clock_filled2 * clock_rect_height
            pygame.draw.rect(screen, BLUE,
                             [clock_rect_x2, clock_rect_y2 + clock_rect_height - filled_height2, clock_rect_width,
                              filled_height2])

        # Display the kilometer counter
        km_text = km_font.render(f"Kilometers: {int(km_counter)}", True, WHITE)
        screen.blit(km_text, (10, 10))  # Position the text on the screen

        # Refresh Screen
        pygame.display.flip()

        # Number of frames per second e.g. 60
        clock.tick(60)

    pygame.quit()