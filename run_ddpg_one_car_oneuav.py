import torch

from EvalDqnAgent import EvalDDPGAgent
from deeprl_util.args import DDPGArgs
from deeprl_util.preprocessing import SimpleNormalizer
from model.actor import DDPGActor
from model.qnet import DDPGQNet
from ddpg import DDPGAgent
from emulator_env import Env



if __name__ == '__main__':

    env = Env()
    eval_agent = EvalDDPGAgent(DDPGActor, SimpleNormalizer, env, 8)    #pnet_cls, eval_env, preprocessing_cls, action_bound
    network_path = './result/ddpg/test_8_velocity_20_canseerange/best.pkl'  # 文件的路径
    norm_path = './result/ddpg/test_8_velocity_20_canseerange/'  # 文件的目录的路径
    eval_reward = eval_agent.run_eval(network_path, norm_path, 50)  # 跑10轮
    print('Eval Reward: {}'.format(eval_reward))
    env.close()
