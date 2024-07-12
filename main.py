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


def rotate_on_pivot(image, angle, pivot, origin):
    surf = pygame.transform.rotate(image, angle)
    offset = pivot + (origin - pivot).rotate(-angle)
    rect = surf.get_rect(center = offset)
    return surf, rect


class Tank(pygame.sprite.Sprite):
    def __init__(self, tank_type, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.tank_type = tank_type
        self.animation_list = []
        self.animation_index = 0
        self.update_time = pygame.time.get_ticks()
        self.speed = speed
        for i in range(3):
            image_name = f'{self.tank_type}{i}'
            image = reference_dict[image_name]
            self.animation_list.append(image)
        self.left_tank_image = self.animation_list[self.animation_index]
        self.player_one_tank = self.left_tank_image.get_rect()
        self.player_one_tank.center = (x, y)

    def move(self, moving_left, moving_right):
        # reset movement variables
        dx = 0
        dy = 0

        # assign movement variables if moving left or right
        if moving_left:
            dx = -self.speed

        if moving_right:
            dx = self.speed

        # update rectangle position
        self.player_one_tank.x = self.player_one_tank.x + dx
        self.player_one_tank.y = self.player_one_tank.y + dy

    def draw(self, surface):
        surface.blit(self.left_tank_image, self.player_one_tank)

    def update_animation(self):
        ANIMATION_COOLDOWN = 100
        # update image depending on current frame
        self.left_tank_image = self.animation_list[self.animation_index]

        # check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.animation_index = self.animation_index + 1

        # if animation has run out, reset back to the start
        if self.animation_index >= len(self.animation_list):
            self.animation_index = 0


class Turret:
    pivot_distance = 24

    def __init__(self, pivot, starting_angle=0):
        self.pivot = pivot
        self.angle = 0
        self.offset = Vector2()
        self.offset.from_polar((self.pivot_distance, -starting_angle))
        self.pos = pivot + self.offset
        self.image_orig = reference_dict['LeftTankTurret']
        self.image = self.image_orig
        self.player_one_turret = self.image.get_rect(center = self.pos)

    def rotate(self, rotating_up, rotating_down):
        if rotating_up:
            self.angle += 1
        if rotating_down:
            self.angle -= 1

        self.image, self.player_one_turret = rotate_on_pivot(self.image_orig, self.angle, self.pivot, self.pos)

    def move(self, pivot):
        self.pivot = Vector2(pivot)
        self.pos = self.pivot + self.offset

    def draw(self, surface):
        pygame.draw.line(surface, 'red', (self.pivot.x, 0), (self.pivot.x, SCREEN_HEIGHT))
        pygame.draw.line(surface, 'red', (0, self.pivot.y), (SCREEN_WIDTH, self.pivot.y))
        surface.blit(self.image, self.player_one_turret)


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

        # Create objects for the first player
        self.first_tank = Tank('LeftTank', 500, 300, 5)

        self.pivot_x = self.first_tank.player_one_tank.x + BLOCK_WIDTH
        self.pivot_y = self.first_tank.player_one_tank.y + BLOCK_HEIGHT - 10
        self.first_turret = Turret(Vector2(self.pivot_x, self.pivot_y), starting_angle=0)

    def load_image(self, tank_type, image_name, colorKey=None):
        image = pygame.image.load(f'Images/{tank_type}/{image_name}.png')

        if colorKey is not None:
            image.set_colorkey(colorKey)

        reference_dict[image_name] = image

    def update(self):
        self.first_tank.update_animation()
        self.first_tank.move(self.tank_moving_left, self.tank_moving_right)
        self.pivot_x = self.first_tank.player_one_tank.x + BLOCK_WIDTH
        self.pivot_y = self.first_tank.player_one_tank.y + BLOCK_HEIGHT - 10
        turret_pivot = Vector2(self.pivot_x, self.pivot_y)

        self.first_turret.rotate(self.turret_rotating_up, self.turret_rotating_down)
        self.first_turret.move(turret_pivot)

    def draw(self, surface):
        surface.fill('black')
        self.first_turret.draw(surface)
        self.first_tank.draw(surface)

    def run(self):
        run = True
        while run:
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


if __name__ == '__main__':
    Game().run()
