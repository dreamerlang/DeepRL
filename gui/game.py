import sys

import pygame
from pygame.locals import *
from gui.uav import Uav
from gui.ugv import Ugv
from gui.obstacle import Obstacle
from collections import defaultdict, deque


class Game:

    SCREEN = (1366, 768)

    def __init__(self):
        self._game_over = False
        pygame.init()
        self._screen = pygame.display.set_mode(Game.SCREEN, 0, 32)
        pygame.display.set_caption("UXVSim Render Client")
        self._uav = []
        self._ugv = []
        self._obstacle = []
        self._his_info = defaultdict(deque)
        self._dx = Game.SCREEN[0] / 2
        self._dy = Game.SCREEN[1] / 2

    def process_event(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self._game_over = True

    def update(self):
        self._uav = []
        self._ugv = []
        self._obstacle = []
        # msg = self._message_dispatcher.pull_msg()
        msg={}


        pressed = pygame.key.get_pressed()
        if pressed[K_UP]:
            self._dy += 5
        if pressed[K_DOWN]:
            self._dy -= 5
        if pressed[K_LEFT]:
            self._dx += 5
        if pressed[K_RIGHT]:
            self._dx -= 5

        uav = Uav(self._screen)
        uav.set_pos([20,20,2])
        uav.move_view_port(self._dx, self._dy)
        self._uav.append(uav)
        # for obj in msg['objects']:
        #     if obj['type'] in ['uav', 'ugv']:
        #         # if self._his_info[obj['id']] and obj['pos'] != self._his_info[obj['id']][-1]:
        #         # if len(self._his_info[obj['id']]) != 0 and self._his_info[obj['id']][-1] != obj['pos']:
        #         self._his_info[obj['id']].append(obj['pos'])
        #         if len(self._his_info[obj['id']]) > 2000:
        #             self._his_info[obj['id']].popleft()
        #     if obj['type'] == 'uav':
        #         uav = Uav(self._screen)
        #         uav.set_pos(obj['pos'])
        #         uav.set_info(obj)
        #         uav.set_his_info(self._his_info[obj['id']])
        #         uav.move_view_port(self._dx, self._dy)
        #         self._uav.append(uav)
        #     elif obj['type'] == 'ugv':
        #         ugv = Ugv(self._screen)
        #         ugv.set_pos(obj['pos'])
        #         ugv.set_info(obj)
        #         ugv.set_his_info(self._his_info[obj['id']])
        #         ugv.move_view_port(self._dx, self._dy)
        #         self._ugv.append(ugv)
        #     elif obj['type'] == 'obstacle':
        #         # TODO: now I don't want to add support for obstacle
        #         lx = obj['shape_info']['width']
        #         ly = obj['shape_info']['height']
        #         cx = obj['shape_info']['cx']
        #         cy = obj['shape_info']['cy']
        #         obs = Obstacle(self._screen, (lx, ly))
        #         obs.set_pos([cx - lx / 2, cy - ly / 2, 0])
        #         obs.set_info(obj)
        #         obs.move_view_port(self._dx, self._dy)
        #         self._obstacle.append(obs)
        #     else:
        #         print('[WARNING]: UNKNOWN OBJECT TYPE {}'.format(obj['type']), file=sys.stderr)

    def render(self):
        self._screen.fill((0xD2, 0xB4, 0x8C))
        # for obs in self._obstacle:
        #     obs.render(debug_info=True)
        # for ugv in self._ugv:
        #     ugv.render(debug_info=True)
        for uav in self._uav:
            uav.render(debug_info=True)
        pygame.display.flip()

    def run(self):
        while not self._game_over:
            self.process_event()
            self.update()
            self.render()
            # delay 10 ms

