from uav_queue_env import Env
from policy_20 import policy
import time


if __name__ == '__main__':
    env = Env()
    success_cnt = 0
    ep=10
    for i in range(ep):
        print("ep:"+str(i))
        s = env.reset()
        print("reseted")
        step_cnt = 0
        while True:
            if env.terminal_state():
                print('success')
                success_cnt = success_cnt + 1
                break
            # print('t0:'+str(time.time()))
            print('Before policy')
            action = policy(s)
            print('policy')
            # print('t1:'+str(time.time()))
            s = env.step(action)
            print('step:'+str(step_cnt))
            # print('t2:'+str(time.time()))
            step_cnt = step_cnt + 1
            # print('t3:'+str(time.time()))
            if step_cnt > 200:
                break
    print('finish')
