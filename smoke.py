import pygame

from scripts.spritesheet import Spritesheet


# Class for the smoke created when tank moves
class Smoke(pygame.sprite.Sprite):
    def __init__(self, speed, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.index = 0
        self.images = []
        self.upload_images()
        self.image = self.images[self.index]
        self.rect = self.image.get_frect(center = (x, y))
        if speed > 0:
            self.smoke_direction = 'left'
        elif speed < 0:
            self.smoke_direction = 'right'
        self.counter = 0

    def update(self):
        smoke_speed = 2
        # Update fire animation
        self.counter += 1
        if self.counter >= smoke_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        # if the animation is complete, reset animation index
        if self.index >= len(self.images) - 1 and self.counter >= smoke_speed:
            self.kill()

    # Method to add the images to the images list
    def upload_images(self):
        spritesheet = Spritesheet('Images/Smoke2-Sheet.png')
        sprite_row = 0
        sprite_column = 0
        for i in range(40):
            image = spritesheet.get_sprite(sprite_column * 150, sprite_row * 150, 150, 150, 'black')
            image = pygame.transform.scale(image, (96, 96))
            self.images.append(image)
            sprite_column += 1
            if sprite_column > 4:
                sprite_column = 0
                sprite_row += 1
