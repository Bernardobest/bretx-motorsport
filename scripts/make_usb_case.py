from PIL import Image, ImageDraw, ImageFilter, ImageFont
import math

W, H = 1400, 1000
RED = (227, 6, 19)
RED_DIM = (140, 10, 20)
DARK = (10, 10, 12)
DARK2 = (20, 20, 24)
METAL = (48, 50, 56)
METAL_LIGHT = (90, 92, 100)
FOAM = (26, 26, 30)
FOAM_EDGE = (40, 40, 46)
WHITE = (240, 240, 242)
GREY = (150, 150, 156)

def font(path, size):
    return ImageFont.truetype(path, size)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

img = Image.new("RGB", (W, H), DARK)
draw = ImageDraw.Draw(img)

# background vertical gradient
for y in range(H):
    t = y / H
    r = int(10 + t * 8)
    g = int(10 + t * 8)
    b = int(12 + t * 10)
    draw.line([(0, y), (W, y)], fill=(r, g, b))

# subtle red radial glow behind the case
glow = Image.new("RGB", (W, H), (0, 0, 0))
gdraw = ImageDraw.Draw(glow)
gdraw.ellipse([W/2-520, H/2-360, W/2+520, H/2+360], fill=RED_DIM)
glow = glow.filter(ImageFilter.GaussianBlur(160))
img = Image.blend(img, glow, 0.55)
draw = ImageDraw.Draw(img)

# faint grid lines (echoes hero-grid)
grid_color = (26, 26, 30)
step = 60
for x in range(0, W, step):
    draw.line([(x, 0), (x, H)], fill=grid_color, width=1)
for y in range(0, H, step):
    draw.line([(0, y), (W, y)], fill=grid_color, width=1)

def rounded_rect(d, box, radius, fill=None, outline=None, width=1):
    d.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)

# ---- CASE (open hard case, viewed from slight top-down angle) ----
case_cx, case_cy = W/2, H/2 + 40
case_w, case_h = 760, 500

# drop shadow of case
shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
sdraw = ImageDraw.Draw(shadow)
sdraw.rounded_rectangle(
    [case_cx - case_w/2 + 20, case_cy - case_h/2 + 40, case_cx + case_w/2 + 20, case_cy + case_h/2 + 60],
    radius=36, fill=(0, 0, 0, 160)
)
shadow = shadow.filter(ImageFilter.GaussianBlur(30))
img = Image.alpha_composite(img.convert("RGBA"), shadow).convert("RGB")
draw = ImageDraw.Draw(img)

# outer case shell
case_box = [case_cx - case_w/2, case_cy - case_h/2, case_cx + case_w/2, case_cy + case_h/2]
rounded_rect(draw, case_box, 34, fill=DARK2, outline=(60, 60, 66), width=3)

# inner bezel
inner_pad = 20
inner_box = [case_box[0]+inner_pad, case_box[1]+inner_pad, case_box[2]-inner_pad, case_box[3]-inner_pad]
rounded_rect(draw, inner_box, 24, fill=(16, 16, 19), outline=(50, 50, 56), width=2)

# red top accent strip on the case lid edge (brand identity)
strip_h = 14
draw.rounded_rectangle(
    [inner_box[0]+30, inner_box[1]+14, inner_box[2]-30, inner_box[1]+14+strip_h],
    radius=7, fill=RED
)

# foam insert with cutout
foam_pad = 40
foam_box = [inner_box[0]+foam_pad, inner_box[1]+foam_pad+30, inner_box[2]-foam_pad, inner_box[3]-foam_pad]
rounded_rect(draw, foam_box, 18, fill=FOAM, outline=FOAM_EDGE, width=2)
# foam texture: diagonal subtle lines
fw0, fh0, fw1, fh1 = foam_box
for i in range(-int(fh1-fh0), int(fw1-fw0), 22):
    x0 = fw0 + i
    y0 = fh0
    x1 = fw0 + i + (fh1 - fh0)
    y1 = fh1
    draw.line([(x0, y0), (x1, y1)], fill=(30, 30, 34), width=1)

# ---- USB drive cutout (diagonal) inside foam ----
usb_cx = (fw0 + fw1) / 2
usb_cy = (fh0 + fh1) / 2
angle = -18  # degrees

usb_len, usb_w = 420, 110
cutout_pad = 14

def rotated_rounded_rect(center, length, width, radius, angle_deg, fill, outline=None, owidth=2):
    layer = Image.new("RGBA", (int(length*1.6), int(width*1.6)), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    lw, lh = layer.size
    box = [lw/2 - length/2, lh/2 - width/2, lw/2 + length/2, lh/2 + width/2]
    ld.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=owidth)
    layer = layer.rotate(angle_deg, resample=Image.BICUBIC, expand=True)
    return layer

# cutout shadow (darker foam recess)
cutout = rotated_rounded_rect((usb_cx, usb_cy), usb_len+cutout_pad*2, usb_w+cutout_pad*2, 26, angle, fill=(14, 14, 16, 255))
cx0 = int(usb_cx - cutout.width/2)
cy0 = int(usb_cy - cutout.height/2)
img.paste(cutout, (cx0, cy0), cutout)
draw = ImageDraw.Draw(img)

# ---- USB drive body ----
def usb_drive_layer(length, width, angle_deg):
    pad = 40
    lw, lh = int(length + pad*2), int(width + pad*2)
    layer = Image.new("RGBA", (lw, lh), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)

    body_len = length * 0.68
    body_box = [pad, lh/2 - width/2, pad + body_len, lh/2 + width/2]
    # metal body gradient (simple: base fill + lighter top band)
    ld.rounded_rectangle(body_box, radius=width*0.28, fill=METAL, outline=(70,72,80), width=3)
    # top highlight band
    hl_box = [body_box[0]+10, body_box[1]+8, body_box[2]-10, body_box[1]+width*0.32]
    ld.rounded_rectangle(hl_box, radius=width*0.18, fill=METAL_LIGHT)

    # brand wordmark on body
    try:
        f = ImageFont.truetype(BOLD, int(width*0.30))
    except Exception:
        f = ImageFont.load_default()
    text = "BretX"
    tb = ld.textbbox((0,0), text, font=f)
    tw, th = tb[2]-tb[0], tb[3]-tb[1]
    tx = body_box[0] + (body_len - tw)/2
    ty = body_box[1] + (width - th)/2 - th*0.15
    ld.text((tx, ty), text, font=f, fill=WHITE)

    # small red dot accent near text
    dot_r = width*0.06
    ld.ellipse([body_box[2]-width*0.55, body_box[1]+width*0.5-dot_r, body_box[2]-width*0.55+dot_r*2, body_box[1]+width*0.5+dot_r], fill=RED)

    # connector cap (red) at the right end
    cap_len = length - body_len
    cap_box = [pad + body_len - 6, lh/2 - width*0.42, pad + body_len - 6 + cap_len, lh/2 + width*0.42]
    ld.rounded_rectangle(cap_box, radius=width*0.16, fill=RED, outline=(90,4,10), width=2)
    # cap ridges
    for i in range(3):
        rx = cap_box[0] + cap_len*0.35 + i*cap_len*0.16
        ld.line([(rx, cap_box[1]+8), (rx, cap_box[3]-8)], fill=(160, 5, 15), width=3)

    # metal USB connector tip at far right
    tip_len = length*0.10
    tip_box = [cap_box[2]-4, lh/2 - width*0.22, cap_box[2]-4+tip_len, lh/2 + width*0.22]
    ld.rounded_rectangle(tip_box, radius=6, fill=(210, 210, 216), outline=(140,140,146), width=2)

    # keyring loop at left end
    loop_r = width*0.28
    loop_cx = body_box[0] - loop_r*0.3
    loop_cy = lh/2
    ld.ellipse([loop_cx-loop_r, loop_cy-loop_r, loop_cx+loop_r, loop_cy+loop_r], outline=(150,150,156), width=6)

    layer = layer.rotate(angle_deg, resample=Image.BICUBIC, expand=True)
    return layer

usb_layer = usb_drive_layer(usb_len, usb_w, angle)
ux0 = int(usb_cx - usb_layer.width/2)
uy0 = int(usb_cy - usb_layer.height/2 - 6)
img.paste(usb_layer, (ux0, uy0), usb_layer)
draw = ImageDraw.Draw(img)

# ---- Case lid label plate (bottom of case, brand plate) ----
plate_w, plate_h = 300, 64
plate_box = [case_cx-plate_w/2, case_box[3]-plate_h-26, case_cx+plate_w/2, case_box[3]-26]
rounded_rect(draw, plate_box, 12, fill=(14,14,16), outline=RED, width=2)
f_plate = font(BOLD, 26)
label = "ÉDITION BretX MOTORSPORT"
tb = draw.textbbox((0,0), label, font=f_plate)
tw, th = tb[2]-tb[0], tb[3]-tb[1]
draw.text((case_cx - tw/2, plate_box[1] + (plate_h-th)/2 - th*0.15), label, font=f_plate, fill=WHITE)

# ---- Caption text top ----
f_kicker = font(BOLD, 30)
kicker = "SAUVEGARDE MULTI-CARTOGRAPHIES"
tb = draw.textbbox((0,0), kicker, font=f_kicker)
tw, th = tb[2]-tb[0], tb[3]-tb[1]
draw.text((W/2 - tw/2, 56), kicker, font=f_kicker, fill=RED)

f_title = font(BOLD, 46)
title = "Votre clé USB, à l'image BretX Motorsport"
tb = draw.textbbox((0,0), title, font=f_title)
tw, th = tb[2]-tb[0], tb[3]-tb[1]
draw.text((W/2 - tw/2, 100), title, font=f_title, fill=WHITE)

img.save("/root/bretx-motorsport/img/usb-case-bretx.jpg", quality=92)
print("done", img.size)
