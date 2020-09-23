class DDPGArgs:

    def __init__(self):
        self.exp_cap = 1000000  #经验池的容量
        self.gamma = 0.95
        self.batch = 128  #抽取的样本训练个数
        self.test_interval = 32  #多少轮进行一次测试
        self.update_cnt = 200  #更新的次数
        self.update_interval = 200  #多少步更新一次
        self.actor_lr = 1e-4  #策略网络的学习率
        self.critic_lr = 5e-3  #值函数的学习率

        self.env_name = input('input env name: ')  #标示每次的实验
        self.action_bound = float(input('input action bound: ')) #动作输出的最大值
        self.max_ep = int(input('input max train episode: ')) #最多训练多少轮
        self.scale = float(input('input scale: ')) #探索的标准差 0.1到1

        self.log_dir = './logs/ddpg/{}'.format(self.env_name) #tensorboard路径
        self.save_path = './result/ddpg/{}'.format(self.env_name) #模型


class DQNArgs:

    def __init__(self):
        self.exp_cap = 1000000
        self.gamma = 0.99
        self.batch = 32
        self.tau = 64
        self.max_ep = 2000
        self.log_interval = 1000
        self.test_interval = 32
        self.lr = 5e-4
        self.epsilon = 0.1
        self.env_name = 'LunarLander-v2'
        self.log_dir = './logs/dqn/{}'.format(self.env_name)
        self.save_dir = './result/dqn/{}'.format(self.env_name)


class DDQNArgs:

    def __init__(self):
        self.exp_cap = 1000000
        self.gamma = 0.99
        self.batch = 32
        self.tau = 32
        self.max_ep = 4000
        self.log_interval = 1000
        self.test_interval = 32
        self.lr = 5e-4
        self.max_epsilon = 0.1
        self.min_epsilon = 0.1
        self.epsilon_decay = 0.5 / 500
        self.env_name = 'LunarLander-v2'
        self.log_dir = './logs/ddqn/{}-soft'.format(self.env_name)
        self.save_dir = './result/ddqn/{}-soft'.format(self.env_name)
