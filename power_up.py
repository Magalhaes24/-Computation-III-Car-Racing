# Import 'pygame' library to build the game
import pygame
# Import 'icecream' library for debuging purposes
from icecream import ic
from abc import ABC, abstractmethod
# Import 'random' and 'time' for functions and features
import random
import time

YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)


class PowerUp(pygame.sprite.Sprite, ABC):
    DEFAULT_DURATION = 4000  # Default duration in milliseconds

    def __init__(self, color, radius, duration=DEFAULT_DURATION):
        super().__init__()
        self.image = pygame.Surface([radius * 2, radius * 2], pygame.SRCALPHA)
        self.color = color
        self.radius = radius
        self.effect_duration = duration
        self.start_time = None
        pygame.draw.circle(self.image, self.color, (radius, radius), radius)
        self.rect = self.image.get_rect()

    @abstractmethod
    def affect_player(self, player):
        pass

    @abstractmethod
    def affect_traffic(self, traffic):
        pass

    def start_effect(self, current_time):
        self.start_time = current_time

    def decrease_duration(self, current_time):
        if self.start_time is not None:
            elapsed_time = current_time - self.start_time
            self.effect_duration -= elapsed_time
            self.start_time = current_time  # Update start_time for the next tick
            if self.effect_duration <= 0:
                self.end_effect()

    def end_effect(self):
        print('The effecet has ended')
        self.kill()  # Remove the power-up

    def update(self, current_time):
        if self.start_time is not None:
            elapsed_time = current_time - self.start_time

            if elapsed_time >= self.effect_duration:  # Check if 4 seconds have passed
                self.end_effect()

    def spawn(self, screen_width, screen_height, road_width, road_left_edge_x):
        # Calculate the range of x-coordinates where power-ups can spawn on the road
        road_right_edge_x = road_left_edge_x + road_width
        spawnable_x_positions = range(road_left_edge_x + self.radius, road_right_edge_x - self.radius)

        # Choose a random position within the road boundaries
        self.rect.x = random.choice(spawnable_x_positions)
        self.rect.y = random.randint(-150, -50)  # Spawn off-screen

    def moveDown(self, speed):
        self.rect.y += speed


class Invincibility(PowerUp):

    def __init__(self, radius):
        super().__init__(YELLOW, radius, 4000)  # Custom duration for Invincibility

    def affect_player(self, player):
        player.invincible = True
        self.start_effect(pygame.time.get_ticks())
        self.player = player  # Keep a reference to the player
        self.player.changeImage('car_i.png')

    def affect_traffic(self, traffic):
        pass  # No effect on traffic


class Slowing(PowerUp):
    def __init__(self, radius):
        super().__init__(CYAN, radius, 3000)  # Example: 3000 milliseconds for Slowing

    def affect_player(self, player):
        pass  # No effect on player

    def affect_traffic(self, traffic):
        for car in traffic:
            car.speed *= 0.5  # Halve the speed of traffic cars


class SpeedBoost(PowerUp):
    def __init__(self, radius):
        super().__init__(RED, radius, 5000)  # Example: 5000 milliseconds for SpeedBoost

    def affect_player(self, player):
        player.speed *= 1.5  # Increase the player's speed

    def affect_traffic(self, traffic):
        pass  # No effect on traffic


class DoubleKilometers(PowerUp):
    def __init__(self, radius):
        super().__init__(WHITE, radius, 4000)  # Duration for Double Kilometers

    def affect_player(self, player):
        player.double_km_active = True
        self.start_effect(pygame.time.get_ticks())

    def affect_traffic(self, traffic):
        pass  # No effect on traffic


class Shrinking(PowerUp):
    def __init__(self, radius):
        super().__init__(GREEN, radius, 4000)  # Duration for Shrinking

    def affect_player(self, player):
        self.original_size = player.image.get_size()  # Store the original size
        new_size = (self.original_size[0] * 0.5, self.original_size[1] * 0.5)  # Reduce size by 50%
        player.image = pygame.transform.scale(player.image, new_size)
        player.rect = player.image.get_rect(center=player.rect.center)  # Update rect to new size
        self.start_effect(pygame.time.get_ticks())
        self.player = player  # Keep a reference to the player
        player.Shrinking = True

    def affect_traffic(self, traffic):
        pass  # No effect on traffic

