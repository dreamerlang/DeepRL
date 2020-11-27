import jpype
import json
import uuid
import random
import math
import numpy as np
from sympy import *

jpype.startJVM(classpath=['F:/IdeaProjects/UXVSimulator/target/UXVSim-1.0-SNAPSHOT-jar-with-dependencies.jar'])
Emulator = jpype.JClass("uxvsim.Emulator")


def solve_acc():
    t = 1
    x_abs = 20
    v_abs = 10
    param_list = [[[[t, 0, 0, 0, 0], [t, 0, 0, 0, 0]], [[t, x_abs, 0, v_abs, 5], [t, 0, 0, 0, 0]],
                   [[t, -x_abs, 0, -v_abs, -5], [t, 0, 0, 0, 0]], [[t, 0, 0, 0, 0], [t, x_abs, 0, v_abs, 5]],
                   [[t, 0, 0, 0, 0], [t, -x_abs, 0, -v_abs, -5]]],
                  [[[t, 0, v_abs, 0, -5], [t, 0, 0, 0, 0]], [[t, x_abs, v_abs, v_abs, 0], [t, 0, 0, 0, 0]],
                   [[t, -x_abs, v_abs, -v_abs, -5], [t, 0, 0, 0, 0]], [[t, 0, v_abs, 0, -5], [t, x_abs, 0, v_abs, 5]],
                   [[t, 0, v_abs, 0, -5], [t, -x_abs, 0, -v_abs, -5]]],
                  [[[t, 0, -v_abs, 0, 5], [t, 0, 0, 0, 0]], [[t, x_abs, -v_abs, v_abs, 5], [t, 0, 0, 0, 0]],
                   [[t, -x_abs, -v_abs, -v_abs, 0], [t, 0, 0, 0, 0]], [[t, 0, -v_abs, 0, 5], [t, x_abs, 0, v_abs, 5]],
                   [[t, 0, -v_abs, 0, 5], [t, -x_abs, 0, -v_abs, -5]]],
                  [[[t, 0, 0, 0, 0], [t, 0, v_abs, 0, -5]], [[t, x_abs, 0, v_abs, 5], [t, 0, v_abs, 0, -5]],
                   [[t, -x_abs, 0, -v_abs, -5], [t, 0, v_abs, 0, -5]], [[t, 0, 0, 0, 0], [t, x_abs, v_abs, v_abs, 0]],
                   [[t, 0, 0, 0, 0], [t, -x_abs, v_abs, -v_abs, -5]]],
                  [[[t, 0, 0, 0, 0], [t, 0, -v_abs, 0, 5]], [[t, x_abs, 0, v_abs, 5], [t, 0, -v_abs, 0, 5]],
                   [[t, -x_abs, 0, -v_abs, -5], [t, 0, -v_abs, 0, 5]], [[t, 0, 0, 0, 0], [t, x_abs, -v_abs, v_abs, 5]],
                   [[t, 0, 0, 0, 0], [t, -x_abs, -v_abs, -v_abs, 0]]]]  # t,x,v0,v1,b
    acc_cmd_table = []
    for i in range(5):
        list_i = []
        for j in range(5):
            list_acc = []
            # print(i,j)
            x_list = param_list[i][j][0]
            t = x_list[0]
            x = x_list[1]
            v0 = x_list[2]
            v1 = x_list[3]
            b = x_list[4]
            a1 = Symbol('a1')
            a2 = Symbol('a2')
            a3 = Symbol('a3')
            x_res_map = solve(
                [a1 - b, 6 * v0 * t + 5 * t * t * a1 + 3 * t * t * a2 + t * t * a3 - 2 * x,
                 v0 + t * a1 + t * a2 + t * a3 - v1],
                [a1, a2, a3])
            # print(x_res_map[a1],x_res_map[a2],x_res_map[a3])
            list_acc_x = [float(x_res_map[a1]), float(x_res_map[a2]), float(x_res_map[a3])]
            list_acc.append(list_acc_x)

            y_list = param_list[i][j][1]
            t = y_list[0]
            x = y_list[1]
            v0 = y_list[2]
            v1 = y_list[3]
            b = y_list[4]
            y_res_map = solve(
                [a1 - b, 6 * v0 * t + 5 * t * t * a1 + 3 * t * t * a2 + t * t * a3 - 2 * x,
                 v0 + t * a1 + t * a2 + t * a3 - v1],
                [a1, a2, a3])
            # print(y_res_map[a1],y_res_map[a2],y_res_map[a3])
            list_acc_y = [float(y_res_map[a1]), float(y_res_map[a2]), float(y_res_map[a3])]
            list_acc.append(list_acc_y)
            list_i.append(list_acc)
        acc_cmd_table.append(list_i)

    # print(acc_cmd_table)
    return acc_cmd_table


def action_to_state(action):
    if action == 0:
        return 0
    if action == 1:
        return 2
    if action == 2:
        return 1
    if action == 3:
        return 4
    if action == 4:
        return 3
    return -1


def velocity_to_state(vx, vy):
    if math.fabs(vx) <= 0.1 and math.fabs(vy) <= 0.1:
        return 0
    if vx > 0.1 and math.fabs(vy) <= 0.1:
        return 1
    if vx < -0.1 and math.fabs(vy) <= 0.1:
        return 2
    if math.fabs(vx) <= 0.1 and vy > 0.1:
        return 3
    if math.fabs(vx) <= 0.1 and vy < -0.1:
        return 4
    return -1


class Env:
    def __init__(self):

        self._env = Emulator()
        self._runtime = jpype.java.lang.Runtime.getRuntime()
        self.move_action = [[0, 0], [-1, 0], [1, 0], [0, -1], [0, 1]]  # 1：<-，2:-> 3:↓  4:↑
        self.initial_height = 0.0
        self.min_bound = 0
        self.max_bound = 19
        self.agent_num = 20
        self.agent_pos = [[] for _ in range(self.agent_num)]
        self.velocity_list = [[] for _ in range(self.agent_num)]
        self.acc_cmd_table = solve_acc()

    def discretize_position(self, x, y):  # 一格的长度表示20
        return int(round(x)) // 20, int(round(y)) // 20

    def continuous_position(self, x, y):
        return x * 20.0 + 10, y * 20.0 + 10

    def get_observation(self):
        obs = self._env.getObs()
        obs_json = json.loads(str(obs))
        json_arr = obs_json['objects']
        sort_list = []
        for obj in json_arr:
            discretized_pos_x, discretized_pos_y = self.discretize_position(obj['pos'][0], obj['pos'][1])
            self.velocity_list[int(obj['id'])] = [obj['linear_vel'][0], obj['linear_vel'][1]]
            sort_list.append([discretized_pos_x, discretized_pos_y, int(obj['id'])])
        sort_list.sort()
        obs_list = []
        for i in range(self.agent_num):
            single_list = []
            for obs in sort_list:
                if obs[2] == i:
                    single_list.append(i)
                    single_list.append(obs[0])
                    single_list.append(obs[1])
                    self.agent_pos[i] = [obs[0], obs[1]]  # 环境里保存格子的位置
                    break
            for obs in sort_list:
                if obs[2] != i:
                    single_list.append(obs[0])
                    single_list.append(obs[1])
            obs_list.append(single_list)
        return obs_list

    def step(self, action):
        cmd_list = []
        for i in range(self.agent_num):
            start_state = velocity_to_state(self.velocity_list[i][0], self.velocity_list[i][1])
            end_state = action_to_state(int(action[i]))
            acc_cmd = self.acc_cmd_table[start_state][end_state]
            acc_x_list = acc_cmd[0]
            acc_y_list = acc_cmd[1]
            cmd_list.append(
                self.moveOneGrid(str(i), acc_x_list[0], acc_x_list[1], acc_x_list[2], acc_y_list[0], acc_y_list[1],
                                 acc_y_list[2]))
        self._env.step(json.dumps(cmd_list))  # 环境里执行action
        return self.get_observation()

    def reset(self):
        self._env.reset()
        pos_set = set()
        for i in range(self.agent_num):
            now = np.random.randint(self.min_bound, self.max_bound, (2, ))
            now_tuple = (int(now[0]), int(now[1]))
            while now_tuple in pos_set:
                now = np.random.randint(self.min_bound, self.max_bound, (2,))
                now_tuple = (int(now[0]), int(now[1]))
            pos_set.add(now_tuple)
            String = jpype.JClass('java.lang.String')
            self.agent_pos[i] = [now_tuple[0], now_tuple[1]]
            pos_x, pos_y = self.continuous_position(now_tuple[0], now_tuple[1])
            self._env.addOneUav(String(str(i)), float(pos_x), float(pos_y), float(50.0))
        #起飞
        # cmd_list = []
        # for i in range(self.agent_num):
        #     cmd_list.append(self.takeoff(str(i), self.initial_height))
        # self._env.step(json.dumps(cmd_list))
        return self.get_observation()

    def terminal_state(self):
        # 距离最远的点 距离不超过C
        dist = -1
        for i in range(self.agent_num):
            for j in range(i + 1, self.agent_num):
                d = np.abs(self.agent_pos[i][0] - self.agent_pos[j][0]) + np.abs(
                    self.agent_pos[i][1] - self.agent_pos[j][1])
                if d > dist:
                    dist = d
        return dist <= 12

    def takeoff(self, vehicle_name, height=10.0, timeout=9999999, _async=False):
        request = {}
        request['objectID'] = vehicle_name
        request['messageID'] = str(uuid.uuid1())
        request['function'] = 'takeoff'
        request['height'] = height
        request['timeout'] = timeout
        request['async'] = _async
        return request

    def moveOneGrid(self, vehicle_name, acc1x, acc2x, acc3x, acc1y, acc2y, acc3y):
        request = {}
        request['objectID'] = vehicle_name
        request['messageID'] = str(uuid.uuid1())
        request['function'] = 'moveOneGrid'
        request['acc1x'] = acc1x
        request['acc2x'] = acc2x
        request['acc3x'] = acc3x
        request['acc1y'] = acc1y
        request['acc2y'] = acc2y
        request['acc3y'] = acc3y
        return request