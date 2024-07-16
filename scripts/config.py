# Define the variables
import pygame
from pygame import Vector2

BLOCK_WIDTH = 48
BLOCK_HEIGHT = 48
NUMBER_OF_COLUMNS = 24
NUMBER_OF_ROWS = 14
SCREEN_WIDTH = BLOCK_WIDTH * NUMBER_OF_COLUMNS
SCREEN_HEIGHT = BLOCK_HEIGHT * NUMBER_OF_ROWS
SCREEN_SIZE = Vector2(SCREEN_WIDTH, SCREEN_HEIGHT)
reference_dict = {}


# Method to load the required images into the reference dictionary
def load_image(tank_type, image_name, scale, colorKey=None):
    image = pygame.image.load(f'Images/{tank_type}/{image_name}.png')
    width = image.get_width() * scale
    height = image.get_height() * scale

    image = pygame.transform.scale(image, (width, height))

    if colorKey is not None:
        image.set_colorkey(colorKey)

    reference_dict[image_name] = image


# function to rotate an object on a specified pivot (2D vector)
def rotate_on_pivot(image, angle, pivot, origin):
    surf = pygame.transform.rotate(image, angle)
    offset = pivot + (origin - pivot).rotate(-angle)
    rect = surf.get_frect(center=offset)
    return surf, rect


# function to rotate an object on a specified pivot, without rotating the image itself
def rotate_on_pivot_still(image, angle, pivot, origin):
    offset = pivot + (origin - pivot).rotate(-angle)
    rect = image.get_frect(center=offset)
    return rect
