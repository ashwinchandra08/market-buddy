"""Download Pokémon artwork from PokeAPI at build time and prepare it for e-ink."""
from __future__ import annotations

import os
import urllib.request

from PIL import Image, ImageEnhance, ImageFilter, ImageOps

URL = ("https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/"
       "other/official-artwork/{id}.png")
NAMES = {25: "Pikachu", 39: "Jigglypuff", 35: "Clefairy", 133: "Eevee", 1: "Bulbasaur",
         4: "Charmander", 143: "Snorlax", 132: "Ditto", 113: "Chansey", 54: "Psyduck",
         7: "Squirtle", 79: "Slowpoke", 94: "Gengar", 130: "Gyarados", 150: "Mewtwo"}


def name_for(pid: int) -> str:
    return NAMES.get(pid, f"#{pid}")


def fetch_sprite(pid: int, cache_dir: str = "sprites"):
    os.makedirs(cache_dir, exist_ok=True)
    path = os.path.join(cache_dir, f"{pid}.png")
    if not os.path.exists(path):
        try:
            req = urllib.request.Request(URL.format(id=pid), headers={"User-Agent": "market-buddy"})
            with urllib.request.urlopen(req, timeout=20) as r, open(path, "wb") as f:
                f.write(r.read())
        except Exception as e:
            print(f"[sprite] download failed for {pid}: {e}")
            return None
    try:
        return Image.open(path).convert("RGBA")
    except Exception as e:
        print(f"[sprite] bad file {path}: {e}")
        return None


def prepare(img: Image.Image, box: tuple[int, int]):
    """RGBA artwork -> (grayscale image with dark outline, transparency mask), fitted into box."""
    bbox = img.getchannel("A").getbbox()
    if bbox:
        img = img.crop(bbox)
    img.thumbnail(box, Image.LANCZOS)
    alpha = img.getchannel("A")
    outline = alpha.filter(ImageFilter.MaxFilter(7))
    gray = ImageOps.autocontrast(img.convert("L"), cutoff=1)
    gray = ImageEnhance.Contrast(gray).enhance(1.25)
    gray = gray.filter(ImageFilter.UnsharpMask(radius=2, percent=80, threshold=2))
    out = Image.new("L", img.size, 255)
    out.paste(0, mask=outline)
    out.paste(gray, mask=alpha)
    return out, outline
