import pygame
from pygame import Vector2, FRect

# Define the variables
BLOCK_WIDTH = 48
BLOCK_HEIGHT = 48
NUMBER_OF_COLUMNS = 24
NUMBER_OF_ROWS = 14
SCREEN_WIDTH = BLOCK_WIDTH * NUMBER_OF_COLUMNS
SCREEN_HEIGHT = BLOCK_HEIGHT * NUMBER_OF_ROWS
SCREEN_SIZE = Vector2(SCREEN_WIDTH, SCREEN_HEIGHT)
reference_dict = {}


# function to rotate an object on a specified pivot (2D vector)
def rotate_on_pivot(image, angle, pivot, origin):
    surf = pygame.transform.rotate(image, angle)
    offset = pivot + (origin - pivot).rotate(-angle)
    rect = surf.get_frect(center = offset)
    return surf, rect


# Class for the Tanks
class Tank(pygame.sprite.Sprite):
    max_speed = 2.5
    acceleration = 0.1

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
        self.tank = self.tank_image.get_frect()
        self.tank.center = (x, y)
        self.pivot_x = self.tank.center[0]
        self.pivot_y = self.tank.center[1] - 10
        self.turret = Turret(Vector2(self.pivot_x, self.pivot_y), starting_angle = 0)

    # Method to update the positions of the tank and turret
    def update(self, move_left, move_right, rotate_up, rotate_down):
        # the cooldown before each time the tank is accelerated/decelerated
        ACCELERATION_COOLDOWN = 100

        # accelerate or decelerate the tank based on keys pressed
        if pygame.time.get_ticks() - self.acceleration_update_time > ACCELERATION_COOLDOWN:
            self.acceleration_update_time = pygame.time.get_ticks()

            if move_left:
                self.decelerate()
            elif move_right:
                self.accelerate()
            # if no keys are pressed, friction slows down the tank
            else:

                if self.speed != 0:
                    if self.speed > 0:
                        self.speed -= self.acceleration * 4
                    elif self.speed < 0:
                        self.speed += self.acceleration * 4

                    if 0.2 > self.speed > -0.2:
                        self.speed = 0
                        
        # update rectangle position
        self.tank.x = self.tank.x + self.speed

        # update turret position
        self.pivot_x = self.tank.center[0]
        self.pivot_y = self.tank.center[1] - 10
        turret_pivot = Vector2(self.pivot_x, self.pivot_y)

        self.turret.move(turret_pivot)
        self.turret.rotate(rotate_up, rotate_down)

    # method to speed up the tank in the right direction
    def accelerate(self):
        if self.speed <= 0:
            self.speed += self.acceleration * 6
        else:
            if abs(self.speed) < self.max_speed:
                self.speed += self.acceleration

    # method to speed up the tank in the left direction
    def decelerate(self):
        if self.speed >= 0:
            self.speed -= self.acceleration * 3
        else:
            if abs(self.speed) < self.max_speed:
                self.speed -= self.acceleration

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
class Turret:
    # Distance between the turret and the point of pivot
    pivot_distance = 24

    def __init__(self, pivot, starting_angle = 10):
        self.pivot = pivot
        self.angle = 10
        self.offset = Vector2()
        self.offset.from_polar((self.pivot_distance, -starting_angle))
        self.pos = pivot + self.offset
        self.image_orig = reference_dict['LeftTankTurret']
        self.image = self.image_orig
        self.turret = self.image.get_frect(center=self.pos)

    # Method to handle the rotation of the turret
    def rotate(self, rotating_up, rotating_down):
        if rotating_up:
            if self.angle < 65:
                self.angle += 1
        if rotating_down:
            if self.angle > 10:
                self.angle -= 1

        self.image, self.turret = rotate_on_pivot(self.image_orig, self.angle, self.pivot, self.pos)

    # Method to move the turret's pivot point
    def move(self, pivot):
        self.pivot = Vector2(pivot)
        self.pos = self.pivot + self.offset

    # Method to draw the turret
    def draw(self, surface):
        pygame.draw.line(surface, 'red', (self.pivot.x, 0), (self.pivot.x, SCREEN_HEIGHT))
        pygame.draw.line(surface, 'red', (0, self.pivot.y), (SCREEN_WIDTH, self.pivot.y))
        surface.blit(self.image, self.turret)


# Class for the Cannon-Balls that are launched from the turret
class CannonBall:
    def __init__(self, launch_pivot, launch_angle):
        self.launch_pivot = launch_pivot
        self.launch_angle = launch_angle


# Class that handles the game logic
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE, flags=pygame.SCALED)
        pygame.display.set_caption('Tank Wars')

        # set Framerate
        self.clock = pygame.time.Clock()
        self.FPS = 60

        # player action variables
        self.tank_moving_left = False
        self.tank_moving_right = False
        self.turret_rotating_up = False
        self.turret_rotating_down = False

        # Add the required images to the reference dictionary
        self.scale = 0.2
        self.load_image('LeftTank', 'LeftTankTurret')
        for i in range(3):
            self.load_image('LeftTank', f'LeftTank{i}')

        # Create Tank object for the first player
        self.first_tank = Tank('LeftTank', 500, 300)

    # Method to load the required images into the reference dictionary
    def load_image(self, tank_type, image_name, colorKey=None):
        image = pygame.image.load(f'Images/{tank_type}/{image_name}.png')

        if colorKey is not None:
            image.set_colorkey(colorKey)

        reference_dict[image_name] = image

    # Method to update the tank and its animation
    def update(self):
        self.first_tank.update_animation()
        self.first_tank.update(self.tank_moving_left, self.tank_moving_right,
                               self.turret_rotating_up, self.turret_rotating_down)

    # Method to draw the tank on the screen
    def draw(self, surface):
        surface.fill('black')
        self.first_tank.draw(surface)

    # Method that handles the game loop
    def run(self):
        run = True
        while run:
            # every 1/60th of a second, update the object positions and draw them
            self.clock.tick(self.FPS)
            self.update()
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

            pygame.display.update()
        pygame.quit()


# Run the game
if __name__ == '__main__':
    Game().run()
