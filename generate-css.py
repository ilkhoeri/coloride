import json
from pathlib import Path

# Path setup
input_path = Path(__file__).parent / "colors.json"
output_path = Path(__file__).parent / "colors.css"

# Fungsi utama untuk generate CSS custom properties
def generate_css_vars(tokens: dict) -> str:
    lines = [":root,", ":host {"]

    def walk(prefix: str, value):
        if isinstance(value, str):
            lines.append(f"  --{prefix}: {value};")
        elif isinstance(value, dict):
            for key, val in value.items():
                walk(f"{prefix}-{key}", val)

    for name, token in tokens.items():
        walk(name, token)

    lines.append("}")
    return "\n".join(lines)

# Load JSON dan generate output
with open(input_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Support struktur `json.colors` atau langsung `json`
tokens = data.get("colors", data)

css_output = generate_css_vars(tokens)

# Simpan hasil ke file
with open(output_path, "w", encoding="utf-8") as f:
    f.write(css_output)

print(f"✅ CSS variables generated at: {output_path}")
