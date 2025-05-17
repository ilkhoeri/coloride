from coloraide import Color
from collections import OrderedDict
import json

def generate_overlay_alpha(scale, alphas=None, base="#000"): # or base="#fff"
    if alphas is None:
        alphas = [0.0125, 0.025, 0.0625, 0.094, 0.125, 0.157, 0.192, 0.27, 0.45, 0.49, 0.61, 0.875]

    overlay_scale = OrderedDict()
    for i, (key, fg) in enumerate(scale.items()):
        if i >= len(alphas):
            break
        a = alphas[i]
        fg_color = Color(fg).convert("srgb").fit()
        bg_color = Color(base).convert("srgb")

        blended = fg_color.mix(bg_color, p=1 - a, space="srgb").convert("srgb").fit()
        r, g, b = [int(x * 255) for x in blended.coords()]
        aa = round(a * 255)
        hex_rgba = "#{:02x}{:02x}{:02x}{:02x}".format(r, g, b, aa)

        overlay_scale[f"{key}"] = hex_rgba
    return overlay_scale

def generate_from_hue(name, hue, chroma=0.15, l_start=0.95, l_end=0.2, steps=9):
    scale = OrderedDict()
    for i, step in enumerate(range(100, 1000, 100)):
        t = i / (steps - 1)
        l = l_start + (l_end - l_start) * t
        color = Color('oklch', [l, chroma, hue]).convert('srgb')
        color.fit(method='clip')
        scale[str(step)] = color.to_string(hex=True)
    return name, scale

palette = OrderedDict()

# (dalam derajat 0-360)
colors = {
    # Netral, sangat rendah chroma (misal 0.01), hue default 0
    "gray": {"hue": 0, "chroma": 0.005},
    "silver": {"hue": 260, "chroma": 0.0058},

    # Warna hangat, chroma sedang (0.15-0.2)
    "coral": {"hue": 12, "chroma": 0.18},
    "punch": {"hue": 0, "chroma": 0.22},
    "orange": {"hue": 35, "chroma": 0.2},
    "gold": {"hue": 50, "chroma": 0.15},
    "lime": {"hue": 90, "chroma": 0.2},

    # Warna dingin, chroma sedang (0.15-0.2), hue berbeda jelas
    "java": {"hue": 140, "chroma": 0.18},
    "teal": {"hue": 180, "chroma": 0.18},
    "cyan": {"hue": 190, "chroma": 0.2},
    "azure": {"hue": 210, "chroma": 0.18},

    # Biru lebih gelap, chroma sedikit lebih rendah
    "shark": {"hue": 230, "chroma": 0.15},
    "woodsmoke": {"hue": 250, "chroma": 0.13},

    # Ungu dan magenta
    "ameth": {"hue": 270, "chroma": 0.18},
    "shaft": {"hue": 285, "chroma": 0.18},
    "violet": {"hue": 290, "chroma": 0.2},
    "fuchsia": {"hue": 320, "chroma": 0.22},
    "pink": {"hue": 340, "chroma": 0.18},
}

def generate_from_hue(name, hue, chroma=0.15, l_start=0.95, l_end=0.2, steps=9):
    scale = OrderedDict()
    for i, step in enumerate(range(100, 1000, 100)):
        t = i / (steps - 1)
        l = l_start + (l_end - l_start) * t
        color = Color('oklch', [l, chroma, hue]).convert('srgb')
        color.fit(method='clip')
        scale[str(step)] = color.to_string(hex=True)
    return name, scale


palette = OrderedDict()

for name, props in colors.items():
    name, scale = generate_from_hue(name, props["hue"], props["chroma"])
    alpha = generate_overlay_alpha(scale)
    scale["overlay"] = alpha
    palette[name] = scale


# for name, hue in colors.items():
#     _, scale = generate_from_hue(name, hue)
#     alpha = generate_overlay_alpha(scale) # default blend to black
#     # palette[name] = scale
#     # palette[f"{name}A"] = alpha
#     scale["overlay"] = alpha
#     palette[name] = scale

palette["pure"] = OrderedDict({
    "white": "#ffffff",
    "black": "#000000"
})

with open("colors.json", "w") as f:
    json.dump(palette, f, indent=2)

print("✅ Palet dari hue berhasil dibuat dan disimpan ke 'colors.json'")

# Run python generate_hue.py && python generate-css.py
