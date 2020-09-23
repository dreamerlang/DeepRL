import jpype
import json
import numpy as np
import uuid
from gym import spaces

jpype.startJVM(classpath=['./jars/UXVSim-1.0-SNAPSHOT-jar-with-dependencies.jar'])
Emulator = jpype.JClass("uxvsim.Emulator")


class Env:

    def __init__(self):
        self._env = Emulator()
        self._runtime = jpype.java.lang.Runtime.getRuntime()
        self.max_speed = 8
        self.max_bound = 1000
        self.step_cnt = 0
        self.observation_space = spaces.Box(
            low=-self.max_bound,
            high=self.max_bound, shape=(6,),
            dtype=np.float32
        )
        self.action_space = spaces.Box(
            low=-self.max_speed,
            high=self.max_speed, shape=(2,),
            dtype=np.float32
        )

    def get_reward(self, dis_square):
        return -dis_square / 100.0

    def step(self, action):  # step  return a tuple（state_, reward, done, _）
        cmd_list = [self.moveByVelocity('uav0', float(action[0]), float(action[1]), 0.0, 1.0, True)]
        new_state_str = self._env.step(json.dumps(cmd_list))
        self.step_cnt += 1
        print('step:' + str(self.step_cnt))
        new_state_json = json.loads(str(new_state_str))
        uav_x, uav_y, uav_z = new_state_json[0], new_state_json[1], new_state_json[2]
        ugv_x, ugv_y, ugv_z = new_state_json[3], new_state_json[4], new_state_json[5]
        dis_square = (uav_x - ugv_x) ** 2 + (uav_y - ugv_y) ** 2
        reward = self.get_reward(dis_square)
        done = False
        if dis_square <= 1 or self.step_cnt >= 200:
            done = True
            self.step_cnt = 0
        state_ = np.array([uav_x, uav_y, uav_z, ugv_x, ugv_y, ugv_z], dtype=np.float32)
        info = {}
        return state_, reward, done, info

    def get_observation(self):
        obs = self._env.getObs()
        return json.loads(str(obs))

    def reset(self):
        # del self._env
        self._env.reset()
        obs_str = self._env.getObs()
        obs = json.loads(str(obs_str))
        # uav+uvg
        return np.array(obs['objects'][0]['pos'] + obs['objects'][1]['pos'], dtype=np.float32)

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
