import numpy as np
import torch
import torch.nn as nn


# NN
class QNet(torch.nn.Module):

    def __init__(self, state_dim, action_cnt):
        super().__init__()
        self._fc0 = nn.Linear(state_dim, 64)
        self._fc1 = nn.Linear(64, 64)
        self._fc2 = nn.Linear(64, action_cnt)

    def forward(self, x):
        x = torch.tanh(self._fc0(x))
        x = torch.tanh(self._fc1(x))
        x = self._fc2(x)
        return x


net = QNet(11, 5)
net.load_state_dict(torch.load('./models/45700.pkl'))


def choose_action(state):
    s = torch.tensor([state]).float()
    with torch.no_grad():
        q_val = net(s).numpy()[0]
    return np.argmax(q_val)


def policy(states):
    actions = []
    for s in states:
        actions.append(choose_action(s))
    return actions


# TODO: 使用方式
# 1. 修改模型加载路径（23行）
# 2. 使用方式可见main


def main():
    states = [
        [0] * 11,
        [1] * 11,
        [2] * 11,
        [3] * 11
    ]
    actions = policy(states)
    # actions 为长度为4的list，表示每一个智能体的动作
    # 动作定义为0，1，2，3，4，含义见文档
