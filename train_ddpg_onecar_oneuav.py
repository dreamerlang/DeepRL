from deeprl_util.args import DDPGArgs
from deeprl_util.preprocessing import SimpleNormalizer
from model.actor import DDPGActor
from model.qnet import DDPGQNet
from ddpg import DDPGAgent
from emulator_env import Env
import os


def train_ddpg_with_onecar_oneuav():
    args = DDPGArgs()
    env = Env()
    agent = DDPGAgent(env, DDPGQNet, DDPGActor, SimpleNormalizer, args)
    max_reward = 0
    for ep in range(args.max_ep):
        agent.train_one_episode()
        if ep % args.test_interval == 0:
            mean_reward = agent.test_model()
            if mean_reward > max_reward:
                max_reward = mean_reward
                print('max_reward:{}'.format(max_reward))
                dir = './result/ddpg/' + args.env_name + '/'
                if not os.path.exists(dir):
                    os.makedirs(dir)
                agent.save(dir)
    env.close()


if __name__ == '__main__':
    train_ddpg_with_onecar_oneuav()
