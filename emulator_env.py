import jpype
import json
import numpy as np
import uuid
from gym import spaces
import random

jpype.startJVM(classpath=['./jars/UXVSim-1.0-SNAPSHOT-jar-with-dependencies.jar'])
Emulator = jpype.JClass("uxvsim.Emulator")


class Env:
    CAN_SEE_RANGE = 20
    MAX_STEP_CNT = 200

    def __init__(self):
        self._env = Emulator()
        self._runtime = jpype.java.lang.Runtime.getRuntime()
        self.max_speed = 10
        self.max_bound = 1000
        self.step_cnt = 0
        self.loss_cnt = 0
        self.observation_space = spaces.Box(
            low=-self.max_bound,
            high=self.max_bound, shape=(4,),
            dtype=np.float32
        )
        self.action_space = spaces.Box(
            low=-self.max_speed,
            high=self.max_speed, shape=(2,),
            dtype=np.float32
        )

    def get_reward(self, uav_x, uav_y, ugv_x, ugv_y):
        if (uav_x - ugv_x) ** 2 + (uav_y - ugv_y) ** 2 <= Env.CAN_SEE_RANGE ** 2:
            return 1
        return 0

    def step(self, action):  # step  return a tuple（state_, reward, done, _）
        cmd_list = [self.moveByVelocity('uav0', float(action[0]), float(action[1]), 0.0, 1.0, True),
                    self.moveToPosition('ugv0', 5, random.uniform(-50, 50), random.uniform(-50, 50), 0, False)]
        self._env.step_one_car_one_uav(json.dumps(cmd_list))  # 原jar包代码有更改，这个场景调用step_one_car_one_uav
        self.step_cnt += 1
        print('step:' + str(self.step_cnt))
        world_info_json = json.loads(str(self._env.getObs()))
        json_arr = world_info_json['objects']
        uav_x, uav_y = 0.0, 0.0
        ugv_x, ugv_y = 0.0, 0.0
        for obj in json_arr:
            if obj['id'] == 'uav0':
                uav_x, uav_y = obj['pos'][0], obj['pos'][1]
            elif obj['id'] == 'ugv0':
                ugv_x, ugv_y = obj['pos'][0], obj['pos'][1]
        reward = self.get_reward(uav_x, uav_y, ugv_x, ugv_y)
        if reward == 1:
            self.loss_cnt = 0
        else:
            self.loss_cnt += 1
        state_ = np.array([uav_x, uav_y, ugv_x, ugv_y], dtype=np.float32)
        info = {}
        done = False
        if self.step_cnt == Env.MAX_STEP_CNT or self.loss_cnt > 10:
            done = True
        return state_, reward, done, info

    def get_observation(self):
        obs = self._env.getObs()
        return json.loads(str(obs))

    def reset(self):
        # reset self._env
        self._env.reset()
        self.step_cnt = 0
        self.loss_cnt = 0
        String = jpype.JClass('java.lang.String')
        self._env.addOneUav(String("uav0"), float(0.0), float(0.0), float(0.0))
        self._env.addOneUgv(String("ugv0"), float(1200), float(250000), float(0.0), float(0.0), float(0.0))
        obs_str = self._env.getObs()
        obs = json.loads(str(obs_str))
        # uav+uvg
        return np.array([obs['objects'][0]['pos'][0], obs['objects'][0]['pos'][1], obs['objects'][1]['pos'][0],
                         obs['objects'][1]['pos'][1]], dtype=np.float32)

    def close(self):
        self._env.close()

    def get_jvm_memory(self):
        return self._runtime.totalMemory()

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

    def moveByVelocity(self, vehicle_name, vx, vy, vz, fly_time, _async):
        request = {}
        request['objectID'] = vehicle_name
        request['messageID'] = str(uuid.uuid1())
        request['function'] = 'moveByVelocity'
        request['vx'] = vx
        request['vy'] = vy
        request['vz'] = vz
        request['flyTime'] = fly_time
        request['async'] = _async
        return request
