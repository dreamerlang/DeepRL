import os

from uav_8floor_env import Env
import numpy as np
from sympy import *
import torch
from torch.autograd import Variable
from uav_8floor_train_dqn import QNet
import random
import numpy as np
from pyheatmap.heatmap import HeatMap
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D



def solve_acc():
    t = 1
    x_abs = 20
    v_abs = 10
    param_list=[[[[t,0,0,0,0],[t,0,0,0,0]],[[t,x_abs,0,v_abs,5],[t,0,0,0,0]],[[t,-x_abs,0,-v_abs,-5],[t,0,0,0,0]],[[t,0,0,0,0],[t,x_abs,0,v_abs,5]],[[t,0,0,0,0],[t,-x_abs,0,-v_abs,-5]]],
                [[[t,0,v_abs,0,-5],[t,0,0,0,0]],[[t,x_abs,v_abs,v_abs,0],[t,0,0,0,0]],[[t,-x_abs,v_abs,-v_abs,-5],[t,0,0,0,0]],[[t,0,v_abs,0,-5],[t,x_abs,0,v_abs,5]],[[t,0,v_abs,0,-5],[t,-x_abs,0,-v_abs,-5]]],
                [[[t,0,-v_abs,0,5],[t,0,0,0,0]],[[t,x_abs,-v_abs,v_abs,5],[t,0,0,0,0]],[[t,-x_abs,-v_abs,-v_abs,0],[t,0,0,0,0]],[[t,0,-v_abs,0,5],[t,x_abs,0,v_abs,5]],[[t,0,-v_abs,0,5],[t,-x_abs,0,-v_abs,-5]]],
                [[[t,0,0,0,0],[t,0,v_abs,0,-5]],[[t,x_abs,0,v_abs,5],[t,0,v_abs,0,-5]],[[t,-x_abs,0,-v_abs,-5],[t,0,v_abs,0,-5]],[[t,0,0,0,0],[t,x_abs,v_abs,v_abs,0]],[[t,0,0,0,0],[t,-x_abs,v_abs,-v_abs,-5]]],
                [[[t,0,0,0,0],[t,0,-v_abs,0,5]],[[t,x_abs,0,v_abs,5],[t,0,-v_abs,0,5]],[[t,-x_abs,0,-v_abs,-5],[t,0,-v_abs,0,5]],[[t,0,0,0,0],[t,x_abs,-v_abs,v_abs,5]],[[t,0,0,0,0],[t,-x_abs,-v_abs,-v_abs,0]]]]  #t,x,v0,v1,b
    acc_cmd_table = []
    for i in range(5):
        list_i=[]
        for j in range(5):
            list_acc=[]
            print(i,j)
            x_list=param_list[i][j][0]
            t=x_list[0]
            x=x_list[1]
            v0 =x_list[2]
            v1=x_list[3]
            b=x_list[4]
            a1 = Symbol('a1')
            a2 = Symbol('a2')
            a3 = Symbol('a3')
            x_res_map=solve(
                [a1 - b, 6 * v0 * t + 5 * t * t * a1 + 3 * t * t * a2 + t * t * a3 - 2 * x, v0 + t * a1 + t * a2 + t * a3 - v1],
                [a1, a2, a3])
            print(x_res_map[a1],x_res_map[a2],x_res_map[a3])
            list_acc_x=[x_res_map[a1],x_res_map[a2],x_res_map[a3]]
            list_acc.append(list_acc_x)


            y_list=param_list[i][j][1]
            t=y_list[0]
            x=y_list[1]
            v0 =y_list[2]
            v1=y_list[3]
            b=y_list[4]
            y_res_map=solve(
                [a1 - b, 6 * v0 * t + 5 * t * t * a1 + 3 * t * t * a2 + t * t * a3 - 2 * x, v0 + t * a1 + t * a2 + t * a3 - v1],
                [a1, a2, a3])
            print(y_res_map[a1],y_res_map[a2],y_res_map[a3])
            list_acc_y = [y_res_map[a1],y_res_map[a2],y_res_map[a3]]
            list_acc.append(list_acc_y)
            list_i.append(list_acc)
        acc_cmd_table.append(list_i)

    print(acc_cmd_table)
    return acc_cmd_table


    # t = 1
    # x = 0
    # v0 = 10
    # v1 = 0
    # b = -5  #a1的值
    # a1 = Symbol('a1')
    # a2 = Symbol('a2')
    # a3 = Symbol('a3')
    # res_map=solve(
    #     [a1 - b, 6 * v0 * t + 5 * t * t * a1 + 3 * t * t * a2 + t * t * a3 - 2 * x, v0 + t * a1 + t * a2 + t * a3 - v1],
    #     [a1, a2, a3])
    # res_map[a1]
    # print(res_map[a1])
    # print(res_map[a2])
    # print(res_map[a3])

def test2(state):
    state[0]=1
    return state


if __name__ == '__main__':
    qnet=QNet(2,10)
    path = os.path.join('/Users/hulang/nju/s1/RL/DeepRL/result/dqn/test_no_building/', 'best.pkl')
    state_dict = torch.load(path)
    qnet.load_state_dict(state_dict)
    # state = torch.tensor([22.8400/57.0*2-1, 3.0998/28*2-1], dtype=torch.float32)
    # print(qnet.forward(state))
    x_list=[]
    y_list=[]
    data=[]
    # fig = plt.figure()
    # ax1 = plt.axes(projection='3d')
    for i in range(10000):
        x=random.uniform(-1,1)
        x_list.append(x)
        y=random.uniform(-1,1)
        y_list.append(y)
        state = torch.tensor([x,y], dtype=torch.float32)
        q_max=qnet.forward(state).max()
        # data.append(float(q_max))
        data.append([int((x+1)*1000),int((y+1)*1000),float(q_max)])
    heat = HeatMap(data)
    heat.heatmap(save_as="test_no_building2.png")  # 热图



    # solve_acc()
    # env = Env()
    # obs=env.reset()
    # print(obs)
    # print(env.step([11,0]))




    # env.step([1,1,1,1])  #向前
    # env.step([2, 2, 2, 2])  #向后
    # env.step([3, 3, 3, 3])  #向左
    # env.step([4, 4, 4, 4])  #向右
