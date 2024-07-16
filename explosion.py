import pygame

from scripts.config import reference_dict


# Class for the cannonball explosion
class Explosion(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for i in range(1, 9):
            self.images.append(reference_dict[f'explosion{i}'])
        self.index = 0
        self.image = self.images[self.index]
        self.explosion = self.image.get_frect(center = position)
        self.counter = 0
        self.explosion_started = False

    # Method to make the about-to-be explosion follow the cannonball
    def update_position(self, position):
        self.explosion.center = position

    # Method to initiate and handle the explosion
    def explode(self):
        explosion_speed = 4

        # Update explosion animation
        self.counter += 1
        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        # if the animation is complete, reset animation index
        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.reset()

    # Method to reset the explosion to its about-to-be state
    def reset(self):
        self.explosion_started = False
        self.index = 0
        self.counter = 0

    # Method to draw the explosion
    def draw(self, surface):
        if self.explosion_started:
            surface.blit(self.image, self.explosion)