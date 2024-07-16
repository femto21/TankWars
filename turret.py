from math import cos, radians, sin

import pygame
from pygame import Vector2

from cannonball import Cannonball
from fire import Fire
from scripts.config import reference_dict, rotate_on_pivot, SCREEN_HEIGHT, SCREEN_WIDTH


# Class for the Tank Turrets
class Turret(pygame.sprite.Sprite):
    # Distance between the turret and the point of pivot
    pivot_distance = 24

    def __init__(self, pivot, starting_angle = 10):
        pygame.sprite.Sprite.__init__(self)
        self.pivot = pivot
        self.angle = 10
        self.offset = Vector2()
        self.offset.from_polar((self.pivot_distance, -starting_angle))
        self.pos = pivot + self.offset
        self.image_orig = reference_dict['LeftTankTurret']
        self.image = self.image_orig
        self.turret = self.image.get_frect(center=self.pos)
        self.cannonball_offset = Vector2(20 * cos(radians(self.angle)), -20 * sin(radians(self.angle)))
        self.cannonball_origin = self.turret.center + self.cannonball_offset
        self.cannonball = Cannonball(self.cannonball_origin, self.angle)
        self.launch_ready = True
        self.charged = False
        self.fire_animation = Fire(self.turret.center, self.angle)
        self.fire = False

    # Method to handle other methods of the turret and the cannonballs
    def update(self, turret_pivot, rotate_up, rotate_down, dt):
        self.move(turret_pivot)
        self.rotate(rotate_up, rotate_down, dt)
        self.cannonball.handle_projectile(dt)
        self.cannonball.update_position(self.turret.center, self.angle)
        self.cannonball.check_if_landed(self.pivot)
        self.cannonball.handle_explosion()
        self.fire_animation.update_position(self.turret.center, self.angle)
        self.handle_fire_animation()

    # Method to handle the rotation of the turret
    def rotate(self, rotating_up, rotating_down, dt):
        if rotating_up:
            if self.angle < 65:
                self.angle += 30 * dt
        if rotating_down:
            if self.angle > 10:
                self.angle -= 30 * dt

        self.image, self.turret = rotate_on_pivot(self.image_orig, self.angle, self.pivot, self.pos)

    # Method to move the turret's pivot point
    def move(self, pivot):
        self.pivot = Vector2(pivot)
        self.pos = self.pivot + self.offset

    # Method to increase the cannonball launch speed if the user is charging it
    def charge_launch(self, dt):
        if not self.cannonball.launched:
            self.cannonball.launch_speed += 100 * dt
            self.cannonball.update_speed()

    # Method to launch the cannonball
    def launch(self):
        self.cannonball.launch_angle = self.angle
        self.cannonball.launched = True
        self.charged = False
        self.fire = True

    def handle_fire_animation(self):
        if self.fire:
            self.fire_animation.fire()
            if not self.fire_animation.firing:
                self.fire = False

    # Method to draw the turret
    def draw(self, surface):
        pygame.draw.line(surface, 'red', (self.pivot.x, 0), (self.pivot.x, SCREEN_HEIGHT))
        pygame.draw.line(surface, 'red', (0, self.pivot.y), (SCREEN_WIDTH, self.pivot.y))
        self.cannonball.draw(surface)
        self.fire_animation.draw(surface)
        surface.blit(self.image, self.turret)
