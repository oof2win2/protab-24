import maze
c = maze.Connect('oof2win2', 'sazenice')
print("Conn")
print('Šířka hrací plochy je', c.width)
print('Výška hrací plochy je', c.height)

moje_x = c.x()
moje_y = c.y()

print('Nacházíš se na souřadnicích', moje_x, moje_y)
print('Políčko pod tebou má hodnotu', c.get(moje_x, moje_y))
c.wait()
while True:
    char = input()
    if char not in ["w", "a", "s", "d"]:
        print("zadej znovu")
        continue
    if not c.move(char):
        print('Posun nahoru se nepodařil, protože:', c.error)
