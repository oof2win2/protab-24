import ky from "ky";

const token = "jan-kocourek-98a35af78caa";
const offset_x = 0;
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
for (const line of file.trim().split("\n")) {
  const [x, y, r, g, b] = line.split(" ").map(Number);
  pixels.push({ x, y, r, g, b });
}

let i = 1;
for (const pixel of pixels) {
  const x = pixel.x + offset_x;
  const y = pixel.y + offset_y;
  const current = await ky(`http://misto.i.protab.cz/api/get/${x}/${y}`).json<{
    ok: boolean;
    color: [number, number, number];
  }>();
  if (!current.ok) {
    console.error("Failed to get current pixel");
    process.exit();
  }
  if (
    current.color[0] === pixel.r &&
    current.color[1] === pixel.g &&
    current.color[2] === pixel.b
  ) {
    console.log(`Pixel ${i++}/${pixels.length} is already correct`);
    continue;
  }
  const res = await ky("http://misto.i.protab.cz/api/draw", {
    method: "POST",
    json: {
      token,
      x,
      y,
      color: [pixel.r, pixel.g, pixel.b],
    },
    throwHttpErrors: false,
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
