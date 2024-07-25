import pygame
from pygame import Vector2

from scripts.config import rotate_on_pivot
from scripts.spritesheet import Spritesheet


# Class for the launch fire animation
class Fire(pygame.sprite.Sprite):
    fire_distance = 90

    def __init__(self, tank_type, pivot, angle):
        pygame.sprite.Sprite.__init__(self)
        self.index = 0
        self.images = []
        self.tank_type = tank_type
        self.upload_images()
        self.pivot = pivot
        self.offset = Vector2()
        self.offset.from_polar((self.fire_distance, -angle))
        if tank_type == 'LeftTank':
            self.angle = angle - 10
        elif tank_type == 'RightTank':
            self.angle = angle + 14
        self.position = self.pivot - self.offset
        self.image = self.images[self.index]
        self.images_orig = self.images
        self.image_orig = self.images_orig[self.index]
        self.rect = self.image.get_frect(center = self.position)
        self.counter = 0
        self.firing = False

    # Method to move the fire animation's pivot point
    def move(self, pivot):
        self.pivot = Vector2(pivot)
        if self.tank_type == 'LeftTank':
            self.position = self.pivot + self.offset
        elif self.tank_type == 'RightTank':
            self.position = self.pivot - self.offset

    # Method to have the image rotated and ready in place
    def rotate(self, angle):
        if self.tank_type == 'LeftTank':
            self.angle = angle - 10
        elif self.tank_type == 'RightTank':
            self.angle = angle + 14
        self.image, self.rect = rotate_on_pivot(self.image_orig, self.angle,
                                                self.pivot, self.position)
        if self.tank_type == 'LeftTank':
            self.image = pygame.transform.rotate(self.image, -30)
        elif self.tank_type == 'RightTank':
            self.image = pygame.transform.rotate(self.image, 30)
        self.rect = self.image.get_frect(center = self.rect.center)

    # Method to initiate the animation when a shot is fired
    def fire(self):
        if self.firing:
            fire_speed = 4
            # Update fire animation
            self.counter += 1
            if self.counter >= fire_speed and self.index < len(self.images) - 1:
                self.counter = 0
                self.index += 1
                self.image = self.images[self.index]
                self.image_orig = self.images_orig[self.index]
                self.image, self.rect = rotate_on_pivot(self.image_orig, self.angle,
                                                        self.pivot, self.position)
                if self.tank_type == 'LeftTank':
                    self.image = pygame.transform.rotate(self.image, -30)
                elif self.tank_type == 'RightTank':
                    self.image = pygame.transform.rotate(self.image, 30)
                self.rect = self.image.get_frect(center = self.rect.center)

            # if the animation is complete, reset animation index
            if self.index >= len(self.images) - 1 and self.counter >= fire_speed:
                self.reset()

    # Method to reset the fire animation to its about-to-be state
    def reset(self):
        self.index = 0
        self.counter = 0
        self.firing = False

    # Method to add the images to the images list
    def upload_images(self):
        spritesheet = Spritesheet('Images/Sparks-Sheet.png')
        sprite_row = 0
        sprite_column = 0
        for i in range(7):
            image = spritesheet.get_sprite(sprite_column * 96, sprite_row * 96, 96, 96, 'black')
            if self.tank_type == 'RightTank':
                image = pygame.transform.flip(image, False, True)
            self.images.append(image)
            sprite_column += 1
            if sprite_column > 2:
                sprite_column = 0
                sprite_row += 1

    # Method to draw the animation
    def draw(self, surface):
        if self.firing:
            surface.blit(self.image, self.rect)
