import random
import maze

AMOUNT_RUNS = 1024
CHROMOSOME_COUNT = 64

EMPTY = 0
PLAYER = 1
WALL = 2
GOAL = 3
KEY = 4
GATE = 5

c = maze.Connect('oof2win2', 'sazenice')
fields = c.get_all()
mapped = [[None] * 16 for _ in range(16)]

startx = 8
starty = 8

class Individual:
    chromosome: list[str]

    def __init__(self):
        self.chromosome = [random.choice(['w', 'a', 's', 'd']) for _ in range(CHROMOSOME_COUNT)]

    def mutate(self):
        to_change = random.randint(0, CHROMOSOME_COUNT - 1)
        prior: str | None
        if to_change == 0:
            prior = None
        else:
            prior = self.chromosome[to_change - 1]
        choices = filter(lambda el: el != prior, ['w', 'a', 's', 'd'])
        self.chromosome[to_change] = random.choice(list(choices))

    def ensure_valid_move(self, start: tuple[int, int], delta: tuple[int, int]):
        x, y = start
        dx, dy = delta
        if x + dx < 0 or x + dx >= 16 or y + dy < 0 or y + dy >= 16:
            return False
        print((y+dy, x+dx))
        if mapped[y + dy][x + dx] == WALL:
            return False
        return True

    def fitness(self):
        # the fitness function is how far the total distance the player has moved
        # within the maze
        # the higher the fitness, the better the individual is
        x = startx
        y = starty
        distance = 0
        incorrect = 0
        for move in self.chromosome:
            dy = 0
            dx = 0
            if move == 'w':
                dy -= 1
            elif move == 'a':
                dx -= 1
            elif move == 's':
                dy += 1
            elif move == 'd':
                dx += 1

            if not self.ensure_valid_move((x, y), (dx, dy)):
                incorrect += 1
            else:
                x += dx
                y += dy
                distance += 1
        print(distance, incorrect)
        return 1 - (1 / (distance - incorrect))

x = Individual()
print(x.chromosome)
print(x.fitness())

c.wait()
