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

def hsl_to_hex(hsl_literal):
    hls = hsl_literal_to_hls(hsl_literal)
    r, g, b = colorsys.hls_to_rgb(*hls)
    hexval = Color(rgb=(r*255, g*255, b*255)).hex
    return hexval

def hex_to_hsl(hex_literal):
    pass

