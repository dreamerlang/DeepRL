import jpype
import json
import uuid
import random
import math
from sympy import *

jpype.startJVM(classpath=['/Users/hulang/IdeaProjects/UXVSimulator/target/UXVSim-1.0-SNAPSHOT-jar-with-dependencies.jar'])
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
        self._target_x = 0
        self._target_y = 0
        self.move_action = [[0, 0], [-1, 0], [1, 0], [0, -1], [0, 1]]  # 1：<-，2:-> 3:↓  4:↑
        self.initial_height = 0.0
        self.min_bound = 0
        self.max_bound = 9
        self.agent_pos = [[], [], [], []]
        self.velocity_list = [[0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0]]
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
            self.velocity_list[int(obj['id'])][0] = obj['linear_vel'][0]  # 保存无人机的速度信息
            self.velocity_list[int(obj['id'])][1] = obj['linear_vel'][1]
            sort_list.append([discretized_pos_x, discretized_pos_y, int(obj['id'])])
        sort_list.sort()
        obs_list = []
        for i in range(0, 4):
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
            single_list.append(self._target_x)
            single_list.append(self._target_y)
            obs_list.append(single_list)
        return obs_list

    def step(self, action):
        # print(action)
        obs_list = self.get_observation()
        # print(obs_list)
        cmd_list = []
        for i in range(4):
            if int(action[i]) == 0:  # action为0时表示不动
                continue
            new_grid_x = int(obs_list[i][1]) + self.move_action[int(action[i])][0]
            if new_grid_x < self.min_bound or new_grid_x > self.max_bound:
                continue
            new_grid_y = int(obs_list[i][2]) + self.move_action[int(action[i])][1]
            if new_grid_y < self.min_bound or new_grid_y > self.max_bound:
                continue
            new_pos_x, new_pos_y = self.continuous_position(new_grid_x, new_grid_y)
            cmd_list.append(self.moveToPosition(str(i), 8.0, new_pos_x, new_pos_y, self.initial_height, False))
        self._env.step(json.dumps(cmd_list))  # 环境里执行action
        return self.get_observation()

    def step_for_queue(self, action):
        # print(action)
        obs_list = self.get_observation()
        # print(obs_list)
        cmd_list = []
        for i in range(4):
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
        random_x = random.randint(self.min_bound, self.max_bound)
        while random_x == self.min_bound or random_x == self.max_bound:
            random_x = random.randint(self.min_bound, self.max_bound)
        random_y = random.randint(self.min_bound, self.max_bound)
        while random_y == self.min_bound or random_y == self.max_bound:
            random_y = random.randint(self.min_bound, self.max_bound)
        self._target_x = random_x
        self._target_y = random_y
        String = jpype.JClass('java.lang.String')
        random_x = random.randint(self.min_bound, self.max_bound)
        random_y = random.randint(self.min_bound, self.max_bound)
        pos_x, pos_y = self.continuous_position(random_x, random_y)
        self._env.addOneUav(String("0"), float(pos_x), float(pos_y), float(0.0))
        random_x = random.randint(self.min_bound, self.max_bound)
        random_y = random.randint(self.min_bound, self.max_bound)
        pos_x, pos_y = self.continuous_position(random_x, random_y)
        self._env.addOneUav(String("1"), float(pos_x), float(pos_y), float(0.0))
        random_x = random.randint(self.min_bound, self.max_bound)
        random_y = random.randint(self.min_bound, self.max_bound)
        pos_x, pos_y = self.continuous_position(random_x, random_y)
        self._env.addOneUav(String("2"), float(pos_x), float(pos_y), float(0.0))
        random_x = random.randint(self.min_bound, self.max_bound)
        random_y = random.randint(self.min_bound, self.max_bound)
        pos_x, pos_y = self.continuous_position(random_x, random_y)
        self._env.addOneUav(String("3"), float(pos_x), float(pos_y), float(0.0))
        # 起飞
        # cmd_list = []
        # for i in range(0, 4):
        #     cmd_list.append(self.takeoff(str(i), self.initial_height))
        # self._env.step(json.dumps(cmd_list))
        return self.get_observation()

    def terminal_state(self):
        needed_pos = [
            [self._target_x - 1, self._target_y],
            [self._target_x + 1, self._target_y],
            [self._target_x, self._target_y - 1],
            [self._target_x, self._target_y + 1]
        ]
        # print('needed_pos:')
        # print(needed_pos)
        # print('agent_pos:')
        # print(self.agent_pos)
        used = [False] * 4
        for j in range(4):
            for v in self.agent_pos:
                if v[0] == needed_pos[j][0] and v[1] == needed_pos[j][1]:
                    used[j] = True
        return all(used)

    def moveToPosition(self, vehicle_name, velocity, x, y, z, _async):
        request = {}
        request['objectID'] = vehicle_name
        request['messageID'] = str(uuid.uuid1())
        request['function'] = 'moveToPosition'
        request['velocity'] = velocity
        request['position_x'] = x
        request['position_y'] = y
        request['position_z'] = z
        request['async'] = _async
        return request

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
