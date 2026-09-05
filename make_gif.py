import sys, glob, os, argparse
from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument("folder", help="project folder jisme screenshots hain")
ap.add_argument("--seconds", type=float, default=2.5, help="har image kitni der dikhe")
ap.add_argument("--width", type=int, default=400, help="visible image width (px) — laptop pe isi size me dikhegi")
ap.add_argument("--height", type=int, default=231, help="visible image height (px) — sab projects me same rakho")
ap.add_argument("--pad_right", type=int, default=20, help="transparent gap image aur text ke beech")
ap.add_argument("--pad_bottom", type=int, default=44, help="transparent gap neeche (text wrap hone se rokta hai)")
a = ap.parse_args()

files = sorted(
    f for f in glob.glob(os.path.join(a.folder, "*"))
    if f.lower().endswith((".png", ".jpg", ".jpeg", ".webp")) and not f.endswith("slideshow.gif")
)
if not files:
    sys.exit(f"❌ {a.folder} me koi image nahi mili")

W, H = a.width + a.pad_right, a.height + a.pad_bottom
TRANSPARENT = 255  # palette index reserved for transparency

frames = []
for f in files:
    img = Image.open(f).convert("RGB")
    img.thumbnail((a.width, a.height))                      # aspect ratio maintain
    # visible area: image centered on a dark card (GitHub dark bg)
    card = Image.new("RGB", (a.width, a.height), (13, 17, 23))
    card.paste(img, ((a.width - img.width) // 2, (a.height - img.height) // 2))
    card_p = card.quantize(colors=255, method=Image.Quantize.MEDIANCUT)   # indices 0..254

    # full canvas: card top-left, padding transparent (index 255)
    canvas = Image.new("P", (W, H), TRANSPARENT)
    canvas.putpalette(card_p.getpalette() + [0, 0, 0])      # add 256th palette entry
    canvas.paste(card_p, (0, 0))
    canvas.info["transparency"] = TRANSPARENT
    frames.append(canvas)

out = os.path.join(a.folder, "slideshow.gif")
frames[0].save(
    out, save_all=True, append_images=frames[1:],
    duration=int(a.seconds * 1000), loop=0,
    transparency=TRANSPARENT, disposal=2, optimize=False,
)
print(f"✅ {out}  ({len(frames)} images, {W}x{H}px, {os.path.getsize(out)//1024} KB)")
print(f"   README me lagao:  <img align=\"left\" src=\"./{out.replace(os.sep, '/')}\" width=\"{W}\"/>")
