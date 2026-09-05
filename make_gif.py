"""
make_gif.py  —  Project ke saare screenshots se ek auto-cycling slideshow GIF banao.

Setup (ek baar):
    pip install pillow

Folder structure:
    assets/
      ecommerce/
        1.png   2.png   3.png   4.png     <- apni screenshots yahan rakho
      employee/
        1.png   2.png   3.png

Run:
    python make_gif.py assets/ecommerce
    python make_gif.py assets/employee --seconds 3      # har image 3 sec dikhegi

Output:
    assets/ecommerce/slideshow.gif   <- README me yahi lagta hai
"""
import sys, glob, os, argparse
from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument("folder", help="project folder jisme screenshots hain")
ap.add_argument("--seconds", type=float, default=2.5, help="har image kitni der dikhe")
ap.add_argument("--width", type=int, default=900, help="GIF ki width (px)")
ap.add_argument("--height", type=int, default=520, help="GIF ki height (px) — sab projects me same rakho")
a = ap.parse_args()

files = sorted(
    f for f in glob.glob(os.path.join(a.folder, "*"))
    if f.lower().endswith((".png", ".jpg", ".jpeg", ".webp")) and not f.endswith("slideshow.gif")
)
if not files:
    sys.exit(f"❌ {a.folder} me koi image nahi mili")

frames = []
for f in files:
    img = Image.open(f).convert("RGB")
    # same canvas size, aspect ratio maintain, baaki jagah dark bg
    img.thumbnail((a.width, a.height))
    canvas = Image.new("RGB", (a.width, a.height), (13, 17, 23))  # GitHub dark bg
    canvas.paste(img, ((a.width - img.width) // 2, (a.height - img.height) // 2))
    frames.append(canvas.quantize(colors=256, method=Image.Quantize.MEDIANCUT))

out = os.path.join(a.folder, "slideshow.gif")
frames[0].save(
    out, save_all=True, append_images=frames[1:],
    duration=int(a.seconds * 1000), loop=0, optimize=True,
)
print(f"✅ {out}  ({len(frames)} images, {os.path.getsize(out)//1024} KB)")
