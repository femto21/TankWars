import pygame

from background import Background
from scripts.config import SCREEN_SIZE, load_image
from tank import Tank
from tiles import Tiles


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
        load_image('LeftTankTurret', 1, 'LeftTank')
        load_image('RightTankTurret', 1, 'RightTank')
        for i in range(3):
            load_image(f'LeftTank{i}', 1, 'LeftTank')
            load_image(f'RightTank{i}', 1, 'RightTank')
        load_image('Cannonball', 0.6)
        for i in range(1, 9):
            load_image(f'explosion{i}', 3, 'LeftTank')
        load_image('Background', 1)

        self.bg = Background()
        self.tiles = Tiles()

        # Create Tank object for the first player
        self.first_tank = Tank('LeftTank', 500, 405)

        # Create Tank object for the second player
        self.second_tank = Tank('RightTank', 800, 405)

        self.player_turn = 1
        self.timer = 0
        self.timer_started = False

    # Method to update the tank and its animation
    def update(self, dt):
        if self.player_turn == 1:
            self.first_tank.update_animation()
            self.first_tank.update(self.tank_moving_left, self.tank_moving_right,
                                   self.turret_rotating_up, self.turret_rotating_down, self.charging_launch, dt)
        else:
            self.first_tank.smoke_group.update()
        if self.player_turn == 2:
            self.second_tank.update_animation()
            self.second_tank.update(self.tank_moving_left, self.tank_moving_right,
                                    self.turret_rotating_up, self.turret_rotating_down, self.charging_launch, dt)
        else:
            self.second_tank.smoke_group.update()

    # Method to draw the tank on the screen
    def draw(self, surface):
        surface.fill('black')
        self.bg.draw_canvas(surface)
        self.tiles.draw_tiles(surface)
        self.first_tank.draw(surface)
        self.second_tank.draw(surface)

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

            if self.player_turn == 1:
                if self.first_tank.turret.cannonball.explosion.explosion_started:
                    self.timer_started = True
                if self.timer_started:
                    self.timer += dt * self.FPS
                    if self.timer >= 35:
                        self.player_turn = 2
                        self.timer = 0
                        self.timer_started = False
            elif self.player_turn == 2:
                if self.second_tank.turret.cannonball.explosion.explosion_started:
                    self.timer_started = True
                if self.timer_started:
                    self.timer += dt * self.FPS
                    if self.timer >= 35:
                        self.player_turn = 1
                        self.timer = 0
                        self.timer_started = False

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
