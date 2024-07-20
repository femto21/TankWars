import pygame

from scripts.config import reference_dict, SCREEN_WIDTH, SCREEN_HEIGHT
from scripts.spritesheet import Spritesheet


# Class for drawing the background canvas
class Background(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        green_tree_spritesheet = Spritesheet('Images/Green-Tree.png')
        red_tree_spritesheet = Spritesheet('Images/Red-Tree.png')
        golden_tree_spritesheet = Spritesheet('Images/Golden-Tree.png')
        yellow_tree_spritesheet = Spritesheet('Images/Yellow-Tree.png')
        bg_trees_spritesheet = Spritesheet('Images/Background-Trees.png')
        tiles_spritesheet = Spritesheet('Images/Tiles.png')
        self.background_image = reference_dict['Background']
        self.bg_tree1 = bg_trees_spritesheet.get_sprite(0, 0, 96, 256, 'black')
        self.bg_tree2 = bg_trees_spritesheet.get_sprite(112, 0, 96, 256, 'black')
        self.bg_tree3 = bg_trees_spritesheet.get_sprite(224, 0, 96, 256, 'black')
        self.tree0 = green_tree_spritesheet.get_sprite(890, 0, 110, 370, 'black')
        self.tree1 = green_tree_spritesheet.get_sprite(900, 390, 110, 320, 'black')
        self.tree2 = green_tree_spritesheet.get_sprite(0, 390, 110, 320, 'black')
        self.tree3 = golden_tree_spritesheet.get_sprite(0, 390, 110, 320, 'black')
        self.tree4 = green_tree_spritesheet.get_sprite(670, 0, 110, 370, 'black')
        self.tree5 = yellow_tree_spritesheet.get_sprite(0, 0, 110, 370, 'black')
        self.tree6 = green_tree_spritesheet.get_sprite(0, 720, 90, 210, 'black')
        self.tree7 = yellow_tree_spritesheet.get_sprite(0, 940, 90, 150, 'black')
        self.tree8 = red_tree_spritesheet.get_sprite(0, 720, 90, 210, 'black')
        self.tree9 = green_tree_spritesheet.get_sprite(0, 940, 90, 150, 'black')
        self.tree10 = golden_tree_spritesheet.get_sprite(670, 1090, 80, 110, 'black')
        self.bush1 = tiles_spritesheet.get_sprite(274, 0, 397, 47, 'black')
        self.bush2 = tiles_spritesheet.get_sprite(274, 47, 397, 47, 'black')
        self.rock1 = tiles_spritesheet.get_sprite(159, 335, 80, 33, 'black')
        self.rock2 = tiles_spritesheet.get_sprite(0, 335, 80, 33, 'black')
        self.depth = 69

    # Method to draw the background canvas
    def draw_canvas(self, surface):
        self.background_image = pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        surface.blit(self.background_image, (0, -200))
        for i in range(6):
            surface.blit(self.bg_tree1, (i*196 - 20, 114 + self.depth))
            surface.blit(self.bg_tree2, (i*196 + 76, 114 + self.depth))
            surface.blit(self.bg_tree3, (i*196 + 172, 114 + self.depth))
        for i in range(10):
            surface.blit(self.tree0, (-30 + i*120, 0 + self.depth))
        for i in range(6):
            surface.blit(self.tree1, (30 + i*200, 55 + self.depth))
        for i in range(10):
            surface.blit(self.tree2, (50 + i*120, 55 + self.depth))
        for i in range(7):
            surface.blit(self.tree3, (-30 + i*200, 55 + self.depth))
        for i in range(5):
            surface.blit(self.tree4, (i*300, 0 + self.depth))
        for i in range(4):
            surface.blit(self.tree5, (60 + i*320, 0 + self.depth))
        for i in range(7):
            surface.blit(self.tree6, (-20 + i*180, 160 + self.depth))
        for i in range(6):
            surface.blit(self.tree7, (70 + i*220, 220 + self.depth))
        for i in range(5):
            surface.blit(self.tree8, (80 + i*250, 160 + self.depth))
        for i in range(11):
            surface.blit(self.tree9, (10 + i*110, 220 + self.depth))
        for i in range(8):
            surface.blit(self.tree10, (40 + i*150, 258 + self.depth))
        for i in range(5):
            surface.blit(self.bush1, (100 + i*200, 322 + self.depth))
        for i in range(4):
            surface.blit(self.bush2, (i*350, 322 + self.depth))
        for i in range(7):
            surface.blit(self.rock1, (10 + i*240, 335 + self.depth))
        for i in range(4):
            surface.blit(self.rock2, (50 + i*330, 335 + self.depth))
        for i in range(4):
            surface.blit(self.rock1, (80 + i*330, 335 + self.depth))
