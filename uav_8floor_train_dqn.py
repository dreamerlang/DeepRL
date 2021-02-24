import torch
import torch.nn as nn
import gym
import numpy as np
from uav_8floor_dqn import DQNAgent
from ddqn import DDQNAgent
from deeprl_util.args import DQNArgs, DDQNArgs
from deeprl_util.preprocessing import SimpleNormalizer
from uav_8floor_env import Env


class QNet(nn.Module):

    def __init__(self, state_shape, action_cnt):
        super().__init__()
        self.fc0 = nn.Linear(state_shape, 128)
        self.fc1 = nn.Linear(128, 64)
        self.fc2 = nn.Linear(64, action_cnt)

    def forward(self, x):
        x = torch.tanh(self.fc0(x))
        x = torch.tanh(self.fc1(x))
        x = self.fc2(x)
        return x


def train_dqn(env_name):
    args = DQNArgs()
    args.lr = 5e-5

    args.env_name = env_name
    args.log_dir = './logs/dqn/{}'.format(env_name)
    args.save_dir = './result/dqn/{}'.format(env_name)
    env = Env()
    agent = DQNAgent(env, QNet, SimpleNormalizer, args)
    pre_best = -1e9
    for ep in range(args.max_ep):
        agent.train_one_episode()
        if ep != 0 and ep % args.test_interval == 0:
            r = agent.test_model()
            if r > pre_best:
                pre_best = r
                agent.save(args.save_dir)
    env.close()


def test_dqn():
    args = DQNArgs()
    env = gym.make(args.env_name)
    agent = DQNAgent(env, QNet, SimpleNormalizer, args)
    agent.load(args.save_dir)
    for _ in range(10):
        agent.test_one_episode(True)


if __name__ == '__main__':
    env_name = input('input env name:')
    train_dqn(env_name)
    # test_dqn()
    # train_ddqn()
    # train_dqn()
