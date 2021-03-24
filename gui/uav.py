import pygame
from gui.entity import Entity


class Uav(Entity):

    def __init__(self, window):
        self._img = pygame.image.load('./imgs/uav.png').convert_alpha()
        self._img = pygame.transform.scale(self._img, (20, 20))
        super(Uav, self).__init__(self._img, window)
