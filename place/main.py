from PIL import Image

TOKEN = "jan-kocourek-98a35af78caa"

im = Image.open("andy.png")
pixels = list(im.getdata())
width, height = im.size
pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]

for y, row in enumerate(pixels):
    for x, pixel in enumerate(row):
        r, g, b = pixel
        if a != 255: continue
        print(f"{x} {y} {r} {g} {b}")
