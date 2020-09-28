import torch
import numpy as np
from deeprl_util.preprocessing import SimpleNormalizer
import time

from emulator_env import Env
from model.actor import DDPGActor


class EvalDDPGAgent:

    def __init__(self, pnet_cls, preprocessing_cls, eval_env, action_bound):
        self.state_dim, self.action_dim = eval_env.observation_space.shape, eval_env.action_space.shape[0]
        self._actor = pnet_cls(self.state_dim, self.action_dim)
        self._pre = preprocessing_cls(eval_env)
        self._env = eval_env
        self._action_bound = action_bound

    def choose_action(self, state):
        with torch.no_grad():
            state = torch.from_numpy(state).float()
            action = self._actor(state)
        action = action.detach().numpy()
        return action  # np.array([0.0,0.0,0.0],dtype=float)

    def _eval(self):
        state = self._env.reset()
        done = False
        total_reward = 0
        while not done:
            action = self.choose_action(self._pre.transform(state))
            state_, reward, done, _ = self._env.step(action * self._action_bound)  # 环境里也需要约束速度大小
            state = state_
            total_reward += reward
        return total_reward

    def run_eval(self, network_path, norm_dir, n):
        state_dict = torch.load(network_path)
        self._actor.load_state_dict(state_dict)
        self._pre.load(norm_dir)
        r = [self._eval() for _ in range(n)]
        return np.mean(r)
