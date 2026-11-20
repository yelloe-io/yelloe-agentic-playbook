import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont


def font(names, size):
    for name in names:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            pass
    return ImageFont.load_default(size)


BOLD = font(["segoeuib.ttf", "Arial Bold.ttf", "arialbd.ttf", "DejaVuSans-Bold.ttf", "LiberationSans-Bold.ttf"], 30)
REG = font(["segoeui.ttf", "Arial.ttf", "arial.ttf", "DejaVuSans.ttf", "LiberationSans-Regular.ttf"], 24)
KINDS = {"before": ("BEFORE", (214, 48, 49)), "after": ("AFTER", (46, 140, 80))}


def panel(shots, p, scale):
    title, colour = KINDS[p["kind"]]
    img = Image.open(os.path.join(shots, p["shot"])).convert("RGB")
    if p.get("box"):
        ImageDraw.Draw(img).rectangle(p["box"], outline=colour, width=6)
    if p.get("crop"):
        img = img.crop(p["crop"])
    img = img.resize((int(img.width * scale), int(img.height * scale)), Image.LANCZOS)
    head = 64
    out = Image.new("RGB", (img.width, img.height + head), "white")
    d = ImageDraw.Draw(out)
    d.rectangle((0, 0, img.width, head), fill=colour)
    d.text((16, 12), title, font=BOLD, fill="white")
    d.text((32 + d.textlength(title, font=BOLD), 17), p.get("note", ""), font=REG, fill="white")
    out.paste(img, (0, head))
    return out


def combine(panels, side, path):
    gap = 24
    if side:
        size = (sum(p.width for p in panels) + gap * (len(panels) - 1), max(p.height for p in panels))
    else:
        size = (max(p.width for p in panels), sum(p.height for p in panels) + gap * (len(panels) - 1))
    out = Image.new("RGB", size, (220, 220, 220))
    pos = 0
    for p in panels:
        out.paste(p, (pos, 0) if side else (0, pos))
        pos += (p.width if side else p.height) + gap
    out.save(path)
    print(path, out.size)


spec = json.load(open(sys.argv[1], encoding="utf-8"))
os.makedirs(spec["out"], exist_ok=True)
for image in spec["images"]:
    scale = image.get("scale", 0.75)
    panels = [panel(spec["shots"], p, scale) for p in image["panels"]]
    combine(panels, image.get("layout") == "side", os.path.join(spec["out"], image["file"]))
