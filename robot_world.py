from random import *
from robot import *

class RobotWorld:
    def __init__(self, cell_size, step_time_in_ms):
        self.cell = cell_size
        self.width = 0
        self.height = 0
        self.robot = None
        self.objects = None
        self.game_state = None
        self.level_number = 0
        self.delay = step_time_in_ms
        self.screen = None

    def set_step_time(self, step_time_in_ms):
        if 50 <= step_time_in_ms <= 1000:
            self.delay = step_time_in_ms
        else:
            print("Step time must be between 50 and 1000 ms")

    def turn_right(self):
        self.robot.turn_right()
        self.calculate_new_game_state()
        self.draw()

    def turn_left(self):
        self.robot.turn_left()
        self.calculate_new_game_state()
        self.draw()

    def step_forward(self):
        self.robot.step_forward(self.objects)
        self.calculate_new_game_state()
        self.draw()

    def step_back(self):
        self.robot.step_back(self.objects)
        self.calculate_new_game_state()
        self.draw()

    def grab_release_block(self):
        self.robot.grab_release_block(self.objects)
        self.calculate_new_game_state()
        self.draw()

    def scan_steps_ahead(self):
        # return the nr of step_forward actions the robot can do before encountering a Wall, Block or Tile
        return self.robot.steps_ahead(self.objects)

    def scan_object_ahead(self):
        # returns the first object the robot would encounter with repeated step_forward: Wall, Block or Tile
        return self.robot.object_ahead(self.objects)

    def scan_direction(self):
        # returns the current direction of the robot
        return self.robot.direction

    def scan_energy(self):
        # return the remaining energy of the robot
        return self.robot.energy

    def all_tiles_covered(self):
        # are all tiles covered by a block of the same color?
        # split into lists tiles and blocks to check
        tiles  = []
        blocks = []
        for obj in self.objects:
            if isinstance(obj, Tile):
                tiles.append(obj)
            elif isinstance(obj, Block):
                blocks.append(obj)

        if tiles == [] or blocks == []:
            return False

        for tile in tiles:
            covered = False
            for block in blocks:
                if tile.x == block.x and tile.y == block.y and tile.color == block.color:
                    covered = True
            if not covered:
                return False
        return True

    def calculate_new_game_state(self):
        # game state can only change from 'RUNNING' to 'FAILED' or 'COMPLETED'
        if self.game_state != 'PLAYING':
            return
        # energy ran out ?
        if self.robot.energy == 0:
            self.game_state = 'FAILED'
        # all tiles covered by same colored blocks?
        elif self.all_tiles_covered():
            self.game_state = 'COMPLETED'

    def object_at(self, x, y):
        for obj in self.objects:
            if obj.at_location(x, y):
                return obj
        return None

    def user_info(self):
        my_font = pygame.font.SysFont("monospace", 20)
        info = self.game_state + " Lvl: " + str(self.level_number).rjust(2)\
               + " Energy: " + str(self.robot.energy).rjust(2)
        label_top = my_font.render(info, 1, (255, 255, 255))
        x = self.cell * 2
        y = 5 * self.cell // 4
        self.screen.blit(label_top, (x, y))

        for x_value in range(self.width - 2):
            x_label = str(x_value + 1)
            x_render = my_font.render(x_label, 1, (255, 255, 255))
            x_pos = int((x_value + 2.25)*self.cell)
            y_pos = int((self.height + 0.25) * self.cell)
            self.screen.blit(x_render, (x_pos, y_pos))

        for y_value in range(self.height - 2):
            y_label = str(y_value + 1)
            y_render = my_font.render(y_label, 1, (255, 255, 255))
            x_pos = int(1.25 * self.cell)
            y_pos = int((self.height - y_value - 0.75)*self.cell)
            self.screen.blit(y_render, (x_pos, y_pos))

    def draw(self):
        self.screen.fill(BLACK)

        for obj in self.objects:
            obj.draw(self.screen, self.cell)

        # draw grid
        for w in range(self.width + 1):
            start = [self.cell * (w + 1) , self.cell]
            end   = [self.cell * (w + 1),  self.cell * (self.height + 1)]
            pygame.draw.line(self.screen, GREY, start, end, 1)
        for h in range(self.height + 1):
            start = [self.cell, self.cell * (h + 1)]
            end   = [self.cell * (self.width + 1), self.cell * (h + 1)]
            pygame.draw.line(self.screen, GREY, start, end, 1)

        self.robot.draw(self.screen, self.cell)
        self.user_info()

        pygame.display.flip()
        events = pygame.event.get() # hack to avoid 'application does not respond' in windows
        pygame.time.delay(self.delay)

    def add_outer_walls(self):
        for w in range(self.width):
            self.objects.append(Wall(w, 0))
            self.objects.append(Wall(w, self.height - 1))
        for h in range(1, self.height - 1):
            self.objects.append(Wall(0, h))
            self.objects.append(Wall(self.width - 1, h))

    def add_random_blocks(self, nr_of_blocks, color):
        desired_nr_objects = len(self.objects) + nr_of_blocks
        while len(self.objects) < desired_nr_objects:
            x = randint(1, self.width - 2)
            y = randint(1, self.height - 2)
            if self.object_at(x, y) == None:
                self.objects.append(Block(x, y, color))

    def add_random_tiles(self, nr_of_tiles, color):
        desired_nr_objects = len(self.objects) + nr_of_tiles
        while len(self.objects) < desired_nr_objects:
            x = randint(1, self.width - 2)
            y = randint(1, self.height - 2)
            if self.object_at(x, y) == None:
                self.objects.append(Tile(x, y, color))

    def add_robot(self, x, y, direction, energy):
        if x == 0:
            x = randint(1, self.width - 2)
        if y == 0:
            y = randint(1, self.height - 2)
        if direction == 'RANDOM':
            direction = choice(['LEFT', 'RIGHT', 'UP', 'DOWN'])
        self.robot = Robot(x, y, direction, energy, cargo = None)

    def wait_until_start_or_cancel(self):
        # return == True means can_start, False means cancelled
        while True: # endless loop because we use returns to exit
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                return False # cancelled
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return False # cancelled
            elif event.type == pygame.KEYDOWN:
                return True
            else:
                continue  # ignore any other key or mouse event

    def start_level(self, level_number):
        self.game_state = 'PLAYING'
        self.level_number = level_number

        if level_number == 0:
            self.width = randint(15, 20)
            self.height = randint(10, 15)
            self.screen = pygame.display.set_mode((self.cell * (self.width + 2), self.cell * (self.height + 2)))
            self.objects = []
            self.add_outer_walls()
            robot_x = self.width // 2 - 1
            robot_y = self.height // 2
            self.add_robot(robot_x, robot_y, direction='UP', energy=100)
            self.objects.append(Block(robot_x + 2, robot_y, BLUE))
            #self.add_random_blocks(nr_of_blocks = 0, color = None)
            #self.add_random_tiles(nr_of_tiles = 0, color = None)

        if level_number == 1:
            self.width = randint(15, 20)
            self.height = randint(10, 15)
            self.screen = pygame.display.set_mode((self.cell * (self.width + 2), self.cell * (self.height + 2)))
            self.objects = []
            self.add_outer_walls()
            self.add_robot(x=0, y=0, direction='RANDOM', energy=100)
            self.add_random_blocks(nr_of_blocks = 0, color = None)
            self.add_random_tiles(nr_of_tiles = 0, color = None)

        elif level_number == 2:
            self.width = randint(10, 15)
            self.height = randint(8, 12)
            self.screen = pygame.display.set_mode((self.cell * (self.width + 2), self.cell * (self.height + 2)))
            self.objects = []
            self.add_outer_walls()
            x_inner_wall = self.width // 2 + randint(-1, 1)
            y_inner_wall_gap = self.height // 2 + randint(-1, 1)
            for y in range(1, self.height):
                if y != y_inner_wall_gap:
                    self.objects.append(Wall(x_inner_wall, y))
            x_robot = randint(2, self.width - 2)
            y_robot = randint(2, self.height - 2)
            while x_robot == x_inner_wall:
                x_robot = randint(2, self.height - 2)
            self.add_robot(x_robot, y_robot, direction='RANDOM', energy=100)
            self.add_random_blocks(nr_of_blocks = 0, color = None)
            self.add_random_tiles(nr_of_tiles = 0, color = None)

        elif level_number == 3:
            # create a world with one random red tile
            self.energy = 99
            self.width = randint(15, 20)
            self.height = randint(10, 15)
            self.screen = pygame.display.set_mode((self.cell * (self.width + 2), self.cell * (self.height + 2)))
            self.objects = []
            self.add_outer_walls()
            self.add_robot(x=0, y=0, direction='RANDOM', energy=100)
            self.add_random_tiles(nr_of_tiles=1, color=RED)

        elif level_number == 4:
            # create world with a single block not touching a wall
            self.width = randint(15, 20)
            self.height = randint(12, 15)
            self.screen = pygame.display.set_mode((self.cell * (self.width + 2), self.cell * (self.height + 2)))
            self.objects = []
            self.add_outer_walls()
            self.add_robot(x=0, y=0, direction='RANDOM', energy=100)
            x_blue, y_blue = self.robot.x, self.robot.y
            while self.robot.x - 1 <= x_blue <= self.robot.x + 1 or self.robot.y - 1 <= y_blue <= self.robot.y + 1:
                x_blue, y_blue = randint(3, self.width - 3), randint(3, self.height - 3)
            self.objects.append(Block(x_blue, y_blue, BLUE))

        elif level_number == 5:
            # create world with random path of yellow tiles from left to right
            self.energy = 99
            self.width = randint(15, 20)
            self.height = randint(10, 15)
            self.screen = pygame.display.set_mode((self.cell * (self.width + 2), self.cell * (self.height + 2)))
            self.objects = []
            self.add_outer_walls()
            x = 1
            y = randint(2, self.height - 2)
            self.add_robot(x, y, direction='RANDOM', energy=100)
            self.objects.append(Tile(x, y, YELLOW))
            old_direction = 'RIGHT'
            while x < self.width - 2:
                # chose new direction
                if y == self.height - 2: # near bottom side
                    if old_direction == 'DOWN':
                        direction = 'RIGHT'
                    else:
                        direction = choice(['UP', 'RIGHT'])
                elif y == 1: # near top side
                    if old_direction == 'UP':
                        direction = 'RIGHT'
                    else:
                        direction = choice(['DOWN', 'RIGHT'])
                elif old_direction == 'DOWN':
                    direction = choice(['RIGHT', 'DOWN'])
                elif old_direction == 'UP':
                    direction = choice(['RIGHT', 'UP'])
                else:
                    direction = choice(['RIGHT', 'DOWN', 'UP'])

                # add 1 or 2 tiles depending on direction
                if direction == 'UP':
                    y = y - 1
                    self.objects.append(Tile(x, y, YELLOW))
                elif direction == 'DOWN':
                    y = y + 1
                    self.objects.append(Tile(x, y, YELLOW))
                else: # direction == 'RIGHT'
                    x = x + 1
                    self.objects.append(Tile(x, y, YELLOW))
                    x = x + 1
                    if x < self.width - 1:
                        self.objects.append(Tile(x, y, YELLOW))

                old_direction = direction

        elif level_number == 6:
            # create a world with one random pink block and tile
            self.energy = 1000
            self.width = randint(15, 20)
            self.height = randint(10, 15)
            self.screen = pygame.display.set_mode((self.cell * (self.width + 2), self.cell * (self.height + 2)))
            self.objects = []
            self.add_outer_walls()
            self.add_robot(x=0, y=0, direction='RANDOM', energy=1000)
            x_block, y_block = self.robot.x, self.robot.y
            while x_block == self.robot.x and y_block == self.robot.y:
                x_block, y_block = randint(3, self.width - 3), randint(3, self.height - 3)
            self.objects.append(Block(x_block, y_block, PINK))
            x_tile, y_tile = self.robot.x, self.robot.y
            while (x_tile == self.robot.x and y_tile == self.robot.y)\
                    or (x_tile == x_block and y_tile == y_block):
                x_tile, y_tile = randint(3, self.width - 3), randint(3, self.height - 3)
            self.objects.append(Tile(x_tile, y_tile, PINK))

        self.draw()
        print("\nClick on game window and press key to start script", self.level_number)
        print("Close window or press <ESC> to cancel\n")
        start_script = self.wait_until_start_or_cancel()
        return start_script

    def stop_level(self, ran_script):
        self.game_state = 'NOT_PLAYING'
        if ran_script:
            print("\nClose game window to finish.", self.level_number)
            result = self.wait_until_start_or_cancel()  # we want to close so result is ignored
        else:
            print("\n*** You cancelled running script", self.level_number, "***")
        pygame.display.quit()
