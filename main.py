import pygame
from pygame import Vector2
from math import cos, sin, radians

# Define the variables
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
    rect = surf.get_frect(center = offset)
    return surf, rect


# function to rotate an object on a specified pivot, without rotating the image itself
def rotate_on_pivot_still(image, angle, pivot, origin):
    offset = pivot + (origin - pivot).rotate(-angle)
    rect = image.get_frect(center = offset)
    return rect


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
        self.acceleration_update_time = pygame.time.get_ticks()
        for i in range(3):
            image_name = f'{self.tank_type}{i}'
            image = reference_dict[image_name]
            self.animation_list.append(image)
        self.tank_image = self.animation_list[self.animation_index]
        self.tank = self.tank_image.get_frect(center = (x, y))
        self.pivot_x = self.tank.center[0]
        self.pivot_y = self.tank.center[1] - 10
        self.turret = Turret(Vector2(self.pivot_x, self.pivot_y), starting_angle = 0)

    # Method to update the positions of the tank and turret
    def update(self, move_left, move_right, rotate_up, rotate_down, charging_launch, dt):

        # accelerate or decelerate the tank based on keys pressed
        if move_left:
            self.decelerate(dt)
        elif move_right:
            self.accelerate(dt)
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
        self.pivot_x = self.tank.center[0]
        self.pivot_y = self.tank.center[1] - 10
        turret_pivot = Vector2(self.pivot_x, self.pivot_y)

        self.turret.update(turret_pivot, rotate_up, rotate_down, dt)

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

    # method to speed up the tank in the left direction
    def decelerate(self, dt):
        if self.speed >= 0:
            self.speed -= self.acceleration * dt * 3
        else:
            if abs(self.speed) < self.max_speed:
                self.speed -= self.acceleration * dt

    # Method to draw the turret and the tank
    def draw(self, surface):
        self.turret.draw(surface)
        surface.blit(self.tank_image, self.tank)

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

    # Method to handle other methods of the turret and the cannonballs
    def update(self, turret_pivot, rotate_up, rotate_down, dt):
        self.move(turret_pivot)
        self.rotate(rotate_up, rotate_down, dt)
        self.cannonball.handle_projectile(dt)
        self.cannonball.update_position(self.turret.center, self.angle)
        self.cannonball.check_if_landed(self.pivot)
        self.cannonball.handle_explosion()

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

    # Method to draw the turret
    def draw(self, surface):
        pygame.draw.line(surface, 'red', (self.pivot.x, 0), (self.pivot.x, SCREEN_HEIGHT))
        pygame.draw.line(surface, 'red', (0, self.pivot.y), (SCREEN_WIDTH, self.pivot.y))
        self.cannonball.draw(surface)
        surface.blit(self.image, self.turret)


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
        self.explosion = Explosion(launch_point)
        self.launched = False
        self.explosion_started = False
        self.explosion_point = launch_point

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
            current_x_position = self.cannonball.centerx
            current_y_position = self.cannonball.centery
            current_x_position += self.horizontal_speed * dt
            current_y_position -= self.vertical_speed * dt
            self.cannonball.center = Vector2(current_x_position, current_y_position)
            # Implement gravity
            self.vertical_speed -= self.g
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
            self.explosion.explosion_started = True
            self.explosion.update_position(self.cannonball.center)
            self.launched = False
            self.launch_speed = self.min_speed

    # Method to implement the explosion of the cannonball
    def handle_explosion(self):
        if self.explosion.explosion_started:
            self.explosion.explode()

    # Method to draw the cannonball on the screen
    def draw(self, surface):
        pygame.draw.line(surface, 'green', (self.cannonball.centerx, 0), (self.cannonball.centerx, SCREEN_HEIGHT))
        pygame.draw.line(surface, 'green', (0, self.cannonball.centery), (SCREEN_WIDTH, self.cannonball.centery))
        if self.launched:
            surface.blit(self.image, self.cannonball)
        self.explosion.draw(surface)


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


# Class that handles the game logic
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE, flags=pygame.SCALED)
        pygame.display.set_caption('Tank Wars')

        # set Framerate
        self.clock = pygame.time.Clock()
        self.FPS = 60
        self.last_time = pygame.time.get_ticks() * 0.001

        # player action variables
        self.tank_moving_left = False
        self.tank_moving_right = False
        self.turret_rotating_up = False
        self.turret_rotating_down = False
        self.charging_launch = False

        # Add the required images to the reference dictionary
        load_image('LeftTank', 'LeftTankTurret', 1)
        for i in range(3):
            load_image('LeftTank', f'LeftTank{i}', 1)
        load_image('LeftTank', 'Cannonball', 1)
        for i in range(1, 9):
            load_image('LeftTank', f'explosion{i}', 3)

        # Create Tank object for the first player
        self.first_tank = Tank('LeftTank', 500, 300)

    # Method to update the tank and its animation
    def update(self, dt):
        self.first_tank.update_animation()
        self.first_tank.update(self.tank_moving_left, self.tank_moving_right,
                               self.turret_rotating_up, self.turret_rotating_down, self.charging_launch, dt)

    # Method to draw the tank on the screen
    def draw(self, surface):
        surface.fill('black')
        self.first_tank.draw(surface)

    # Method that handles the game loop. It is called 60 times each second
    def run(self):
        run = True
        while run:
            # calculate delta time
            current_time = pygame.time.get_ticks() * 0.001
            dt = current_time - self.last_time
            self.last_time = current_time

            # Limit framerate
            self.clock.tick(self.FPS)
            self.update(dt)
            self.draw(self.screen)

            for event in pygame.event.get():
                # quit game
                if event.type == pygame.QUIT:
                    run = False
                # keyboard button presses
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.tank_moving_left = True
                    if event.key == pygame.K_RIGHT:
                        self.tank_moving_right = True
                    if event.key == pygame.K_UP:
                        self.turret_rotating_up = True
                    if event.key == pygame.K_DOWN:
                        self.turret_rotating_down = True
                    if event.key == pygame.K_SPACE:
                        self.charging_launch = True
                    # quit game
                    if event.key == pygame.K_ESCAPE:
                        run = False

                # keyboard button releases
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.tank_moving_left = False
                    if event.key == pygame.K_RIGHT:
                        self.tank_moving_right = False
                    if event.key == pygame.K_UP:
                        self.turret_rotating_up = False
                    if event.key == pygame.K_DOWN:
                        self.turret_rotating_down = False
                    if event.key == pygame.K_SPACE:
                        self.charging_launch = False

            pygame.display.update()
        pygame.quit()


# Run the game
if __name__ == '__main__':
    Game().run()
