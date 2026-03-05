import sys
from collections import deque
import heapq
from math import sqrt
from typing import Callable

class Node:
    point: tuple
    parent: Node
    path_cost: float

    def __init__(self, point: tuple, prev_node: Node | None = None):
        self.point = point
        self.parent = prev_node
        self.path_cost = self.__calculate_path_cost()

    def __lt__(self, other):
        return self.path_cost < other.path_cost

    def __calculate_path_cost(self):
        previous_node = self.parent
        path_cost = 0
        while previous_node is not None:
            path_cost += cost(previous_node.point, self.point)
            previous_node = previous_node.parent
        return path_cost

    def construct_path(self):
        previous_node = self.parent
        path = [self.point]
        while previous_node is not None:
            path.append(previous_node.point)
            previous_node = previous_node.parent
        return path[::-1]

    def expand(self):
        output = []

        above = (self.point[0],self.point[1]-1)
        if above[1] >= 0:
            output.append(Node(above, self))

        below = (self.point[0], self.point[1]+1)
        if below[1] < SIZE[1]:
            output.append(Node(below, self))

        left = (self.point[0]-1, self.point[1])
        if left[0] >= 0:
            output.append(Node(left, self))

        right = (self.point[0]+1, self.point[1])
        if right[0] < SIZE[0]:
            output.append(Node(right, self))
        return output

def parse_map(map: str):
    rows = map.split('\n')
    size = tuple([int(num) for num in rows[0].split(' ')])
    #shift the start and end values down 1 to become 0 based
    start = tuple([int(num)-1 for num in rows[1].split(' ')])
    end = tuple([int(num)-1 for num in rows[2].split(' ')])
    parsed_map = []
    for i in range(size[1]):
        points = rows[3+i].split(' ')
        parsed_map.append([int(point) if point != 'X' else 0 for point in points])
    return parsed_map, size, start, end

# def cost(i1: int,j1: int,i2: int,j2: int):
def cost(p1: tuple, p2: tuple):
    step_up_height = MAP[p2[1]][p2[0]] - MAP[p1[1]][p2[0]]
    if step_up_height > 0:
        return 1 + step_up_height
    else:
        return 1

def print_map(path: list | None = None):
    output = [row[:] for row in MAP]
    if path is not None:
        for point in path:
            output[point[1]][point[0]] = "*"
    for row in output:
        print(" ".join(str(el) for el in row))
    return


def read_text_file(path: str):
    with open(path, 'r') as f:
        contents = f.read()
    return contents

def bfs(goal: tuple, fringe: deque[Node]) -> tuple[bool, list]:
    closed = []
    visited = [fringe[0].point]
    while len(fringe) > 0:
        node = fringe.popleft()
        if node.point[0] == goal[0] and node.point[1] == goal[1]:
            return True, node.construct_path()
        if node.point not in closed:
            closed.append(node.point)
            neighbors = node.expand()
            for neighbor in neighbors:
                if neighbor.point not in visited and MAP[neighbor.point[1]][neighbor.point[0]] != 0:
                    visited.append(neighbor.point)
                    fringe.append(neighbor)
    return False, []

def dfs(goal: tuple, fringe: deque[Node]) -> tuple[bool, list]:
    closed = []
    visited = [fringe[0].point]
    while len(fringe) > 0:
        node = fringe.popleft()
        if node.point[0] == goal[0] and node.point[1] == goal[1]:
            return True, node.construct_path()
        if node.point not in closed:
            closed.append(node.point)
            neighbors = node.expand()
            for neighbor in neighbors:
                if neighbor.point not in visited and MAP[neighbor.point[1]][neighbor.point[0]] != 0:
                    visited.append(neighbor.point)
                    fringe.appendleft(neighbor)
    return False, []

def a_star(goal: tuple, fringe: heapq[tuple[int, Node]], hueristic: Callable[[Node, Node], float]) -> tuple[bool, list]:
    closed = []
    visited = [fringe[0][1].point]
    while len(fringe) > 0:
        est_cost, node = heapq.heappop(fringe)
        if node.point[0] == goal[0] and node.point[1] == goal[1]:
            return True, node.construct_path()
        if node.point not in closed:
            closed.append(node.point)
            neighbors = node.expand()
            for neighbor in neighbors:
                if neighbor.point not in visited and MAP[neighbor.point[1]][neighbor.point[0]] != 0:
                    visited.append(neighbor.point)
                    estimated_cost = node.path_cost + hueristic(node, neighbor)
                    heapq.heappush(fringe, (estimated_cost,neighbor))
    return False, []

def manhatten_distance(n1: Node, n2: Node) -> float:
    return abs(n1.point[0] - n2.point[0]) + abs(n2.point[1] - n1.point[1])
def euclidean_distance(n1: Node, n2: Node) -> float:
    return sqrt((n2.point[0] - n1.point[0])**2 + (n2.point[1] - n1.point[1])**2)


MODE = sys.argv[1]
MAP_FILE = sys.argv[2]
MAP, SIZE, START, END = parse_map(read_text_file(MAP_FILE))
ALGORITHM = sys.argv[3]
HEURISTIC = sys.argv[4]
if MODE == 'debug':
    print('mode:', MODE)
    print('map:')
    print_map()
    print('algorithm:', ALGORITHM)
    print('heuristic:', HEURISTIC)
    print('start:', START)
    print('end:', END)
    print('size:', SIZE)
    # print(cost(1,0,0,0))
path = None
success = False
if ALGORITHM == 'bfs':
    success, path = bfs(END, deque([Node(START)]))
elif ALGORITHM == 'dfs':
    success, path = dfs(END, deque([Node(START)]))
elif ALGORITHM == 'astar':
    success, path = a_star(END, [(0,Node(START))], manhatten_distance)
if success:
    print_map(path)
else:
    print("Failed to find path on map")
    print_map()




