import os
if __name__ == '__main__':
    dir='./result/ddpg/test'
    if not os.path.exists(dir):
        os.makedirs(dir)