from math import radians, cos, sin

import pygame
from pygame import Vector2

from cannonballflame import CannonballFlame
from explosion import Explosion
from scripts.config import reference_dict, SCREEN_WIDTH, SCREEN_HEIGHT


# Class for the Cannonballs that are launched from the turret
class Cannonball(pygame.sprite.Sprite):
    # Minimum and maximum speeds of the cannon-ball
    min_speed = 250
    max_speed = 500
    # acceleration due to gravity
    g = 5

    def __init__(self, launch_point, launch_angle):
        pygame.sprite.Sprite.__init__(self)
        self.launch_angle = launch_angle
        self.image = reference_dict['Cannonball']
        self.cannonball = self.image.get_frect(center = launch_point)
        self.launch_speed = self.min_speed
        self.horizontal_speed = self.launch_speed * cos(radians(self.launch_angle))
        self.vertical_speed = self.launch_speed * sin(radians(self.launch_angle))
        self.flame_effect = CannonballFlame(self.cannonball.center)
        self.explosion = Explosion(launch_point)
        self.launched = False
        self.explosion_started = False
        self.explosion_point = launch_point
        self.next_shot_ready = True

    # update the position of the cannonball while it's loaded in the turret
    def update_position(self, position, angle):
        if not self.launched:
            self.cannonball.center = position
            cannonball_offset = Vector2(20 * cos(radians(angle)), -20 * sin(radians(angle)))
            self.cannonball.center += cannonball_offset
            self.launch_angle = angle

    # update the position of the cannonball after it's launched
    def handle_projectile(self, dt):
        if self.launched:
            self.next_shot_ready = False
            current_x_position = self.cannonball.centerx
            current_y_position = self.cannonball.centery
            current_x_position += self.horizontal_speed * dt
            current_y_position -= self.vertical_speed * dt
            self.cannonball.center = Vector2(current_x_position, current_y_position)
            # Implement gravity
            self.vertical_speed -= self.g
            self.flame_effect.update(Vector2(self.cannonball.centerx, self.cannonball.centery),
                                     Vector2(self.cannonball.centerx - 16, self.cannonball.centery - 12),
                                     self.horizontal_speed, self.vertical_speed)
            self.explosion.update(self.cannonball.center)

    # Method to update the horizontal and vertical speed components of the turret while it is loaded in the turret
    def update_speed(self):
        self.horizontal_speed = self.launch_speed * cos(radians(self.launch_angle))
        self.vertical_speed = self.launch_speed * sin(radians(self.launch_angle))

    # Method to check that the cannonball isn't charged beyond the max speed
    def check_max_speed(self):
        if self.launch_speed > self.max_speed:
            self.launch_speed = self.max_speed

    # Method to check if the cannonball has landed
    def check_if_landed(self, pivot):
        if self.cannonball.centery > pivot.y + 30:
            self.next_shot_ready = True
            self.explosion.explosion_started = True
            self.explosion.update_position(self.cannonball.center)
            self.launched = False
            self.launch_speed = self.min_speed
            self.flame_effect.burn = False

    # Method to implement the explosion of the cannonball
    def handle_explosion(self):
        if self.explosion.explosion_started:
            self.explosion.explode()

    # Method to draw the cannonball on the screen
    def draw(self, surface):
        pygame.draw.line(surface, 'green', (self.cannonball.centerx, 0), (self.cannonball.centerx, SCREEN_HEIGHT))
        pygame.draw.line(surface, 'green', (0, self.cannonball.centery), (SCREEN_WIDTH, self.cannonball.centery))
        if self.launched:
            self.flame_effect.draw(surface)
            surface.blit(self.image, self.cannonball)
        self.explosion.draw(surface)
