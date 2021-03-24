import pygame
from entity import Entity


class Ugv(Entity):

    def __init__(self, window):
        self._img = pygame.image.load('./imgs/ugv.png')
        self._img = pygame.transform.scale(self._img, (20, 20))
        super(Ugv, self).__init__(self._img, window)
