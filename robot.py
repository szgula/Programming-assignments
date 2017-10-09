import pygame
from definitions import *
from objects import *

class Robot:
    def __init__(self, x, y, direction, energy, cargo):
        self.x = x
        self.y = y
        self.direction = direction
        self.color = GREEN
        self.energy = energy # steps left in this level
        self.cargo = cargo # block being dragged by robot (None means no cargo)

    def at_location(self, x, y):
        return x == self.x and y == self.y

    def object_at(self, game_objects, x, y):
        for obj in game_objects:
            if obj.at_location(x, y):
                return obj
        return None

    def turn_right(self):
        if self.energy < 1: # cannot turn without energy
            return

        if self.cargo != None: # cannot turn with cargo
            return

        if self.direction == 'LEFT':
            self.direction = 'UP'
        elif self.direction == 'RIGHT':
            self.direction = 'DOWN'
        elif self.direction == 'UP':
            self.direction = 'RIGHT'
        elif self.direction == 'DOWN':
            self.direction = 'LEFT'

    def turn_left(self):
        if self.energy < 1:  # cannot turn without energy
            return

        if self.cargo != None: # cannot turn with cargo
            return

        elif self.direction == 'LEFT':
            self.direction = 'DOWN'
        elif self.direction == 'RIGHT':
            self.direction = 'UP'
        elif self.direction == 'UP':
            self.direction = 'LEFT'
        elif self.direction == 'DOWN':
            self.direction = 'RIGHT'

    def move(self, game_objects, step):
        if self.energy < 1: # cannot move without energy
            return

        dx, dy = step
        if self.cargo == None: # try move without cargo
            obstacle = self.object_at(game_objects, self.x + dx, self.y + dy)
            if not isinstance(obstacle, Block) and not isinstance(obstacle, Wall):
                # cannot walk into a block or a wall
                self.x, self.y = self.x + dx, self.y + dy
            # energy is also lost when trying to walk into a wall or a block
            self.energy = self.energy - 1
        else: # try move with cargo
            obstacle_for_robot = self.object_at(game_objects, self.x + dx, self.y + dy)
            obstacle_for_cargo = self.object_at(game_objects, self.cargo.x + dx, self.cargo.y + dy)
            robot_can_move = (obstacle_for_robot == None\
                              or isinstance(obstacle_for_robot, Tile)\
                              or obstacle_for_robot == self.cargo)
            cargo_can_move = (obstacle_for_cargo == None\
                              or isinstance(obstacle_for_cargo, Tile))
            if robot_can_move and cargo_can_move:
                self.x, self.y = self.x + dx, self.y + dy
                self.cargo.x, self.cargo.y = self.cargo.x + dx, self.cargo.y + dy
            # energy is lost also when movement is blocked by a wall or a block
            self.energy = max(0, self.energy - 2)

    def step_forward(self, game_objects):
        if self.energy == 0: # cannot move without energy
            return

        if self.direction == 'LEFT':
            self.move(game_objects, STEP_LEFT)
        elif self.direction == 'RIGHT':
            self.move(game_objects, STEP_RIGHT)
        elif self.direction == 'UP':
            self.move(game_objects, STEP_UP)
        elif self.direction == 'DOWN':
            self.move(game_objects, STEP_DOWN)


    def step_back(self, game_objects):
        if self.energy == 0: # cannot move without energy
            return

        if self.direction == 'LEFT':
            self.move(game_objects, STEP_RIGHT)
        elif self.direction == 'RIGHT':
            self.move(game_objects, STEP_LEFT)
        elif self.direction == 'UP':
            self.move(game_objects, STEP_DOWN)
        elif self.direction == 'DOWN':
            self.move(game_objects, STEP_UP)


    def grab_release_block(self, game_objects):
        if self.energy == 0: # cannot grab without energy
            return

        if self.cargo != None:
            self.cargo = None  # release cargo
            return

        if self.direction == 'LEFT':
            candidate_cargo = self.object_at(game_objects, self.x - 1, self.y)
        elif self.direction == 'RIGHT':
            candidate_cargo = self.object_at(game_objects, self.x + 1, self.y)
        elif self.direction == 'UP':
            candidate_cargo = self.object_at(game_objects, self.x, self.y - 1)
        else:  # direction == 'DOWN'
            candidate_cargo = self.object_at(game_objects, self.x, self.y + 1)
        if isinstance(candidate_cargo, Block):
            self.cargo = candidate_cargo

    def object_and_steps_ahead(self, game_objects, direction): # returns the first object ahead and distance to it
        steps = 0
        if direction == 'UP':
            object_ahead = self.object_at(game_objects, self.x, self.y - (steps + 1))
            while object_ahead == None:
                steps = steps + 1
                object_ahead = self.object_at(game_objects, self.x, self.y - (steps + 1))
        elif direction == 'DOWN':
            object_ahead = self.object_at(game_objects, self.x, self.y + (steps + 1))
            while object_ahead == None:
                steps = steps + 1
                object_ahead = self.object_at(game_objects, self.x, self.y + (steps + 1))
        elif direction == 'RIGHT':
            object_ahead = self.object_at(game_objects, self.x + (steps + 1), self.y)
            while object_ahead == None:
                steps = steps + 1
                object_ahead = self.object_at(game_objects, self.x + (steps + 1), self.y)
        else: # direction == 'LEFT':
            object_ahead = self.object_at(game_objects, self.x - (steps + 1), self.y)
            while object_ahead == None:
                steps = steps + 1
                object_ahead = self.object_at(game_objects, self.x - (steps + 1), self.y)
        if type(object_ahead) is Tile:
            object_type = 'Tile'
        elif type(object_ahead) is Block:
            object_type = 'Block'
#        elif type(object_ahead) is Charger:
#            object_type = 'Charger'
        else:
            object_type = 'Wall'
        return object_type, steps

    def steps_ahead(self, game_objects):
        color, steps = self.object_and_steps_ahead(game_objects, self.direction)
        return steps

    def object_ahead(self, game_objects):
        color, steps = self.object_and_steps_ahead(game_objects, self.direction)
        return color

    def draw(self, screen, cell):
        pygame.draw.rect(screen, self.color,
                         (cell * (self.x + 1), cell * (self.y + 1), cell, cell))
        if self.direction == 'UP':
            pygame.draw.circle(screen, WHITE, (cell * (self.x + 1) + cell // 3, cell * (self.y + 1) + cell // 4), cell // 4)
            pygame.draw.circle(screen, WHITE, (cell * (self.x + 1) + 2 * cell // 3, cell * (self.y + 1) + cell // 4), cell // 4)
            pygame.draw.circle(screen, BLACK, (cell * (self.x + 1) + cell // 3, cell * (self.y + 1) + cell // 5), cell // 7)
            pygame.draw.circle(screen, BLACK, (cell * (self.x + 1) + 2 * cell // 3, cell * (self.y + 1) + cell // 5), cell // 7)
        elif self.direction == 'DOWN':
            pygame.draw.circle(screen, WHITE, (cell * (self.x + 1) + cell // 3, cell * (self.y + 1) + 3 * cell // 4), cell // 4)
            pygame.draw.circle(screen, WHITE, (cell * (self.x + 1) + 2 * cell // 3, cell * (self.y + 1) + 3 * cell // 4), cell // 4)
            pygame.draw.circle(screen, BLACK, (cell * (self.x + 1) + cell // 3, cell * (self.y + 1) + 4 * cell // 5), cell // 7)
            pygame.draw.circle(screen, BLACK, (cell * (self.x + 1) + 2 * cell // 3, cell * (self.y + 1) + 4 * cell // 5), cell // 7)
        elif self.direction == 'RIGHT':
            pygame.draw.circle(screen, WHITE, (cell * (self.x + 1) + 3 * cell // 4, cell * (self.y + 1) + cell // 3), cell // 4)
            pygame.draw.circle(screen, WHITE, (cell * (self.x + 1) + 3 * cell // 4, cell * (self.y + 1) + 2 * cell // 3), cell // 4)
            pygame.draw.circle(screen, BLACK, (cell * (self.x + 1) + 4 * cell // 5, cell * (self.y + 1) + cell // 3), cell // 7)
            pygame.draw.circle(screen, BLACK, (cell * (self.x + 1) + 4 * cell // 5, cell * (self.y + 1) + 2 * cell // 3), cell // 7)
        elif self.direction == 'LEFT':
            pygame.draw.circle(screen, WHITE, (cell * (self.x + 1) + cell // 4, cell * (self.y + 1) + cell // 3), cell // 4)
            pygame.draw.circle(screen, WHITE, (cell * (self.x + 1) + cell // 4, cell * (self.y + 1) + 2 * cell // 3), cell // 4)
            pygame.draw.circle(screen, BLACK, (cell * (self.x + 1) + cell // 5, cell * (self.y + 1) + cell // 3), cell // 7)
            pygame.draw.circle(screen, BLACK, (cell * (self.x + 1) + cell // 5, cell * (self.y + 1) + 2 * cell // 3), cell // 7)
        if self.cargo != None:
            pygame.draw.rect(screen, self.color,
                             (cell * (self.cargo.x + 1), cell * (self.cargo.y + 1), cell, cell),
                             2)
