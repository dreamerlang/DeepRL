import pygame


class Entity:

    def __init__(self, render_obj, render_window):
        self._pos = [0, 0, 0]
        self._obj = render_obj
        self._debug_info = {}
        self._window = render_window
        self._cam_x = 0
        self._cam_y = 0
        self._font = pygame.font.SysFont('ubuntumono', 16)
        self._his = []

    def set_pos(self, pos):
        self._pos = [pos[0], pos[1], pos[2]]

    def set_info(self, info):
        self._debug_info = info

    def move_view_port(self, dx, dy):
        self._cam_x += dx
        self._cam_y += dy

    def set_his_info(self, his_info):
        for p in his_info:
            self._his.append([int(p[0]), int(p[1])])

    def render(self, debug_info=False):
        SCALE = 20
        self._window.blit(self._obj, (self._pos[0] * SCALE + self._cam_x , self._pos[1] * SCALE + self._cam_y))
        if debug_info:
            info = []
            name = self._font.render('name: {}'.format(self._debug_info.get('id', None)),
                                     True, (0xff, 0x00, 0x00))
            info.append(name)
            pos = self._font.render('pos: {:.2f}, {:.2f}, {:.2f}'.format(self._pos[0], self._pos[1], self._pos[2]),
                                    True, (0xff, 0x00, 0x00))
            info.append(pos)

            if self._debug_info.get('linear_vel', None) is not None:
                vel = self._font.render('vel: {:.2f}, {:.2f}, {:.2f}'.format(*self._debug_info['linear_vel']), True,
                                        (0xff, 0x00, 0x00))
                info.append(vel)
            cnt = 0
            for f in info:
                self._window.blit(f, (self._pos[0] * SCALE + self._cam_x + 50, self._pos[1] * SCALE + self._cam_y + 20 * cnt))
                cnt += 1
            for p in self._his:
                pygame.draw.circle(self._window, (0xff, 0x00, 0x00),
                                   (int(p[0] * SCALE + self._cam_x), int(p[1] * SCALE + self._cam_y)), 1)
