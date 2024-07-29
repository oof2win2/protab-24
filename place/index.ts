import ky from "ky";

const token = "jan-kocourek-98a35af78caa";
const offset_x = 32;
const offset_y = 0;

type Pixel = {
  r: number;
  g: number;
  b: number;

  x: number;
  y: number;
};
const pixels: Pixel[] = [];
const file = await Bun.file("./output").text();
for (const line of file.split("\n")) {
  const [x, y, r, g, b] = line.split(" ").map(Number);
  pixels.push({ x, y, r, g, b });
}

let i = 0;
for (const pixel of pixels) {
  const res = await ky("http://misto.i.protab.cz/api/draw", {
    method: "POST",
    json: {
      token,
      x: pixel.x + offset_x,
      y: pixel.y + offset_y,
      color: [pixel.r, pixel.g, pixel.b],
    },
  }).json<{
    ok: boolean;
    message: string;
    cooldown: number;
  }>();

  if (!res.ok) {
    console.error(res.message);
    process.exit();
  }

  console.log(`Placed pixel ${i++}/${pixels.length}`);

  await new Promise((resolve) => setTimeout(resolve, res.cooldown));
}
