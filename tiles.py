import pygame

from scripts.config import NUMBER_OF_COLUMNS, TILE_WIDTH, TILE_HEIGHT, NUMBER_OF_ROWS
from scripts.spritesheet import Spritesheet


# Class for the surface tiles
class Tiles(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        tiles_spritesheet = Spritesheet('Images/Tiles.png')
        grass = tiles_spritesheet.get_sprite(112, 59, 16, 20, 'black')
        dirt = tiles_spritesheet.get_sprite(16, 46, 16, 16)
        self.grass = pygame.transform.scale(grass, (grass.get_width() * 3, grass.get_height() * 3))
        self.dirt = pygame.transform.scale(dirt, (48, 48))

    # Method to draw the tiles
    def draw_tiles(self, surface):
        for i in range(NUMBER_OF_COLUMNS):
            for j in range(9, NUMBER_OF_ROWS):
                surface.blit(self.dirt, (i * TILE_WIDTH, j * TILE_HEIGHT))
            surface.blit(self.grass, (i * TILE_WIDTH, 9 * TILE_HEIGHT))
