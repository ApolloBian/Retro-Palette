#!/usr/bin/env python
"""
use yy:@" to execute the following command, this will show correct hsl color
call css_color#init('css', 'extended', 'cssMediaBlock,cssFunction,cssDefinition,cssAttrRegion')
"""

from collections import defaultdict
import json
import colorsys
from colorutils import Color
from colortools import hsl_literal_to_hls, hls_to_hsl_literal, hsl_to_hex, color_distance, approx_ansi
# all ansi colors:
# black red green yellow blue magenta cyan white

ansi_alias = {
    'black': 'color0', 'light_black': 'color8',
    'red': 'color1', 'light_red': 'color9',
    'green': 'color2', 'light_green': 'color10',
    'yellow': 'color3', 'light_yellow': 'color11',
    'blue': 'color4', 'light_blue': 'color12',
    'magenta': 'color5', 'light_magenta': 'color13',
    'cyan': 'color6', 'light_cyan': 'color14',
    'white': 'color7', 'light_white': 'color15',
}
ansi_alias.update({v: k for k, v in ansi_alias.items()})

ansi_hsl = {
    "black": "hsl(0, 0%, 0%)",
    "light_black": "hsl(0, 0%, 70%)",
    "red": "hsl(0, 80%, 39%)",
    "light_red": "hsl(0, 80%, 47%)",
    "green": "hsl(170, 80%, 28%)",
    "light_green": "hsl(170, 80%, 36%)",
    "yellow": "hsl(50, 97%, 50%)",
    "light_yellow": "hsl(50, 100%, 50%)",
    "blue": "hsl(214, 80%, 28%)",
    "light_blue": "hsl(215, 80%, 40%)",
    "magenta": "hsl(287, 80%, 39%)",
    "light_magenta": "hsl(287, 80%, 47%)",
    "cyan": "hsl(192, 80%, 28%)",
    "light_cyan": "hsl(192, 80%, 33%)",
    "white": "hsl(0, 0%, 95%)",
    "light_white": "hsl(0, 0%, 100%)"
}

colors = defaultdict(lambda: defaultdict(dict))


# generate shades
num_shades = 20
shades = {}
for i in range(num_shades):
    hls = (0, 1 / num_shades * i, 0)
    r, g, b = colorsys.hls_to_rgb(*hls)
    hex_color = Color(rgb=(r*255, g*255, b*255)).hex
    shades[f"shade{i*5:02d}"] = hex_color

colors['hex']['shades'] = shades


# generate hex color
for name, hslval in ansi_hsl.items():
    colors['hex']['ansi'][name] = hsl_to_hex(hslval)

colors['hex']['ansi_enum'] = {ansi_alias[k]: v for k,
                              v in colors['hex']['ansi'].items()}


for kname in colors['hex'].keys():
    colors['8bit_hex'][kname] = {
        k: [*approx_ansi(v), v] for k, v in colors['hex'][kname].items()}
    colors['8bit'][kname] = {k: v[0]
                             for k, v in colors['8bit_hex'][kname].items()}


with open('colors.json', 'w') as f:
    json.dump(colors, f, indent=4)
