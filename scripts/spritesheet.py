import pygame


# Class for the spritesheets and getting their individual images
class Spritesheet:
    def __init__(self, filename):
        self.sheet = pygame.image.load(filename).convert_alpha()

    def get_sprite(self, x, y, width, height, colorkey = None):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        sprite.set_colorkey(colorkey)
        return sprite
