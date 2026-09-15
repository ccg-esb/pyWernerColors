"""Palette access and interpolation."""

from __future__ import annotations

from typing import Iterable, Literal

import matplotlib.colors as mcolors
import numpy as np

from ._data import load_palettes

PaletteType = Literal["discrete", "continuous"]


def list_palettes() -> list[str]:
    """Return all bundled palette names."""
    return sorted(load_palettes())


def _validate_direction(direction: int) -> None:
    if direction not in (1, -1):
        raise ValueError("direction must be 1 or -1")


def _validate_n(n: int | None) -> None:
    if n is not None and n <= 0:
        raise ValueError("n must be a positive integer")


def _base_palette(name: str, direction: int = 1) -> list[str]:
    _validate_direction(direction)
    palettes = load_palettes()
    try:
        colors = list(palettes[name])
    except KeyError as exc:
        available = ", ".join(sorted(palettes))
        raise KeyError(f"Unknown palette {name!r}. Available palettes: {available}") from exc
    if direction == -1:
        colors.reverse()
    return [mcolors.to_hex(c) for c in colors]


def _interpolate(colors: Iterable[str], n: int) -> list[str]:
    colors = list(colors)
    if not colors:
        return []
    if len(colors) == 1:
        return [mcolors.to_hex(colors[0])] * n
    cmap = mcolors.LinearSegmentedColormap.from_list("werner_interpolation", colors)
    return [mcolors.to_hex(cmap(x)) for x in np.linspace(0.0, 1.0, n)]


def palette(name: str, n: int | None = None, direction: int = 1) -> list[str]:
    """Return a discrete Werner palette as hex strings.

    If *n* exceeds the number of colours in the source palette, colours are
    interpolated across the source palette.
    """
    _validate_n(n)
    colors = _base_palette(name, direction)
    if n is None:
        return colors
    if n <= len(colors):
        return colors[:n]
    return _interpolate(colors, n)


def cmap(name: str, n: int | None = None, direction: int = 1):
    """Return a continuous Matplotlib colormap.

    When *n* is supplied, the source palette is first sampled/interpolated to
    *n* anchor colours.
    """
    _validate_n(n)
    colors = _base_palette(name, direction)
    if n is not None:
        colors = _interpolate(colors, n)
    return mcolors.LinearSegmentedColormap.from_list(f"werner_{name}", colors)


def werner_brewer(
    palette: str,
    n: int | None = None,
    type: PaletteType = "discrete",
    direction: int = 1,
    return_hex: bool = False,
):
    """Python analogue of the R package's ``werner_brewer`` function.

    Parameters
    ----------
    palette:
        Palette name.
    n:
        Number of requested colours. For discrete palettes, requesting more
        colours than the source palette triggers interpolation.
    type:
        ``"discrete"`` or ``"continuous"``.
    direction:
        ``1`` for the original order, ``-1`` for reversed order.
    return_hex:
        For discrete palettes, return hex strings instead of RGB tuples.
        For continuous palettes, return 256 sampled hex values (or *n* values
        when *n* is supplied) instead of a Matplotlib colormap.
    """
    if type not in ("discrete", "continuous"):
        raise ValueError("type must be 'discrete' or 'continuous'")

    if type == "discrete":
        colors = globals()["palette"](palette, n=n, direction=direction)
        if return_hex:
            return colors
        return [mcolors.to_rgb(color) for color in colors]

    continuous = cmap(palette, n=n, direction=direction)
    if not return_hex:
        return continuous

    sample_n = n if n is not None else 256
    return [mcolors.to_hex(continuous(x)) for x in np.linspace(0.0, 1.0, sample_n)]
