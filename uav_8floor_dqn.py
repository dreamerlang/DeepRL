import os
import time
import numpy as np
import torch
import torch.optim as optim
from torch.utils.tensorboard import SummaryWriter
from deeprl_util.buffer import ReplayBuffer


class DQNAgent:

    def __init__(self, env, qnet_cls, preprocessing_cls, args):
        self.env = env
        self.state_shape = env.agent_num * 3
        self.action_cnt = 14
        self.qnet = qnet_cls(self.state_shape, self.action_cnt)
        self.target_qnet = qnet_cls(self.state_shape, self.action_cnt)
        self.target_qnet.load_state_dict(self.qnet.state_dict())
        self.optim = optim.Adam(self.qnet.parameters(), lr=args.lr)
        self.loss_fn = torch.nn.MSELoss()
        self.args = args
        self.replay = []
        for i in range(self.env.agent_num):
            self.replay.append(ReplayBuffer(args.exp_cap, self.state_shape, 1))
        self.sw = SummaryWriter(self.args.log_dir)
        self.steps = 0  # 总步数
        self.episode = 0
        self._now_epsilon = args.max_epsilon
        if not os.path.exists(self.args.save_dir):
            os.mkdir(self.args.save_dir)

    def choose_action(self, state):
        state = torch.Tensor([state]).float()
        with torch.no_grad():
            action = self.qnet(state).numpy()
        return np.argmax(action)

    def choose_action_with_exploration(self, state):
        if np.random.uniform() < self._now_epsilon:
            return self.env.sample()
        return self.choose_action(state)

    def update(self):
        update_idx = np.random.randint(0, self.env.agent_num)  # 更新时随机选择一个replayBuffer的样本进行更新
        s, a, r, s_, d = self.replay[update_idx].sample(self.args.batch)
        with torch.no_grad():
            target = self.qnet(torch.Tensor(s))
            nxt_q = self.target_qnet(torch.Tensor(s_)).max(axis=1)[0]
            upd = self.args.gamma * nxt_q
            upd = torch.Tensor(r) + upd
            for i, v in enumerate(a):
                target[i, v] = r[i] if d[i] else upd[i]
        self.optim.zero_grad()
        q = self.qnet(torch.Tensor(s))
        loss = self.loss_fn(q, target)
        loss.backward()
        self.optim.step()
        self.hard_copy_parm()
        if self.steps % self.args.log_interval == 0:
            self.sw.add_scalar('loss/qloss', loss.item(), self.steps)

    def hard_copy_parm(self):
        if self.steps % self.args.tau == 0:
            self.target_qnet.load_state_dict(self.qnet.state_dict())

    def train_one_episode(self):
        state = self.env.reset()
        state = self.normalize(state)
        done = False
        total = 0
        while not done:
            actions = []
            for i in range(self.env.agent_num):
                single_state = []
                single_state.append(state[i * 3])
                single_state.append(state[i * 3 + 1])
                single_state.append(state[i * 3 + 2])
                for j in range(self.env.agent_num):
                    if j != i:
                        single_state.append(state[j * 3])
                        single_state.append(state[j * 3 + 1])
                        single_state.append(state[j * 3 + 2])
                single_action = self.choose_action_with_exploration(single_state)
                # print('single_action:{}'.format(single_action))
                actions.append(single_action)
            # t1=time.time()
            state_, reward, done, _ = self.env.step(actions)
            # t2 = time.time()
            # print("time:{}".format(t2-t1))
            state_ = self.normalize(state_)

            # 得到每个智能体的single_state与single_state_，并加入到buffer里
            for i in range(self.env.agent_num):
                single_state = []
                single_state_ = []
                single_state.append(state[i * 3])
                single_state.append(state[i * 3 + 1])
                single_state.append(state[i * 3 + 2])
                single_state_.append(state_[i * 3])
                single_state_.append(state_[i * 3 + 1])
                single_state_.append(state_[i * 3 + 2])
                for j in range(self.env.agent_num):
                    if j != i:
                        single_state.append(state[j * 3])
                        single_state.append(state[j * 3 + 1])
                        single_state.append(state[j * 3 + 2])
                        single_state_.append(state_[j * 3])
                        single_state_.append(state_[j * 3 + 1])
                        single_state_.append(state_[j * 3 + 2])
                self.replay[i].add(single_state, actions[i], reward, single_state_, done)
            total += reward
            self.update()
            state = state_
            self.steps += 1
        self.episode += 1
        print('train episode {} finished,total reward={}'.format(self.episode, total))
        self._now_epsilon -= self.args.epsilon_decay
        self._now_epsilon = max(self._now_epsilon, self.args.min_epsilon)
        self.sw.add_scalar('reward/train', total, self.episode)
        self._log_avg_q()
        return total

    def test_one_episode(self, viewer=False):
        state = self.env.reset()
        state = self.normalize(state)
        done = False
        total = 0
        while not done:
            actions = []
            for i in range(self.env.agent_num):
                action = self.choose_action(state)
                actions.append(action)
            state_, reward, done, _ = self.env.step(actions)
            state_ = self.normalize(state_)
            total += reward
            state = state_
            self.steps += 1
        print('test episode finished, total reward={}'.format(total))
        return total

    def test_model(self, cnt=10):
        r = [self.test_one_episode() for _ in range(cnt)]
        r_mean = np.mean(r)
        self.sw.add_scalar('reward/test', r_mean, self.episode)
        return r_mean

    def save(self, path):
        path = os.path.join(path, 'best.pkl')
        state_dict = self.qnet.state_dict()
        torch.save(state_dict, path)

    def load(self, path):
        path = os.path.join(path, 'best.pkl')
        state_dict = torch.load(path)
        self.qnet.load_state_dict(state_dict)

    def _log_avg_q(self):
        update_idx = np.random.randint(0, self.env.agent_num)
        s, *_ = self.replay[update_idx].sample(64)
        s_feed = torch.FloatTensor(s)
        with torch.no_grad():
            q = self.qnet(s_feed)
            val = q.mean().item()
        self.sw.add_scalar('avg_q', val, self.episode)

    def normalize(self, state):  # 数据范围缩放到-1到1
        state_box = [[self.env.min_x_bound, self.env.max_x_bound], [self.env.min_y_bound, self.env.max_y_bound],
                     [self.env.min_z_bound, self.env.max_z_bound]]
        for i in range(len(state)):
            if i % 3 == 0:
                rate = (state[i] - state_box[0][0]) / (state_box[0][1] - state_box[0][0])
                state[i] = rate * 2 - 1
            elif i % 3 == 1:
                rate = (state[i] - state_box[1][0]) / (state_box[1][1] - state_box[1][0])
                state[i] = rate * 2 - 1
            elif i % 3 == 2:
                rate = (state[i] - state_box[2][0]) / (state_box[2][1] - state_box[2][0])
                state[i] = rate * 2 - 1
        return state
