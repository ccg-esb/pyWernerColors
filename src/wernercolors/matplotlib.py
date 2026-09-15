"""Matplotlib helpers for Werner palettes."""

from __future__ import annotations

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import Colormap, ListedColormap

from .palettes import cmap, palette, werner_brewer


def set_color_cycle(ax, palette_name: str, n: int | None = None, direction: int = 1):
    """Set an Axes colour cycle from a discrete Werner palette."""
    colors = palette(palette_name, n=n, direction=direction)
    ax.set_prop_cycle(color=colors)
    return colors


def scale_color_werner_d(ax, palette: str, n: int | None = None, direction: int = 1):
    """R-style compatibility alias for :func:`set_color_cycle`."""
    return set_color_cycle(ax, palette, n=n, direction=direction)


def scale_fill_werner_d(ax, palette: str, n: int | None = None, direction: int = 1):
    """R-style compatibility alias for discrete Matplotlib colour cycling."""
    return set_color_cycle(ax, palette, n=n, direction=direction)


def scale_color_werner_c(palette: str, n: int | None = None, direction: int = 1):
    """Return a continuous Werner Matplotlib colormap."""
    return cmap(palette, n=n, direction=direction)


def scale_fill_werner_c(palette: str, n: int | None = None, direction: int = 1):
    """Alias of :func:`scale_color_werner_c`."""
    return cmap(palette, n=n, direction=direction)


def _pick_text_color(hex_color: str) -> str:
    r, g, b = mcolors.to_rgb(hex_color)
    luminance = 0.2126 * r + 0.7152 * g + 0.0722 * b
    return "white" if luminance < 0.6 else "black"


def plot_palette_strip(
    colors_or_cmap,
    n: int | None = None,
    orientation: str = "horizontal",
    title: str | None = None,
    figsize=(8, 1.8),
    savepath=None,
    show: bool = True,
    labels=None,
    text_color: str = "white",
    fontsize_name: int = 10,
    fontsize_hex: int = 9,
    auto_contrast: bool = False,
):
    """Plot a palette as labelled colour swatches."""
    if orientation not in ("horizontal", "vertical"):
        raise ValueError("orientation must be 'horizontal' or 'vertical'")

    if isinstance(colors_or_cmap, Colormap):
        n = 9 if n is None else n
        colors = [mcolors.to_hex(colors_or_cmap(x)) for x in np.linspace(0, 1, n)]
    else:
        colors = [mcolors.to_hex(c) for c in colors_or_cmap]
        n = len(colors) if n is None else n
        colors = colors[:n]

    if not colors:
        raise ValueError("At least one colour is required")
    n = len(colors)
    labels = [""] * n if labels is None else (list(labels) + [""] * n)[:n]

    data = np.arange(n).reshape(1, n) if orientation == "horizontal" else np.arange(n).reshape(n, 1)
    fig, ax = plt.subplots(figsize=figsize)
    ax.imshow(data, aspect="auto", interpolation="nearest", cmap=ListedColormap(colors))
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

    for i, (name, hex_code) in enumerate(zip(labels, colors)):
        tc = _pick_text_color(hex_code) if auto_contrast else text_color
        if orientation == "horizontal":
            x, y_name, y_hex = (i + 0.5) / n, 0.38, 0.77
            rotation = 90
        else:
            x = 0.5
            center = 1 - (i + 0.5) / n
            y_name, y_hex = center + 0.05, center - 0.05
            rotation = 0
        if name:
            ax.text(x, y_name, name, transform=ax.transAxes, ha="center", va="center",
                    color=tc, fontweight="bold", fontsize=fontsize_name)
        ax.text(x, y_hex, hex_code.upper(), transform=ax.transAxes, ha="center", va="center",
                color=tc, fontsize=fontsize_hex, rotation=rotation)

    if title:
        ax.set_title(title, pad=6)
    fig.tight_layout(pad=0.2)
    if savepath:
        fig.savefig(savepath, dpi=200, bbox_inches="tight")
    if show:
        plt.show()
    return fig, ax


def plot_werner_strip(
    palette_name: str,
    n: int | None = None,
    type: str = "discrete",
    direction: int = 1,
    **kwargs,
):
    """Plot one named Werner palette."""
    if type == "continuous":
        colors = werner_brewer(palette_name, n=n, type=type, direction=direction, return_hex=True)
    else:
        colors = palette(palette_name, n=n, direction=direction)
    return plot_palette_strip(colors, n=len(colors), title=kwargs.pop("title", palette_name), **kwargs)
