import maze
from time import sleep

EMPTY = 0
PLAYER = 1
WALL = 2
GOAL = 3
KEY = 4
GATE = 5

class Maze:
    def __init__(self):
        self.c = maze.Connect('oof2win2', 'zmatenost')
        self.endx: int = -1
        self.endy: int = -1
        self.startx: int = self.c.x()
        self.starty: int = self.c.y()

        self.fields = self.c.get_all()

        self.reinit()

    def reinit(self):
        self.fields = self.c.get_all()
        self.visited = set()
        self.queue = []
        self.distances = [[0 for x in range(self.c.width)] for y in range(self.c.height)]

    def find_node(self, node_type: int):
        for y in range(self.c.height):
            for x in range(self.c.width):
                if self.fields[x][y] == node_type:
                    return (x, y)
        return None

    def get_neighbor_coords(self, x: int, y: int):
        neighbors = []
        print(x, y)
        if y - 1 >= 0  and self.fields[x][y - 1] != WALL:
            neighbors.append((x, y - 1))
        if y + 1 < self.c.height   and self.fields[x][y + 1] != WALL:
            neighbors.append((x, y + 1))
        if x - 1 >= 0  and self.fields[x - 1][y] != WALL:
            neighbors.append((x - 1, y))
        if x + 1 < self.c.width  and self.fields[x + 1][y] != WALL:
            neighbors.append((x + 1, y))
        return neighbors

    def bfs(self):
        node = self.queue.pop(0)
        x, y = node
        neighbors = self.get_neighbor_coords(x, y)
        for neighbor in neighbors:
            if neighbor in self.visited:
                continue
            self.visited.add(neighbor)
            nx, ny = neighbor
            self.distances[ny][nx] = (self.distances[y][x] or 0) + 1
            self.queue.append(neighbor)

    def get_path_to(self, endx: int, endy: int):
        self.startx = self.c.x()
        self.starty = self.c.y()
        self.endx = endx
        self.endy = endy

        self.queue.append((endx, endy))

        while len(self.queue) > 0:
            self.bfs()
        self.distances[endy][endx] = 0

        # now we have the distances from all cells
        # we can now find the path by going from the end
        # to the start and always choosing the cell with
        # the lowest number
        path = []
        dist = self.distances[self.starty][self.startx] or 0
        x = self.startx
        y = self.starty
        i = 0

        while dist > 0:
            # get all neighbors of x, y
            # find the one with the lowest distance
            # set x, y to that neighbor
            # add it to the path
            neighbors = self.get_neighbor_coords(x, y)
            min_dist = 10000000
            min_node = None
            for neighbor in neighbors:
                nx, ny = neighbor
                if self.distances[ny][nx] < min_dist:
                    min_dist = self.distances[ny][nx]
                    min_node = neighbor
            if min_node == None:
                print("No path found")
                exit(0)
            x, y = min_node
            i += 1
            path.append(min_node)
            if min_node == (endx, endy):
                break
            dist = min_dist
        return path

    def move_along_path(self, path: list[tuple[int, int]]):
        prev = (self.startx, self.starty)
        for node in path:
            dx = node[0] - prev[0]
            dy = node[1] - prev[1]
            if dx == 1:
                self.c.move('d')
            if dx == -1:
                self.c.move('a')
            if dy == 1:
                self.c.move('s')
            if dy == -1:
                self.c.move('w')
            prev = node

    def find_and_path_to(self, type: int):
        goal = self.find_node(type)
        if goal == None:
            print("No goal found")
            exit(0)
        print(goal)
        path = self.get_path_to(goal[0], goal[1])
        self.move_along_path(path)

    def path_to_coord(self, x: int, y: int):
        path = self.get_path_to(x, y)
        self.move_along_path(path)

mazes = [
    Maze() for _ in range(50)
]

for i in range(49):
    mazes[i].reinit()
    mazes[i].find_and_path_to(KEY)
mazes[49].find_and_path_to(GOAL)
sleep(10)
