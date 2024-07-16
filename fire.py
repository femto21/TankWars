from math import cos, radians, sin

import pygame
from pygame import Vector2

from scripts.config import reference_dict
from scripts.spritesheet import Spritesheet


# Class for the launch fire animation
class Fire(pygame.sprite.Sprite):
    def __init__(self, position, angle):
        pygame.sprite.Sprite.__init__(self)
        self.angle = angle
        self.spritesheet = Spritesheet('Images/LeftTank/Sparks-Sheet.png')
        self.index = 0
        self.images = []
        sprite_row = 0
        sprite_column = 0
        for i in range(7):
            image = self.spritesheet.get_sprite(sprite_column * 96, sprite_row * 96, 96, 96)
            self.images.append(image)
            sprite_column += 1
            if sprite_column > 2:
                sprite_column = 0
                sprite_row += 1
        self.image = self.images[self.index]
        self.position = position
        self.offset = Vector2(60 * cos(radians(self.angle)), -60 * sin(radians(self.angle)))
        self.origin = self.position + self.offset
        self.rect = self.image.get_frect(center = self.origin)
        self.counter = 0
        self.firing = False

    # Method to update the position where the animation will happen as the tank moves and the turret rotates
    def update_position(self, turret_center, angle):
        self.position = turret_center
        self.angle = angle
        self.offset = Vector2(60 * cos(radians(self.angle)), -60 * sin(radians(self.angle)))
        self.origin = self.position + self.offset
        self.rect.center = self.origin

    # Method to initiate the animation when a shot is fired
    def fire(self):
        self.firing = True
        fire_speed = 4

        # Update fire animation
        self.counter += 1
        if self.counter >= fire_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        # if the animation is complete, reset animation index
        if self.index >= len(self.images) - 1 and self.counter >= fire_speed:
            self.reset()

    # Method to reset the fire animation to its about-to-be state
    def reset(self):
        self.index = 0
        self.counter = 0
        self.firing = False

    def draw(self, surface):
        if self.firing:
            surface.blit(self.image, self.rect)
