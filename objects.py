import pygame
from definitions import *

# abstract parent class of Wall, Block and Tile
# therefore: not meant for direct instantiation
class Object():
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def at_location(self, x, y):
        return x == self.x and y == self.y


class Block(Object):
    def draw(self, screen, cell):
        pygame.draw.rect(screen,
                         self.color,
                         (cell * (self.x + 1), cell * (self.y + 1), cell, cell))


class Tile(Object):
    def draw(self, screen, cell):
        pygame.draw.rect(screen,
                         self.color,
                         (cell * (self.x + 1) + 1, cell * (self.y + 1) + 1, cell - 1, cell - 1), 1)

class Wall(Object):
    def __init__(self, x, y):
        Object.__init__(self, x, y, GREY)

    def draw(self, screen, cell):
        pygame.draw.rect(screen,
                         self.color,
                         (cell * (self.x + 1), cell * (self.y + 1), cell, cell))
