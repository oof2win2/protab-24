import maze
from time import sleep

connections = [
    maze.Connect('oof2win2', 'aretace')
    for _ in range(50)
]
print("connected")

for c in connections:
    for _ in range(30):
        if not c.move("w"): print(c.error)
for c in connections:
    for _ in range(30):
        if not c.move("s"): print(c.error)
sleep(10)
