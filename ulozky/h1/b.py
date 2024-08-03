import maze
from time import sleep

c = maze.Connect('oof2win2', 'fronta@MatejH')
print("Conn")
print('Šířka hrací plochy je', c.width)
print('Výška hrací plochy je', c.height)

moje_x = c.x()
moje_y = c.y()

print('Nacházíš se na souřadnicích', moje_x, moje_y)
print('Políčko pod tebou má hodnotu', c.get(moje_x, moje_y))


while True:
    dir = input()
    c.move(dir)
    if c.error: print(c.error)
c.wait()
