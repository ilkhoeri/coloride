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

def generate_scale_from_base_hex(name, hex_value, steps=11):
    anchor = Color(hex_value).convert('oklch').fit()
    l, c, h = anchor.coords()

    scale = OrderedDict()
    labels = ['50', '100', '200', '300', '400', '500', '600', '700', '800', '900', '1000']

    # range lightness: misalnya dari 0.98 ke 0.2, dengan 500 sebagai titik tengah
    lightness_range = [l + (0.98 - l) * (1 - i / 5) if i < 5 else l - (l - 0.2) * ((i - 5) / 5) for i in range(11)]

    for i, label in enumerate(labels):
        l_new = min(max(lightness_range[i], 0), 1)  # clamp
        color = Color('oklch', [l_new, c, h]).convert('srgb').fit()
        scale[label] = color.to_string(hex=True)

    return name, scale

colors = {
    "charcoal": "#264653",
    "persian-green": "#2a9d8f",
    "saffron": "#e9c46a",
    "sandy-brown": "#f4a261",
    "burnt-sienna": "#e76f51",
    "rich-black": "#001219ff",
    "midnight-green": "#005f73ff",
    "dark-cyan": "#0a9396ff",
    "tiffany-blue": "#94d2bdff",
    "vanilla": "#e9d8a6ff",
    "gamboge": "#ee9b00ff",
    "alloy-orange": "#ca6702ff",
    "rust": "#bb3e03ff",
    "rufous": "#ae2012ff",
    "auburn": "#9b2226ff",
    "rose": "#f72585ff",
    "fandango": "#b5179eff",
    "grape": "#7209b7ff",
    "chrysler-blue": "#560badff",
    "dark-blue": "#480ca8ff",
    "zaffre": "#3a0ca3ff",
    "palatinate-blue": "#3f37c9ff",
    "neon-blue": "#4361eeff",
    "chefchaouen-blue": "#4895efff",
    "vivid-sky-blue": "#4cc9f0ff",
}

palette = OrderedDict()


for name, props in colors.items():
    name, scale = generate_scale_from_base_hex(name, props)
    alpha = generate_overlay_alpha(scale)
    scale["overlay"] = alpha
    palette[name] = scale

# for name, hex_color in colors.items():
#     name, scale = generate_scale_from_base_hex(name, hex_color)
#     palette[name] = scale

with open("colors.json", "w") as f:
    json.dump(palette, f, indent=2)

print("✅ Skala warna berhasil dibuat dari warna dasar.")
# python main.py && python generate-css.py
