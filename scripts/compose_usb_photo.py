from PIL import Image, ImageDraw, ImageFilter
import numpy as np

SRC = "/root/.claude/uploads/9e776b5f-0277-592a-b3b3-cca3dd197344/bc18ddf0-usb_bretx.webp"
OUT = "/root/bretx-motorsport/img/usb-case-bretx.jpg"

W, H = 1400, 850
RED_DIM = (140, 10, 20)

# ---------- 1) Rebuild the branded background (same style as before, no baked-in text) ----------
bg = Image.new("RGB", (W, H), (10, 10, 12))
px = bg.load()
for y in range(H):
    t = y / H
    r = int(10 + t * 8)
    g = int(10 + t * 8)
    b = int(12 + t * 10)
    for x in range(0, W, 1):
        pass  # placeholder, replaced by faster line draw below

draw = ImageDraw.Draw(bg)
for y in range(H):
    t = y / H
    r = int(10 + t * 8)
    g = int(10 + t * 8)
    b = int(12 + t * 10)
    draw.line([(0, y), (W, y)], fill=(r, g, b))

glow = Image.new("RGB", (W, H), (0, 0, 0))
gdraw = ImageDraw.Draw(glow)
gdraw.ellipse([W/2-560, H/2-360, W/2+560, H/2+360], fill=RED_DIM)
glow = glow.filter(ImageFilter.GaussianBlur(170))
bg = Image.blend(bg, glow, 0.5)
draw = ImageDraw.Draw(bg)

grid_color = (26, 26, 30)
step = 60
for x in range(0, W, step):
    draw.line([(x, 0), (x, H)], fill=grid_color, width=1)
for y in range(0, H, step):
    draw.line([(0, y), (W, y)], fill=grid_color, width=1)

bg = bg.convert("RGBA")

# ---------- 2) Load the real product photo and crop tight around the case ----------
photo = Image.open(SRC).convert("RGB")
# crop box estimated from the grid overlay (with a little margin)
crop_box = (140, 15, 1160, 920)
crop = photo.crop(crop_box)
cw, ch = crop.size

# ---------- 3) Feathered alpha mask (keeps the case fully opaque, fades the outer grey background) ----------
mask = Image.new("L", (cw, ch), 0)
mdraw = ImageDraw.Draw(mask)
inset = 60  # how far in from the crop edge the fade starts
mdraw.ellipse([-inset, -inset, cw + inset, ch + inset], fill=255)
mask = mask.filter(ImageFilter.GaussianBlur(90))

crop_rgba = crop.convert("RGBA")
crop_rgba.putalpha(mask)

# ---------- 4) Resize foreground to fit nicely on the branded canvas ----------
target_w = int(W * 0.86)
scale = target_w / cw
target_h = int(ch * scale)
fg = crop_rgba.resize((target_w, target_h), Image.LANCZOS)

fx = (W - target_w) // 2
fy = (H - target_h) // 2 + 10

# soft drop shadow of the case on the branded background
shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
sh_alpha = Image.new("L", (target_w, target_h), 0)
ImageDraw.Draw(sh_alpha).ellipse([target_w*0.12, target_h*0.55, target_w*0.88, target_h*0.98], fill=140)
sh_alpha = sh_alpha.filter(ImageFilter.GaussianBlur(40))
shadow_layer = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 255))
shadow_layer.putalpha(sh_alpha)
shadow.paste(shadow_layer, (fx, fy + 25), shadow_layer)
bg = Image.alpha_composite(bg, shadow)

bg.paste(fg, (fx, fy), fg)

final = bg.convert("RGB")
final.save(OUT, quality=93)
print("saved", final.size)
