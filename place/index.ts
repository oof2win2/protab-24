import { decode } from "bmp-js";
import ky from "ky";

const token = "XXX";

const bmp = decode(Buffer.from(await Bun.file("./bmp").arrayBuffer()));
const data = bmp.data;

type Pixel = {
  r: number;
  g: number;
  b: number;

  x: number;
  y: number;
};
const pixels: Pixel[] = [];

for (let i = 0; i < bmp.width * bmp.height; i += 4) {
  const a = data[i];
  const b = data[i + 1];
  const g = data[i + 2];
  const r = data[i + 3];
  const x = i % bmp.width;
  const y = Math.floor(i / bmp.width);
  pixels.push({ r, g, b, x, y });
}

for (const pixel of pixels) {
  const res = await ky("http://misto.i.protab.cz/api/draw", {
    method: "POST",
    json: {
      token,
      x: pixel.x,
      y: pixel.y,
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

  console.log(JSON.stringify(pixel));

  await new Promise((resolve) => setTimeout(resolve, res.cooldown));
}
