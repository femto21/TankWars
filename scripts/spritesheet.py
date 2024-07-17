import pygame


class Spritesheet:
    def __init__(self, filename):
        self.sheet = pygame.image.load(filename)

    def get_sprite(self, x, y, width, height, colorkey):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        sprite.set_colorkey(colorkey)
        return sprite
