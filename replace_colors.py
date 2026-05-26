import os

file_path = "presentation/script.js"
with open(file_path, "r") as f:
    content = f.read()

replacements = {
    "oklch(84% 0.16 85)": "oklch(80% 0.15 80)",   # gold
    "oklch(82% 0.16 205)": "oklch(85% 0.14 200)", # cyan
    "oklch(72% 0.22 335)": "oklch(72% 0.18 335)", # magenta
    "oklch(78% 0.18 145)": "oklch(78% 0.15 145)", # green
    "oklch(8% 0.015 260)": "oklch(12% 0.025 285)",# bg
    "oklch(12% 0.018 260)": "oklch(18% 0.035 285)",# surface
    "oklch(94% 0.01 90)": "oklch(95% 0.015 285)", # text
    "oklch(73% 0.025 275)": "oklch(75% 0.03 285)",# muted
    "oklch(31% 0.035 270)": "oklch(28% 0.04 285)",# line
    "rgba(5, 7, 18, 0.92)": "rgba(18, 19, 28, 0.92)", # map undefined
    "rgba(2, 4, 13, 0.95)": "rgba(18, 19, 28, 0.95)", # map dark
}

for old, new in replacements.items():
    content = content.replace(old, new)

with open(file_path, "w") as f:
    f.write(content)

print("Colors updated in script.js")
