import pygame
from pygame import Vector2

from scripts.config import reference_dict
from smoke import Smoke
from turret import Turret


# Class for the Tanks
class Tank(pygame.sprite.Sprite):
    max_speed = 2.5
    acceleration = 1

    def __init__(self, tank_type, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.tank_type = tank_type
        self.animation_list = []
        self.animation_index = 0
        self.animation_update_time = pygame.time.get_ticks()
        self.speed = 0
        for i in range(3):
            image_name = f'{self.tank_type}{i}'
            image = reference_dict[image_name]
            self.animation_list.append(image)
        self.tank_image = self.animation_list[self.animation_index]
        self.tank = self.tank_image.get_frect(center = (x, y))
        if tank_type == 'LeftTank':
            self.pivot_x = self.tank.centerx
            self.pivot_y = self.tank.centery - 10
        elif tank_type == 'RightTank':
            self.pivot_x = self.tank.centerx - 10
            self.pivot_y = self.tank.centery - 15
        self.turret = Turret(Vector2(self.pivot_x, self.pivot_y), tank_type)
        self.smoke_group = pygame.sprite.Group()
        self.smoke_cooldown = 0

    # Method to update the positions of the tank and turret
    def update(self, move_left, move_right, rotate_up, rotate_down, charging_launch, dt):

        # accelerate or decelerate the tank based on keys pressed
        if move_left:
            self.decelerate(dt)
            self.smoke_cooldown += 1
        elif move_right:
            self.accelerate(dt)
            self.smoke_cooldown += 1
        # if no keys are pressed, friction slows down the tank
        else:
            if self.speed != 0:
                if self.speed > 0:
                    self.speed -= self.acceleration * dt * 4
                elif self.speed < 0:
                    self.speed += self.acceleration * dt * 4

                if 0.1 > self.speed > -0.1:
                    self.speed = 0

        # update rectangle position
        self.tank.x = self.tank.x + self.speed

        # update turret position
        if self.tank_type == 'LeftTank':
            self.pivot_x = self.tank.centerx
            self.pivot_y = self.tank.centery - 10
        elif self.tank_type == 'RightTank':
            self.pivot_x = self.tank.centerx - 10
            self.pivot_y = self.tank.centery - 15
        turret_pivot = Vector2(self.pivot_x, self.pivot_y)

        self.turret.update(turret_pivot, rotate_up, rotate_down, dt)
        self.smoke_group.update()

        # If the cannon-ball launch is ready, check if the player is charging it
        if self.turret.launch_ready:
            if charging_launch:
                self.turret.charge_launch(dt)
                self.turret.cannonball.check_max_speed()
                self.turret.charged = True
            else:
                if self.turret.charged:
                    self.turret.launch()

    # method to speed up the tank in the right direction
    def accelerate(self, dt):
        if self.speed <= 0:
            self.speed += self.acceleration * dt * 6
        else:
            if abs(self.speed) < self.max_speed:
                self.speed += self.acceleration * dt
        if self.smoke_cooldown % 10 == 0:
            smoke = Smoke(self.speed, self.tank.centerx - 20, self.tank.centery - 2)
            self.smoke_group.add(smoke)

    # method to speed up the tank in the left direction
    def decelerate(self, dt):
        if self.speed >= 0:
            self.speed -= self.acceleration * dt * 3
        else:
            if abs(self.speed) < self.max_speed:
                self.speed -= self.acceleration * dt
        if self.smoke_cooldown % 10 == 0:
            smoke = Smoke(self.speed, self.tank.centerx + 20, self.tank.centery - 2)
            self.smoke_group.add(smoke)

    # Method to draw the turret and the tank
    def draw(self, surface):
        self.turret.draw(surface)
        surface.blit(self.tank_image, self.tank)
        self.smoke_group.draw(surface)

    # Method to update the current animation of the tank (excluding the turret)
    def update_animation(self):
        if self.speed != 0:
            ANIMATION_COOLDOWN = 100/abs(self.speed)

            # update image depending on current frame
            self.tank_image = self.animation_list[self.animation_index]

            # check if enough time has passed since the last update
            if pygame.time.get_ticks() - self.animation_update_time > ANIMATION_COOLDOWN:
                self.animation_update_time = pygame.time.get_ticks()

                if self.speed > 0:
                    self.animation_index += 1
                if self.speed < 0:
                    self.animation_index -= 1

            # if animation has run out, reset back to the start
            if self.speed > 0:
                if self.animation_index >= len(self.animation_list):
                    self.animation_index = 0
            if self.speed < 0:
                if self.animation_index < 0:
                    self.animation_index = len(self.animation_list) - 1
