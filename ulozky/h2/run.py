import maze
from time import sleep

c = maze.Connect('oof2win2', 'lzicka@belej')
print('Šířka hrací plochy je', c.width)
print('Výška hrací plochy je', c.height)

print('Nacházíš se na souřadnicích', c.x(), c.y())

EMPTY = 0
PLAYER = 1
WALL = 2
GOAL = 3
KEY = 4
GATE = 5

class Maze:
    def __init__(self):
        self.endx: int = -1
        self.endy: int = -1
        self.startx: int = c.x()
        self.starty: int = c.y()

        self.fields = c.get_all()

        self.reinit()

    def reinit(self):
        self.fields = c.get_all()
        self.visited = set()
        self.queue = []
        self.distances = [[0 for x in range(c.width)] for y in range(c.height)]

    def find_node(self, node_type: int):
        for y in range(c.height):
            for x in range(c.width):
                if self.fields[x][y] == node_type:
                    return (x, y)
        return None

    def get_neighbor_coords(self, x: int, y: int):
        neighbors = []
        print(x, y)
        if y - 1 >= 0  and self.fields[x][y - 1] != WALL:
            neighbors.append((x, y - 1))
        if y + 1 < c.height   and self.fields[x][y + 1] != WALL:
            neighbors.append((x, y + 1))
        if x - 1 >= 0  and self.fields[x - 1][y] != WALL:
            neighbors.append((x - 1, y))
        if x + 1 < c.width  and self.fields[x + 1][y] != WALL:
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
        self.startx = c.x()
        self.starty = c.y()
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
        self.print_distances()

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
                c.move('d')
            if dx == -1:
                c.move('a')
            if dy == 1:
                c.move('s')
            if dy == -1:
                c.move('w')
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

    def print_distances(self):
        for y in range(c.height):
            for x in range(c.width):
                if self.fields[x][y] == WALL:
                    print("###", end=" ")
                else:
                    print(f"{self.distances[y][x]:3}", end=" ")
            print()

for _ in range(30):
    c.move("1")

while True:
    dir = input()
    c.move(dir)
    if c.error: print(c.error)
c.wait()
