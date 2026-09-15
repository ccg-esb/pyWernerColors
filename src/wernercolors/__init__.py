"""WernerColors for Python.

Colour palettes based on Werner's Nomenclature of Colours, with Matplotlib
helpers and colour-name matching utilities.
"""

from .matching import (
    closest_color,
    colors,
    palette_from_names,
    resolve_names,
    werner_label_from_hex,
    werner_labels_for_list,
)
from .matplotlib import (
    plot_palette_strip,
    plot_werner_strip,
    scale_color_werner_c,
    scale_color_werner_d,
    scale_fill_werner_c,
    scale_fill_werner_d,
    set_color_cycle,
)
from .palettes import cmap, list_palettes, palette, werner_brewer

__version__ = "0.1.0"

__all__ = [
    "cmap",
    "closest_color",
    "colors",
    "list_palettes",
    "palette",
    "palette_from_names",
    "plot_palette_strip",
    "plot_werner_strip",
    "resolve_names",
    "scale_color_werner_c",
    "scale_color_werner_d",
    "scale_fill_werner_c",
    "scale_fill_werner_d",
    "set_color_cycle",
    "werner_brewer",
    "werner_label_from_hex",
    "werner_labels_for_list",
]
