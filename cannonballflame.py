import math

import pygame

from scripts.config import rotate_on_pivot


# Class for the cannonball flame effect
class CannonballFlame(pygame.sprite.Sprite):
    def __init__(self, pivot, launch_angle):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.angle = launch_angle
        self.upload_images()
        self.image = self.images[self.index]
        self.images_orig = self.images
        self.image_orig = self.images_orig[self.index]
        self.rect = self.image.get_frect(center = pivot)
        self.burn = False

    def update(self, pivot, position, horizontal_speed, vertical_speed):
        self.burn = True
        self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]
        self.image_orig = self.images_orig[self.index]
        self.rect = self.image.get_frect(center = position)
        angle = math.degrees(math.atan(vertical_speed / horizontal_speed))
        self.image, self.rect = rotate_on_pivot(self.image_orig, angle, pivot, position)

    def upload_images(self):
        for i in range(60):
            if abs(self.angle) < 90:
                image = pygame.image.load(f'Images/CannonballEffect2/1_{i}.png')
            else:
                image = pygame.image.load(f'Images/CannonballEffect2/1_{i}.png')
                image = pygame.transform.flip(image, True, False)
            image = pygame.transform.scale_by(image, 2)
            self.images.append(image)

    def draw(self, surface):
        if self.burn:
            surface.blit(self.image, self.rect)
