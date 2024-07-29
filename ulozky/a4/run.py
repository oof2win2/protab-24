import maze
from time import sleep

c = maze.Connect('oof2win2', 'karimatka')
print("Conn")
print('Šířka hrací plochy je', c.width)
print('Výška hrací plochy je', c.height)

moje_x = c.x()
moje_y = c.y()

print('Nacházíš se na souřadnicích', moje_x, moje_y)
print('Políčko pod tebou má hodnotu', c.get(moje_x, moje_y))
# c.wait()
#
WALL = 2
EMPTY = 0
PLAYER = 1
GOAL = 3

UP = 0
LEFT = 1
DOWN = 2
RIGHT = 3

fields = c.get_all()

startx = moje_x
starty = moje_y

endx = None
endy = None

for x, col in enumerate(fields):
    for y, point in enumerate(col):
        if point == GOAL:
            endx = x
            endy = y
if endy == None or endx == None:
    print("Did not find end")
    exit(0)

def get_neighbor_coords(x, y):
    neighbors = []
    if y - 1 >= 0  and fields[x][y - 1] != WALL:
        neighbors.append((x, y - 1))
    if y + 1 < c.height   and fields[x][y + 1] != WALL:
        neighbors.append((x, y + 1))
    if x - 1 >= 0  and fields[x - 1][y] != WALL:
        neighbors.append((x - 1, y))
    if x + 1 < c.width  and fields[x + 1][y] != WALL:
        neighbors.append((x + 1, y))
    return neighbors

queue = [(endx, endy)]
distances: list[list[int | None]] = [[None for x in range(c.width)] for y in range(c.height)]
visited = set((endx, endy))
distances[endy][endx] = 0

def bfs():
    node = queue.pop(0)
    x, y = node
    neighbors = get_neighbor_coords(x, y)
    print(neighbors)
    for neighbor in neighbors:
        if neighbor in visited:
            continue
        visited.add(neighbor)
        nx, ny = neighbor
        distances[ny][nx] = (distances[y][x] or 0) + 1
        queue.append(neighbor)

while len(queue) > 0:
    bfs()
distances[endy][endx] = 0
print(distances)
print(endy, endx)
print(distances[starty][startx])
print(distances[starty][startx])
print(distances[endy][endx])

# now we have distances from end to all fields
# we can use this to find the shortest path

path = []
dist = distances[starty][startx] or 0
x = startx
y = starty
i = 0
while dist > 0:
    # get all neighbors of x, y
    # find the one with the lowest distance
    # set x, y to that neighbor
    # add it to the path
    neighbors = get_neighbor_coords(x, y)
    min_dist = 10000000
    min_node = None
    for neighbor in neighbors:
        nx, ny = neighbor
        print(distances[ny][nx], min_dist, ny, nx)
        if distances[ny][nx] < min_dist:
            min_dist = distances[ny][nx]
            min_node = neighbor
    if min_node == None:
        print("No path found")
        exit(0)
    x, y = min_node
    print(min_dist, min_node, i)
    i += 1
    path.append(min_node)
    if min_node == (endx, endy):
        break
    dist = min_dist
print(len(path))

rotation = UP

def ensure_rotation(direction: int):
    global rotation
    if direction == rotation: return
    if direction == UP:
        if rotation == LEFT:
            c.move('d')
        if rotation == RIGHT:
            c.move('a')
        if rotation == DOWN:
            c.move('d')
            c.move('d')
    if direction == LEFT:
        if rotation == UP:
            c.move('a')
        if rotation == RIGHT:
            c.move('d')
            c.move('d')
        if rotation == DOWN:
            c.move('d')
    if direction == RIGHT:
        if rotation == UP:
            c.move('d')
        if rotation == LEFT:
            c.move('a')
            c.move('a')
        if rotation == DOWN:
            c.move('a')
    if direction == DOWN:
        if rotation == UP:
            c.move('a')
            c.move('a')
        if rotation == LEFT:
            c.move('a')
        if rotation == RIGHT:
            c.move('d')
    rotation = direction
print(path[0])
c.wait()

prev = (startx, starty)
for node in path:
    dx = node[0] - prev[0]
    dy = node[1] - prev[1]
    if dx == 1:
        ensure_rotation(RIGHT)
        c.move('w')
    if dx == -1:
        ensure_rotation(LEFT)
        c.move('w')
    if dy == 1:
        ensure_rotation(DOWN)
        c.move('w')
    if dy == -1:
        ensure_rotation(UP)
        c.move('w')
    prev = node
    # sleep(0.05)
c.wait()
