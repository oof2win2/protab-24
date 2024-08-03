from PIL import Image

TOKEN = "jan-kocourek-98a35af78caa"

im = Image.open("nyancat.png")
pixels = list(im.getdata())
width, height = im.size
pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]

for y, row in enumerate(pixels):
    for x, pixel in enumerate(row):
        if len(pixel) == 3:
            r, g, b = pixel
            a = 255
        else:
            r, g, b, a = pixel
        if a != 255: continue
        print(f"{x} {y} {r} {g} {b}")
