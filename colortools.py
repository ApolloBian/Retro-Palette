#!/usr/bin/env python
"""
A few suggestions:
    1. Don't make mistakes, mistakes are more expensive
    2. Avoid bugs and code that works in 80% cases
    3. Keep track of things that needs to be tied up
    4. Leverage consistency, reuse instead of creating again
"""


# used colors
from colorutils import Color
import colorsys
import json

def hls_to_hsl_literal(h, l, s):
    h = int(h * 360)
    l = int(l * 100)
    s = int(s * 100)
    return f"hsl({h:d}, {s:d}%, {l:d}%)"

def pfloat(k):
    if '%' in k:
        return float(k.replace('%', ''))/100
    else:
        return float(k)

def hsl_literal_to_hls(hsl_str):
    hsl_str = hsl_str.split('(')[-1].split(')')[0]
    h, s, l = hsl_str.split(',')

    h = pfloat(h.strip()) / 360
    s = pfloat(s.strip())
    l = pfloat(l.strip())
    return h, l, s


def rgb_to_hex(rgb_literal):
    rgb_literal = rgb_literal.split('(')[-1].split(')')[0]
    r, g, b = rgb_literal.split(',')
    r = max(pfloat(r.strip()), 255.0)
    g = max(pfloat(g.strip()), 255.0)
    b = max(pfloat(b.strip()), 255.0)
    return Color(rgb=(r, g, b)).hex



def hsl_to_hex(hsl_literal):
    hls = hsl_literal_to_hls(hsl_literal)
    r, g, b = colorsys.hls_to_rgb(*hls)
    hexval = Color(rgb=(r*255, g*255, b*255)).hex
    return hexval

def auto_parse_to_hex(color_def_string):
    if 'rgb' in color_def_string:
        return rgb_to_hex(color_def_string)
    if 'hsl' in color_def_string:
        return hsl_to_hex(color_def_string)


def color_mix(hex1, hex2, weight):
    c1 = Color(hex=hex1).rgb
    c2 = Color(hex=hex2).rgb
    mixed = [int(a1 * weight + a2 * (1-weight)) for a1, a2 in zip(c1, c2)]
    return Color(rgb=mixed).hex


def color_distance(hex1, hex2):
    # ref: https://en.wikipedia.org/wiki/Color_difference#sRGB
    (r1, g1, b1), (r2, g2, b2) = Color(hex=hex1).rgb, Color(hex=hex2).rgb

    r_ = 0.5 * (r1+r2)
    dr = r1-r2
    dg = g1-g2
    db = b1-b2
    dc = (2 + r_/256) * dr ** 2 + 4 * dg ** 2 + (2 + (255 - r_) / 256) * db ** 2
    dc **= 0.5
    return dc

def approx_ansi(hex_color):
    c1 = hex_color
    sorted_colors = sorted(json.load(open('./ansi-256color.json')),
                           key=lambda x: color_distance(c1, x['hexString']))
    selected = sorted_colors[0]
    return [selected['colorId'], selected['hexString']]

