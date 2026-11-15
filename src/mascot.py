"""Original fallback mascot (a blob with mood faces) used if PokeAPI is unreachable."""
from PIL import Image, ImageDraw


def mascot(tier: int, size: int = 400):
    s = size
    img = Image.new("L", (s, s), 255)
    mask = Image.new("L", (s, s), 0)
    d, m = ImageDraw.Draw(img), ImageDraw.Draw(mask)
    body = (s * .12, s * .22, s * .88, s * .92)
    ears = [[(s * .22, s * .32), (s * .18, s * .06), (s * .42, s * .24)],
            [(s * .78, s * .32), (s * .82, s * .06), (s * .58, s * .24)]]
    for target in (d, m):
        fill = 235 if target is d else 255
        target.ellipse(body, fill=fill, outline=0 if target is d else 255, width=6)
        for e in ears:
            target.polygon(e, fill=fill, outline=0 if target is d else 255)
    d.line(ears[0] + [ears[0][0]], fill=0, width=6)
    d.line(ears[1] + [ears[1][0]], fill=0, width=6)
    ex, ey = (s * .35, s * .5), (s * .65, s * .5)
    r = s * .035
    if tier == 0:   # ^ ^ eyes, big smile, blush
        for cx in (ex[0], ey[0]):
            d.arc((cx - 22, ey[1] - 18, cx + 22, ey[1] + 18), 200, 340, fill=0, width=7)
        d.chord((s * .38, s * .6, s * .62, s * .8), 0, 180, fill=0)
        for cx in (s * .26, s * .74):
            d.ellipse((cx - 20, s * .6, cx + 20, s * .66), fill=170)
    elif tier == 1:
        for cx in (ex[0], ey[0]):
            d.ellipse((cx - r, ey[1] - r, cx + r, ey[1] + r), fill=0)
        d.arc((s * .38, s * .56, s * .62, s * .74), 20, 160, fill=0, width=7)
    elif tier == 2:  # sleepy
        for cx in (ex[0], ey[0]):
            d.line((cx - 22, ey[1], cx + 22, ey[1]), fill=0, width=7)
        d.line((s * .42, s * .7, s * .58, s * .7), fill=0, width=6)
        d.text((s * .74, s * .18), "z Z", fill=0)
    elif tier == 3:  # worried
        for cx in (ex[0], ey[0]):
            d.ellipse((cx - r, ey[1] - r, cx + r, ey[1] + r), fill=0)
        d.line((ex[0] - 25, ey[1] - 32, ex[0] + 20, ey[1] - 48), fill=0, width=6)
        d.line((ey[0] + 25, ey[1] - 32, ey[0] - 20, ey[1] - 48), fill=0, width=6)
        d.arc((s * .4, s * .68, s * .6, s * .8), 200, 340, fill=0, width=7)
        d.ellipse((s * .8, s * .36, s * .86, s * .5), fill=190, outline=0, width=3)
    else:            # scary: angry brows, jagged teeth
        for cx in (ex[0], ey[0]):
            d.ellipse((cx - r * 1.4, ey[1] - r * 1.4, cx + r * 1.4, ey[1] + r * 1.4), fill=0)
        d.line((ex[0] - 30, ey[1] - 50, ex[0] + 25, ey[1] - 22), fill=0, width=9)
        d.line((ey[0] + 30, ey[1] - 50, ey[0] - 25, ey[1] - 22), fill=0, width=9)
        x0, x1, y0, y1 = s * .33, s * .67, s * .62, s * .8
        d.rectangle((x0, y0, x1, y1), fill=0)
        n = 6
        for k in range(n):
            xa = x0 + (x1 - x0) * k / n
            xb = x0 + (x1 - x0) * (k + .5) / n
            xc = x0 + (x1 - x0) * (k + 1) / n
            d.polygon([(xa, y0), (xb, y0 + 28), (xc, y0)], fill=255)
            d.polygon([(xa, y1), (xb, y1 - 28), (xc, y1)], fill=255)
    return img, mask
