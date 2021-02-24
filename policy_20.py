from collections import defaultdict
import numpy as np


def modify_actions(states, actions):
    MAP_SIZE = 20
    N_AGENTS = 20
    positions = []
    for s in states:
        positions.append([int(s[1]), int(s[2])])
    positions = np.array(positions)
    
    dirs = [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)]
    not_move = [False] * 20
    cnt = 0
    prev_not_move = not_move.count(True)
    while True:
        cnt += 1
        print(f'In LOOP: {cnt}')
        positions_cnt = defaultdict(int)
        for i in range(20):
            if not_move[i]:
                next_position = positions[i]
            else:
                next_position = positions[i] + dirs[actions[i]]
            np.clip(next_position, 0, MAP_SIZE - 1, next_position)
            tmp = (int(next_position[0]), int(next_position[1]))
            positions_cnt[tmp] += 1
        for i in range(N_AGENTS):
            if not_move[i]:
                next_position = positions[i]
            else:
                next_position = positions[i] + dirs[actions[i]]
            np.clip(next_position, 0, MAP_SIZE - 1, next_position)

            # double check not move agents
            if positions[i][0] == next_position[0] and positions[i][1] == next_position[1]:
                not_move[i] = True

            tmp = (int(next_position[0]), int(next_position[1]))
            if positions_cnt[tmp] > 1:
                not_move[i] = True

        now_not_move = not_move.count(True)
        if now_not_move > prev_not_move:
            pass
        else:
            break
        prev_not_move = now_not_move

    result = []
    for i in range(N_AGENTS):
        if not_move[i]:
            result.append(0)
        else:
            result.append(actions[i])
    return result


import torch
import torch.nn as nn


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
    
net = QNet(41, 5)
net.load_state_dict(torch.load('./trained_models/95600.pkl'))


def choose_action(state):
    s = torch.tensor([state]).float()
    with torch.no_grad():
        q_val = net(s).numpy()[0]
    return np.argmax(q_val)


def policy(states):
    actions = []
    for s in states:
        actions.append(choose_action(s))
    return modify_actions(states, actions)  # no collision
    # return actions
    
    
# def main():
#     # Tutorial
#     env = EnvWithEntropy(20, 0.0)
#     states = env.reset()
#     done = False
#     total = 0
#     while not done:
#         actions = policy(states)
#         states, reward, done, info = env.step(actions)
#         total += reward
#     print(info)
#     print(f'Total Reward: {total}')