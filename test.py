# from uav_queueing_env import Env
import numpy as np
from sympy import *


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



if __name__ == '__main__':
    solve_acc()
    # env = Env()
    # env.reset()
    # env.step([1,1,1,1])  #向前
    # env.step([2, 2, 2, 2])  #向后
    # env.step([3, 3, 3, 3])  #向左
    # env.step([4, 4, 4, 4])  #向右
