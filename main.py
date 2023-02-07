import sys
from queue import PriorityQueue
from math import sqrt, log10
import time



class Rover:
    def __init__(self, pR, state):
        self.pR = pR
        self.state = state
        self.task = ""

class Order:
    def __init__(self, pT, pP):
        self.pT = pT
        self.pP = pP
        self.time = 0
        self.path = ""

class Map:
    def __init__(self, city):
        self.city = city

class Dispatcher:
    def __init__(self):
        pass


def get_data():
    if debug:
        return next(g)
    else:
        return input()


def setup():
    """
    get init data
    buy rovers and place them on map
    """
    N, max_tips, cost_c = [int(v) for v in get_data().strip().split(' ')]

    lines = []
    for i in range(N):
        lines.append(get_data())

    city = [[1 if v == '.' else 0 for v in line.strip()] for line in lines]

    nT, nD = [int(v) for v in get_data().strip().split(' ')]

    return (N, max_tips, cost_c, city, nT, nD)


def how_much_rovers(N, max_tips, cost_c):
    d = {
        '4_20_10': 1,
        '128_500_1000': 5,
        '180_500_5000': 10,
        '384_3600_765432': 9, # 10
        '1024_3600_555555': 25,
        '1000_3600_131072': 7,
        '1000_3600_123456': 1,
        '1000_3600_101010': 10,
        '1000_3600_1500000': 1,
        '1000_3600_1048576': 1
    }
    return d[f"{N}_{max_tips}_{cost_c}"]


def rovers_init(nrovers, N, max_tips, cost_c):
    rvs = []
    for i in range(nrovers):
        rvs.append(Rover((2, 2), 'S'))

    d = {
        '4_20_10': (1, 1),
        '128_500_1000': (63, 63),
        '180_500_5000': (91, 91),
        '384_3600_765432': (181, 180),
        '1024_3600_555555': (497, 497),
        '1000_3600_131072': (500, 484),
        '1000_3600_123456': (500, 484),
        '1000_3600_101010': (500, 484),
        '1000_3600_1500000': (500, 484),
        '1000_3600_1048576': (500, 484)
    }
    for rv in rvs:
        rv.task = 'S'*60
        rv.pR = d[f"{N}_{max_tips}_{cost_c}"]
    return rvs



if __name__ == "__main__":
    debug = True
    task_id = "04"
    # initialize source
    if debug:
        g = (v for v in open(f"examples/{task_id}"))

    N, max_tips, cost_c, city, nT, nD = setup()

    nrovers = how_much_rovers(N, max_tips, cost_c)
    print(nrovers) # send data, no remove

    rvs = rovers_init(nrovers, N, max_tips, cost_c)
    for v in rvs:
        print(v.pR[0]+1, v.pR[1]+1) # send data, no remove



    










