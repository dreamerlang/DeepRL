import torch
import numpy as np
import time


class EvalDqnAgent:

    def __init__(self, q_net, eval_env):
        self._q = q_net
        self._env = eval_env

    def choose_action(self, state):
        s = torch.tensor([state]).float()
        with torch.no_grad():
            q_val = self._q(s)[0].numpy()
        return np.argmax(q_val)

    def _eval(self, viewer=False):
        s = self._env.reset()
        d = False
        total_r = 0
        while not d:
            actions = []
            for now_s in s:
                a = self.choose_action(now_s)
                actions.append(a)
            s, r, d, _ = self._env.step(actions)
            if viewer:
                self._env.render()
                time.sleep(0.5)
            total_r += sum(r)
        return total_r

    def run_eval(self, state_dict, n, viewer=False):
        self._q.load_state_dict(state_dict)
        r = [self._eval(viewer) for _ in range(n)]
        return np.mean(r)
