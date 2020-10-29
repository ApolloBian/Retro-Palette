#!/usr/bin/env python
"""
use yy:@" to execute the following command, this will show correct hsl color
call css_color#init('css', 'extended', 'cssMediaBlock,cssFunction,cssDefinition,cssAttrRegion')
"""

import json
import colorsys
from colorutils import Color
from colortools import hsl_literal_to_hls, hls_to_hsl_literal, hsl_to_hex
# all ansi colors:
# black red green yellow blue magenta cyan white

ansi_hsl = {
    "color0": "hsl(0, 0%, 0%)",
    "color8": "hsl(0, 0%, 70%)",
    "color1": "hsl(0, 80%, 39%)",
    "color9": "hsl(0, 80%, 47%)",
    "color2": "hsl(170, 80%, 28%)",
    "color10": "hsl(170, 80%, 36%)",
    "color3": "hsl(50, 97%, 50%)",
    "color11": "hsl(50, 100%, 50%)",
    "color4": "hsl(214, 80%, 28%)",
    "color12": "hsl(215, 80%, 40%)",
    "color5": "hsl(287, 80%, 39%)",
    "color13": "hsl(287, 80%, 47%)",
    "color6": "hsl(192, 80%, 28%)",
    "color14": "hsl(192, 80%, 33%)",
    "color7": "hsl(0, 0%, 95%)",
    "color15": "hsl(0, 0%, 100%)"
}

# generate shades
num_shades = 20
shades = { }
for i in range(num_shades):
    hls = (0, 1 / num_shades * i, 0)
    r, g, b = colorsys.hls_to_rgb(*hls)
    hex_color = Color(rgb=(r*255, g*255, b*255)).hex
    print(hex_color)
    shades[f"shade{i:d}"] = hls_to_hsl_literal(*hls)
    shades[f"shade{i:d}"] = hex_color
with open('shades_hsl.json', 'w') as f:
    json.dump(shades, f, indent=4)

# generate hex color

with open('ansi_hex.json', 'w') as f:
    ansi_hex = {}
    for name, hslval in ansi_hsl.items():
        ansi_hex[name] = hsl_to_hex(hslval)
    json.dump(ansi_hex, f, indent=4)
