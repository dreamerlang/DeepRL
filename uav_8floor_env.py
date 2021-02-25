import json
import uuid
import copy
import numpy as np
import time
import jpype

jpype.startJVM(
    classpath=['/Users/hulang/IdeaProjects/UXVSimulator/target/UXVSim-1.0-SNAPSHOT-jar-with-dependencies.jar'])
Emulator = jpype.JClass("uxvsim.Emulator")


class Env:
    def __init__(self):
        self._env = Emulator()
        self._runtime = jpype.java.lang.Runtime.getRuntime()
        self.agent_num = 2
        self.agent_pos = [[] for _ in range(self.agent_num)]  # 存储无人机的当前位置信息
        self.env_info = []  # TODO 环境信息未知
        self.target_x = 32.5
        self.target_y = 3
        self.step_cnt = 0
        self.max_step = 1000
        self.min_x_bound = 0.0
        self.max_x_bound = 57.0
        self.min_y_bound = 0.0
        self.max_y_bound = 28.0
        self.min_z_bound = 0.0
        self.max_z_bound = 3.0

    def reset(self):
        self._env.reset()
        self.step_cnt = 0
        init_list = [[21, 12], [23, 14]]
        # cnt = 0
        # while cnt < self.agent_num:
        #     init_pos = [np.random.uniform(19, 25), np.random.uniform(8, 16)]
        #     if len(init_list) == 0:
        #         init_list.append(init_pos)
        #         cnt += 1
        #     else:
        #         can_add = True
        #         for pos in init_list:
        #             if (pos[0] - init_pos[0]) ** 2 + (pos[1] - init_pos[1]) ** 2 <= 0.3 ** 2:
        #                 can_add = False
        #                 break
        #         if can_add:
        #             init_list.append(init_pos)
        #             cnt += 1

        self.agent_pos = [[] for _ in range(self.agent_num)]  # 清空一下数组
        for i in range(self.agent_num):
            String = jpype.JClass('java.lang.String')
            self._env.addOneUav(String(str(i)), float(init_list[i][0]), float(init_list[i][1]), float(1.5))
            self.agent_pos[i].append(init_list[i][0])
            self.agent_pos[i].append(init_list[i][1])
            self.agent_pos[i].append(1.5)
        return self.get_observation()

    def get_observation(self):
        obs = self._env.getObs()
        obs_json = json.loads(str(obs))
        json_arr = obs_json['objects']
        obs_list = []
        for obj in json_arr:
            if obj['type'] != 'uav':
                continue
            # 限制范围
            pos_x, pos_y = obj['pos'][0], obj['pos'][1]
            if pos_x < self.min_x_bound:
                pos_x = self.min_x_bound
            elif pos_x > self.max_x_bound:
                pos_x = self.max_x_bound
            if pos_y < self.min_y_bound:
                pos_y = self.min_y_bound
            elif pos_y > self.max_y_bound:
                pos_y = self.max_y_bound
            self.agent_pos[int(obj['id'])][0], self.agent_pos[int(obj['id'])][1] = pos_x, pos_y
        for pos in self.agent_pos:
            obs_list.append(pos[0])
            obs_list.append(pos[1])
        return obs_list  # TODO obs是否还需要其他信息

    def step(self, action):  # action[] 5*2=10 action取值范围为0到9 ，0，1时代表无人机静止
        pre_state = copy.deepcopy(self.agent_pos)
        cmd_list = []
        for i in range(self.agent_num):
            if int(action[i] == 2):  # 向前飞20cm
                cmd_list.append(
                    self.moveToPosition(str(i), 0.2, self.agent_pos[i][0] + 0.2,
                                        self.agent_pos[i][1], self.agent_pos[i][2]))
            elif int(action[i] == 3):  # 向前飞50cm
                cmd_list.append(
                    self.moveToPosition(str(i), 0.5, self.agent_pos[i][0] + 0.5,
                                        self.agent_pos[i][1], self.agent_pos[i][2]))
            elif int(action[i] == 4):  # 向后飞20cm
                cmd_list.append(
                    self.moveToPosition(str(i), 0.2, self.agent_pos[i][0] - 0.2,
                                        self.agent_pos[i][1], self.agent_pos[i][2]))
            elif int(action[i] == 5):  # 向后飞50cm
                cmd_list.append(
                    self.moveToPosition(str(i), 0.5, self.agent_pos[i][0] - 0.5,
                                        self.agent_pos[i][1], self.agent_pos[i][2]))
            elif int(action[i] == 6):  # 向左飞20cm
                cmd_list.append(
                    self.moveToPosition(str(i), 0.2, self.agent_pos[i][0],
                                        self.agent_pos[i][1] + 0.2, self.agent_pos[i][2]))
            elif int(action[i] == 7):  # 向左飞50cm
                cmd_list.append(
                    self.moveToPosition(str(i), 0.5, self.agent_pos[i][0],
                                        self.agent_pos[i][1] + 0.5, self.agent_pos[i][2]))

            elif int(action[i] == 8):  # 向右飞20cm
                cmd_list.append(
                    self.moveToPosition(str(i), 0.2, self.agent_pos[i][0],
                                        self.agent_pos[i][1] - 0.2, self.agent_pos[i][2]))
            elif int(action[i] == 9):  # 向右飞50cm
                cmd_list.append(
                    self.moveToPosition(str(i), 0.5, self.agent_pos[i][0],
                                        self.agent_pos[i][1] - 0.5, self.agent_pos[i][2]))
            # elif int(action[i] == 10):  # 向上飞20cm
            #     cmd_list.append(
            #         self.moveToPosition(str(i), 0.2, self.agent_pos[i][0],
            #                             self.agent_pos[i][1], self.agent_pos[i][2] + 0.2))
            # elif int(action[i] == 11):  # 向上飞50cm
            #     cmd_list.append(
            #         self.moveToPosition(str(i), 0.5, self.agent_pos[i][0],
            #                             self.agent_pos[i][1], self.agent_pos[i][2] + 0.5))
            # elif int(action[i] == 12):  # 向下飞20cm
            #     cmd_list.append(
            #         self.moveToPosition(str(i), 0.2, self.agent_pos[i][0],
            #                             self.agent_pos[i][1], self.agent_pos[i][2] - 0.2))
            # elif int(action[i] == 13):  # 向下飞50cm
            #     cmd_list.append(
            #         self.moveToPosition(str(i), 0.5, self.agent_pos[i][0],
            #                             self.agent_pos[i][1], self.agent_pos[i][2] - 0.5))
        # t1 = time.time()
        done = bool(self._env.stepFor8Floor(json.dumps(cmd_list)))  # 环境里执行action
        # t2 = time.time()
        # print("cmd_list:{}".format(cmd_list))
        # print("time:{}".format(t2 - t1))
        state_ = self.get_observation()
        if done:  # 如果发生碰撞
            print('collision')
            print("step_cnt:{}".format(self.step_cnt))
            return state_, -300, done, {}

        # 如果超过这个范围
        for i in range(self.agent_num):
            if state_[i * 2] < 0.1 + self.min_x_bound or state_[i * 2] > self.max_x_bound - 0.1 or state_[
                i * 2 + 1] < 0.1 + self.min_y_bound or state_[i * 2 + 1] > self.max_y_bound - 0.1:
                print("step_cnt:{}".format(self.step_cnt))
                print('out of range')
                print(state_)
                return state_, -300, True, {}

        reward = 0
        for i in range(self.agent_num):
            d_pre = (pre_state[i][0] - self.target_x) ** 2 + (pre_state[i][1] - self.target_y) ** 2
            d_next = (state_[i * 2] - self.target_x) ** 2 + (state_[i * 2 + 1] - self.target_y) ** 2
            reward += d_pre - d_next
        # 某两辆无人机距离较近时气流会干扰真机飞行
        for i in range(self.agent_num):
            for j in range(i + 1, self.agent_num):
                if (self.agent_pos[i][0] - self.agent_pos[j][0]) ** 2 + (
                        self.agent_pos[i][1] - self.agent_pos[j][1]) ** 2 <= 0.3 ** 2:
                    reward -= 50
        done = self.terminal_state()
        if done:
            print('the eps succeed')
            reward += 200 * self.agent_num

        self.step_cnt += 1
        if self.step_cnt >= self.max_step:
            done = True
        return state_, reward, done, {}

    def terminal_state(self):
        x_range = 3
        y_range = 6
        done = True
        for i in range(self.agent_num):
            if np.abs(self.agent_pos[i][0] - self.target_x) > x_range / 2.0 or np.abs(
                    self.agent_pos[i][1] - self.target_y) > y_range / 2.0:
                done = False
                break
        return done

    def moveToPosition(self, vehicle_name, velocity, x, y, z):
        request = {}
        request['objectID'] = vehicle_name
        request['messageID'] = str(uuid.uuid1())
        request['function'] = 'moveToPosition'
        request['async'] = False
        request['velocity'] = velocity
        request['position_x'] = x
        request['position_y'] = y
        request['position_z'] = z
        return request

    def sample(self):
        return np.random.randint(0, 10)

    def close(self):
        self._env.close()
