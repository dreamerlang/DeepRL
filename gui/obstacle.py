import pygame
from entity import Entity


class Obstacle(Entity):

    def __init__(self, window, size):
        surface = pygame.Surface(size)
        surface.fill((0x00, 0x00, 0x00))
        super(Obstacle, self).__init__(surface, window)
