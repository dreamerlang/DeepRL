import jpype
import json
import uuid
import random

jpype.startJVM(classpath=['./jars/UXVSim-1.0-SNAPSHOT-jar-with-dependencies.jar'])
Emulator = jpype.JClass("uxvsim.Emulator")


class Env:
    def __init__(self):
        self._env = Emulator()
        self._runtime = jpype.java.lang.Runtime.getRuntime()
        self._target_x = 0
        self._target_y = 0
        self.move_action = [[0, 0], [-1, 0], [1, 0], [0, -1], [0, 1]]
        self.initial_height = 0.0
        self.min_bound = 0
        self.max_bound = 9
        self.agent_pos = [[], [], [], []]

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
        print(action)
        obs_list = self.get_observation()
        print(obs_list)
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
            [self._target_x-1, self._target_y],
            [self._target_x+1, self._target_y],
            [self._target_x, self._target_y-1],
            [self._target_x, self._target_y+1]
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

        # used = [False] * 4
        # for v in self.agent_pos:
        #     for j in range(4):
        #         if v[0] == needed_pos[j][0] and v[1] == needed_pos[j][1]:
        #             used[j] = True
        # return all(used)

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
