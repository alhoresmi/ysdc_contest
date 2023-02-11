import sys
from queue import PriorityQueue
import heapq
from math import sqrt, log10
import time
import random


class Rover:
    def __init__(self, x, y, state, idx):
        self.x = x
        self.y = y
        self.pR = [self.x, self.y]
        self.state = state
        self.task = ""
        self.idx = idx

    def update(self):
        global norders
        if self.state != 'P':
            # uncomment task print before sending to ya
            #print(60*'S')
            pass
        else:
            if len(self.task) < 60:
                self.task = self.task + 'S'*(60 - len(self.task))

            # uncomment task print before sending to ya
            #print(self.task[:60])

            #dx, dy = route_to_xy(self.task[:60])
            #self.pR[0] += dx
            #self.pR[1] += dy
            if (self.task[59] == 'S' or self.task[59] == 'P') and len(self.task) == 60:
                self.state = 'S'
                self.task = 'S'*60
                norders += 1
            else:
                self.state = 'P'
                self.task = self.task[60:]

            #print(f"ROVER UPDATE {self.idx} {self.pR}")

    def update_position(self, x, y):
        self.pR = [x, y]


class Order:
    def __init__(self, pT, pP):
        self.pT = pT
        self.pP = pP
        self.length = 0
        self.time = 0
        self.path = ""


class Orders:
    def __init__(self, nrovers):
        self.chains = []
        self.empty_chains = nrovers
        for _ in range(nrovers):
            self.chains.append([])

    def put(self, order):
        mdist = 2*N
        midx = 0
        #print(f"PUT ORDER {self.empty_chains}")
        for i in range(nrovers):
            pt = self.chains[i][-1].pP if self.chains[i] != [] else rvs[i].pR 
            dst = dist(order.pT, pt)
            if dst < mdist:
                mdist = dst
                midx = i
        if self.chains[midx] == []:
            self.empty_chains -= 1
        self.chains[midx].append(order)

    def pop(self, idx):
        o = self.chains[idx].pop(0)
        if self.chains[idx] == []:
            self.empty_chains += 1
        return o

    def print_chains(self, verbose=True):
        print(f"empty_chains {self.empty_chains}")
        for i in range(nrovers):
            print(f"chain {i} {len(self.chains[i])}")
            if verbose:
                for o in self.chains[i]:
                    print(f"{o.pT}->{o.pP}")

    def max_chain(self):
        m = 0
        for ch in self.chains:
            if len(ch) > m:
                m = len(ch)
        return m


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

    city = [[1 if v == '.' else 0 for v in get_data().strip()] for _ in range(N)]

    nT, nD = [int(v) for v in get_data().strip().split(' ')]

    return (N, max_tips, cost_c, city, nT, nD)


def how_much_rovers(N, max_tips, cost_c):
    """
    nrovers ~= sum(distances)/nT/60
    """
    d = {
        '4_20_10': 1,
        '128_500_1000': 5, #5
        '180_500_5000': 8, #5
        '384_3600_765432': 15, # 10
        '1024_3600_555555': 25, #25
        '1000_3600_131072': 10,
        '1000_3600_123456': 1,
        '1000_3600_101010': 1,
        '1000_3600_1500000': 25,
        '1000_3600_1048576': 50
    }
    return d[f"{N}_{max_tips}_{cost_c}"]


def rovers_init(nrovers, N, max_tips, cost_c):
    rvs = []
    for i in range(nrovers):
        rvs.append(Rover(2, 2, 'S', i))

    d = {
        '4_20_10': [1, 1],
        '128_500_1000': [63, 63],
        '180_500_5000': [91, 91],
        '384_3600_765432': [181, 180],
        '1024_3600_555555': [497, 497],
        '1000_3600_131072': [500, 484],
        '1000_3600_123456': [500, 484],
        '1000_3600_101010': [500, 484],
        '1000_3600_1500000': [500, 484],
        '1000_3600_1048576': [500, 484]
    }
    for rv in rvs:
        rv.task = 'S'*60
        rv.pR = d[f"{N}_{max_tips}_{cost_c}"]
    return rvs


def create_order(s):
    s = [int(v)-1 for v in s.strip().split(" ")]
    o = Order((s[0], s[1]), (s[2], s[3]))
    o.path = path_to_directions(search(city, o.pT, o.pP))
    #o.path = "UUUDDD"
    o.length = len(o.path)
    o.time = o.length
    #print(f"CREATE ORDER {o.pT}->{o.pP} {o.path}")

    return o


def dist(pR, pT):
    d = abs(pR[0] - pT[0]) + abs(pR[1] - pT[1])
    return d


def pdelta(p1, p2):
    return (p2[0] - p1[0], p2[1] - p1[1])


def search(grid, start, target, flag=False):
    height = len(grid)
    width = len(grid[0])
    #queue = PriorityQueue()
    #queue.put((0, [start]))
    queue = []
    heapq.heappush(queue, (0, [start]))
    seen = set([start])
    mdist = width*height
    while heapq:#queue:
        priority, path = heapq.heappop(queue)#queue.get()
        x, y = path[-1]
        if x == target[0] and y == target[1]:
            return path
        for x2, y2 in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
            if 0 <= x2 < width and 0 <= y2 < height and grid[x2][y2] != 0 and (x2, y2) not in seen:
                # cost for direction change
                #if len(path) > 1:
                #    c = pdelta((x2, y2), (x, y)) == pdelta(path[-1], path[-2])
                #    c = 0 if c else 1
                #else:
                #    c = 0
                c = 0

                # h estimated distance to target
                h = dist((x2, y2), target)

                # g path length so far
                g = pow(len(path), 1-10/len(grid))

                #queue.put((h+g+c, path + [(x2, y2)]))
                heapq.heappush(queue, (h+g+c, path+[(x2, y2)]))
                seen.add((x2, y2))


def simple_search(grid, start, target):
    """
    TODO: for problems 1-5 we actually dont need a*, we can simply compute path by moving along grid axes
    """
    pass


def path_to_directions(p):
    d = ''
    for i in range(len(p) - 1):
        if p[i+1][0] - p[i][0] == 1:
            d += 'D'
        if p[i+1][0] - p[i][0] == -1:
            d += 'U'
        if p[i+1][1] - p[i][1] == 1:
            d += 'R'
        if p[i+1][1] - p[i][1] == -1:
            d += 'L'
    return d


def route_to_xy(s):
    dx, dy = 0, 0
    for v in s:
        if v == 'L':
            dy -= 1
        elif v == 'R':
            dy += 1
        elif v == 'U':
            dx -= 1
        elif v == 'D':
            dx += 1

    return dx, dy


def create_task(rv, orders):
    task = []
    if orders.chains[rv.idx] == []:
        task = 60*'S'
    else:
        #o = orders.chains[rv.idx].pop(0)
        o = orders.pop(rv.idx)
        task = path_to_directions(search(city, tuple(rv.pR), o.pT)) +'T' + o.path + 'P'
        #task = 59*'X' + 'P'
        #print(f"CREATE TASK {rv.idx}@{rv.pR} -> order {o.pT} {task}")
        rv.update_position(o.pP[0], o.pP[1])
        rv.task = task
        rv.state = 'P'
    #return task


def dispatch():
    orders = Orders(nrovers)
    global norders

    for t in range(nT):
        # 1 get fresh orders
        n0 = int(get_data())
        if n0 > 0:
            for i in range(n0):
                o = create_order(get_data())
                orders.put(o)
        #print(f"iter {t}, orders {n0}, max_chain {orders.max_chain()}, empty_chains {orders.empty_chains}")
        #orders.print_chains(False)

        # 2 assign orders to rovers and send commands
        for rv in rvs:
            #print(f"SHOW ROVER {rv.idx} {rv.state} {rv.pR} {len(orders.chains[rv.idx])}")
            if rv.state == 'S' and len(orders.chains[rv.idx]) > 0:
                create_task(rv, orders)

        # 3 update everything (rovers and orders)
        # orders that are not assigned
        #for o in orders:
        #    o.time += 60
        # rovers
        for rv in rvs:
            rv.update()

        if time.time() - t0 > 20:
            break

if __name__ == "__main__":
    # set debug = False before sending solution to yandex
    debug = True
    task_id = sys.argv[1] #"04"
    t0 = time.time()
    norders = 0
    
    # initialize source
    if debug:
        g = (v for v in open(f"examples/{task_id}"))

    N, max_tips, cost_c, city, nT, nD = setup()

    if debug:
        print(f"task_id {task_id}, nT {nT}, nD {nD}")
        #input()

    nrovers = how_much_rovers(N, max_tips, cost_c)
    print(nrovers) # send data, no remove

    rvs = rovers_init(nrovers, N, max_tips, cost_c)
    for v in rvs:
        print(v.pR[0]+1, v.pR[1]+1) # send data, no remove
    
    # receive and process orders
    dispatch()

    print(f"GAME OVER. norders {norders}")
