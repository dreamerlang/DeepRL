import jpype
import json
import random
import numpy as np
import uuid
from gym import spaces
import random

jpype.startJVM(classpath=['./jars/UXVSim-1.0-SNAPSHOT-jar-with-dependencies.jar'])
Emulator = jpype.JClass("uxvsim.Emulator")


class Env:
    def __init__(self):
        self._env = Emulator()
        self._runtime = jpype.java.lang.Runtime.getRuntime()
        self._target_x = 0
        self._target_y = 0
        self.reset()

    def discretize_position(self, x, y):  #一格的长度表示20
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
        for i in range(0, 5):
            single_list = []
            for obs in sort_list:
                if obs[2] == i:
                    single_list.append(i)
                    single_list.append(obs[0])
                    single_list.append(obs[1])
                    break
            for obs in sort_list:
                if obs[2] != i:
                    single_list.append(obs[0])
                    single_list.append(obs[1])
            single_list.append(self._target_x)
            single_list.append(self._target_y)
            obs_list.append(single_list)
        return obs_list

    def step(self):  #TODO
        pass

    def reset(self):
        random_x = random.randint(0, 10)
        while random_x == 0 or random_x == 9:
            random_x = random.randint(0, 10)
        random_y = random.randint(0, 10)
        while random_y == 0 or random_y == 9:
            random_y = random.randint(0, 10)
        self._target_x=random_x
        self._target_y=random_y
