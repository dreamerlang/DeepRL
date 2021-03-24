from gui.game import Game
from uav_8floor_train_dqn import QNet
from uav_8floor_env import Env
import torch
import numpy as np

qnet = QNet(4, 9)
qnet.load_state_dict(torch.load('./trained_models/45700.pkl'))
env=Env()

def choose_action(state):
    state = torch.Tensor([state]).float()
    with torch.no_grad():
        action = qnet(state).numpy()
    return np.argmax(action)

def normalize(state):  # 数据范围缩放到-1到1
    state_box = [[env.min_x_bound, env.max_x_bound], [env.min_y_bound, env.max_y_bound]]
    for i in range(len(state)):
        if i % 2 == 0:
            rate = (state[i] - state_box[0][0]) / (state_box[0][1] - state_box[0][0])
            state[i] = rate * 2 - 1
        elif i % 2 == 1:
            rate = (state[i] - state_box[1][0]) / (state_box[1][1] - state_box[1][0])
            state[i] = rate * 2 - 1
    return state

def test_one_eps():
    state = env.reset()
    state = normalize(state)
    done = False
    total = 0
    while not done:
        actions = []
        for i in range(env.agent_num):
            single_state = [state[i * 2], state[i * 2 + 1]]
            for j in range(env.agent_num):
                if j != i:
                    single_state.append(state[j * 2])
                    single_state.append(state[j * 2 + 1])
            action = choose_action(single_state)
            actions.append(action)
        state_, reward, done, _ = env.step(actions)
        total += sum(reward)
        state = state_
        state = normalize(state)
    print('test episode finished, total reward={}'.format(total))

def main():

    game = Game()
    game.run()





if __name__ == '__main__':
    main()