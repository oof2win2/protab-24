import maze
from time import sleep

EMPTY = 0
PLAYER = 1
WALL = 2
GOAL = 3
KEY = 4
GATE = 5

# class Maze:
#     x: int
#     y: int
#     def __init__(self):
#         self.endx: int = -1
#         self.endy: int = -1
#         self.x = 256
#         self.y = 256

#         self.fields: list[list[int | None]] = [[None for _ in range(512)] for _ in range(512)]
#         self.distances: list[list[int | None]] = [[None for _ in range(512)] for _ in range(512)]
#         self.visited = set()
#         self.queue = []
#         self.path = []

#         self.map_viewable()

#     def map_viewable(self):
#         viewable = c.get_all()
#         for x in range(c.width):
#             realx = self.x + x - 8
#             for y in range(c.height):
#                 realy = self.y + y - 8
#                 self.fields[realx][realy] = viewable[x][y]

#     def find_node(self, node_type: int):
#         for y in range(len(self.fields)):
#             for x in range(len(self.fields[0])):
#                 if self.fields[x][y] == node_type:
#                     return (x, y)
#         return None

#     def get_neighbor_coords(self, x: int, y: int):
#         neighbors = []
#         print(self.fields[x][y - 1], self.fields[x][y + 1], self.fields[x - 1][y], self.fields[x + 1][y])
#         if y - 1 >= 0 and self.fields[x][y - 1] != None and self.fields[x][y - 1] != WALL:
#             neighbors.append((x, y - 1))
#         if y + 1 < 512 and self.fields[x][y - 1] != None and self.fields[x][y + 1] != WALL:
#             neighbors.append((x, y + 1))
#         if x - 1 >= 0  and self.fields[x][y - 1] != None and self.fields[x - 1][y] != WALL:
#             neighbors.append((x - 1, y))
#         if x + 1 < 512  and self.fields[x][y - 1] != None and self.fields[x + 1][y] != WALL:
#             neighbors.append((x + 1, y))
#         return neighbors

#     def bfs(self):
#         node = self.queue.pop(0)
#         x, y = node
#         neighbors = self.get_neighbor_coords(x, y)
#         for neighbor in neighbors:
#             if neighbor in self.visited:
#                 continue
#             self.visited.add(neighbor)
#             nx, ny = neighbor
#             self.distances[ny][nx] = (self.distances[y][x] or 0) + 1
#             self.queue.append(neighbor)

#     def setup_dfs(self):
#         self.path = [(self.x, self.y)]

#     def output_map(self):
#         xlen = len(self.fields)
#         ylen = len(self.fields[0])
#         with open("output", "w+") as file:
#             for y in range (ylen):
#                 for x in range(xlen):
#                     val = self.fields[x][y]
#                     if val == None:
#                         file.write(" ")
#                     elif val == WALL:
#                         file.write("#")
#                     elif val == PLAYER:
#                         file.write("P")
#                     elif val == GOAL:
#                         file.write("G")
#                     elif val == EMPTY:
#                         file.write(" ")
#                 file.write("\n")

#     def dfs(self):
#         node = self.path[-1]
#         self.visited.add(node)
#         x, y = node
#         neighbors = self.get_neighbor_coords(x, y)
#         # sleep(0.5)
#         for neighbor in neighbors:
#             if neighbor in self.visited:
#                 continue
#             nx, ny = neighbor
#             print(neighbor, self.fields[nx][ny])
#             self.path.append(neighbor)
#             self.move_to(neighbor)
#             return
#         # now we don't have any neighbors we didn't visit, so we need to backtrack
#         self.path.pop()
#         return

#     def move_to(self, neighbor: tuple[int, int]):
#         dx = neighbor[0] - self.x
#         dy = neighbor[1] - self.y

#         self.x += dx
#         self.y += dy

#         if dx == 1:
#             c.move('d')
#         if dx == -1:
#             c.move('a')
#         if dy == 1:
#             c.move('s')
#         if dy == -1:
#             c.move('w')

#         m.map_viewable()
#         return

#     def move_direction(self, key: str):
#         dy = 0
#         dx = 0

#         if key == "d":
#             c.move('d')
#             dx = 1
#         if key == "a":
#             c.move('a')
#             dx = -1
#         if key == "s":
#             c.move('s')
#             dy = 1
#         if key == "w":
#             c.move('w')
#             dy = -1

#         self.x += dx
#         self.y += dy


#         m.map_viewable()
#         return

#     def get_path_to(self, endx: int, endy: int):
#         self.endx = endx
#         self.endy = endy

#         self.path = [(self.x, self.y)]
#         self.visited.add((self.x, self.y))
#         self.distances[self.y][self.x] = 0 # start the center square at 0
#         while len(self.path) > 0:
#             self.dfs()
#         self.distances[endy][endx] = 0

#         # now we have the distances from all cells
#         # we can now find the path by going from the end
#         # to the start and always choosing the cell with
#         # the lowest number
#         path = []
#         dist = self.distances[self.y][self.x] or 0
#         x = self.x
#         y = self.y
#         print(x, y)
#         i = 0

#         while dist > 0:
#             # get all neighbors of x, y
#             # find the one with the lowest distance
#             # set x, y to that neighbor
#             # add it to the path
#             neighbors = self.get_neighbor_coords(x, y)
#             min_dist = 10000000
#             min_node = None
#             for neighbor in neighbors:
#                 nx, ny = neighbor
#                 if self.distances[ny][nx] < min_dist:
#                     min_dist = self.distances[ny][nx]
#                     min_node = neighbor
#             if min_node == None:
#                 print("No path found")
#                 exit(0)
#             x, y = min_node
#             i += 1
#             path.append(min_node)
#             if min_node == (endx, endy):
#                 break
#             dist = min_dist
#         return path

#     def move_along_path(self, path: list[tuple[int, int]]):
#         prev = (self.x, self.y)
#         for node in path:
#             dx = node[0] - prev[0]
#             dy = node[1] - prev[1]
            # if dx == 1:
            #     c.move('d')
            # if dx == -1:
            #     c.move('a')
            # if dy == 1:
            #     c.move('s')
            # if dy == -1:
            #     c.move('w')
#             prev = node

#     def find_and_path_to(self, type: int):
#         goal = self.find_node(type)
#         if goal == None:
#             print("No goal found")
#             exit(0)
#         path = self.get_path_to(goal[0], goal[1])
#         self.move_along_path(path)

#     def path_to_coord(self, x: int, y: int):
#         path = self.get_path_to(x, y)
#         self.move_along_path(path)

# m = Maze()
# m.map_viewable()
# m.output_map()
# c.wait()
# while True:
#     dir = input()
#     m.move_direction(dir)
#     m.output_map()
# m.setup_dfs()
# while True:
#     m.dfs()

visited = set((0, 0))
path = [(0, 0)]
x = 0
y = 0

c = maze.Connect("oof2win2", "chobotnice")

def move(dx: int, dy: int):
    global x, y
    if dx == 1:
        c.move('d')
    if dx == -1:
        c.move('a')
    if dy == 1:
        c.move('s')
    if dy == -1:
        c.move('w')
    x += dx
    y += dy


while True:
    page = c.get_all()
    neighbors = []
    if page[16][15] != WALL:
        neighbors.append((16, 15))
    if page[16][17] != WALL:
        neighbors.append((16, 17))
    if page[15][16] != WALL:
        neighbors.append((15, 16))
    if page[17][16] != WALL:
        neighbors.append((17, 16))
    notvisited = None
    for node in neighbors:
        if node not in visited:
            visited.add(node)
            notvisited = node
            break

    # if we visited all neighbors we backtrack
    if notvisited == None:
        current = path.pop()
        prev = path[-1]
        dx = current[0] - prev[0]
        dy = current[1] - prev[1]
        move(dx, dy)
    else:
        path.append((x, y))
        dx = notvisited[0] - x
        dy = notvisited[1] - y
        move(dx, dy)
