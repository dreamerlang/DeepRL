from uav_queueing_env import Env
from policy import policy

if __name__ == '__main__':
    env = Env()
    success_cnt = 0
    ep=10
    for i in range(ep):
        print("ep:"+str(i))
        s = env.reset()
        step_cnt = 0
        while True:
            if env.terminal_state():
                print('success')
                success_cnt = success_cnt + 1
                break
            action = policy(s)
            s = env.step(action)
            step_cnt = step_cnt + 1
            print(step_cnt)
            if step_cnt > 200:
                break
    print('finish')
