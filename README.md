# WernerColors for Python

A Python/Matplotlib implementation of the palettes in the R package
[WernerColors](https://github.com/spiritu-santi/WernerColors), based on
*Werner's Nomenclature of Colours*.

This directory is self-contained: using the Python package does not require R.

## Development installation

```bash
cd python
python -m pip install -e .
```

## Basic use

```python
import wernercolors as wc

wc.list_palettes()
wc.palette("Firebirds", n=7)
wc.palette("Firebirds", n=7, direction=-1)
```

### Continuous Matplotlib colormap

```python
cmap = wc.cmap("Bugs")
```

### R-compatible interface

```python
colors = wc.werner_brewer(
    "Firebirds",
    n=7,
    type="discrete",
    direction=1,
    return_hex=True,
)
```

### Use a palette as a Matplotlib colour cycle

```python
import matplotlib.pyplot as plt
import wernercolors as wc

fig, ax = plt.subplots()
wc.set_color_cycle(ax, "Firebirds", n=7)
```

### Werner colour names

```python
wc.resolve_names(["Scotch Blue", "Vermilion Red"])
wc.palette_from_names(["Campanula Purple", "Siskin Green", "Leek Green"])
```

### Find the closest Werner colour

```python
wc.closest_color("#53658f")
wc.closest_color("steelblue", top_k=3)
```

Nearest-colour matching uses CIE Lab with Delta E 1976, matching the prototype
implementation.

### Plot a palette

```python
wc.plot_werner_strip("Rocks")
```

