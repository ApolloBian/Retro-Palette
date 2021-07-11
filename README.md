# Retro Palette
Retro palette is my solution to colorscheme generation. It consists of
a color generation script as long as a template engine for generating
actual color scheme files.

The file `retro.py` generates a set of hex colors and closest ansi colors, it defines the color space for the colorscheme.

The file `template_engine.py` takes a template file and populates it with
defined colors from the datasource.
