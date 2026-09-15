"""Internal loaders for bundled Werner colour data."""

from __future__ import annotations

import csv
import json
from functools import lru_cache
from importlib.resources import files
from typing import Dict, List


@lru_cache(maxsize=1)
def load_color_table() -> List[dict]:
    path = files("wernercolors.data").joinpath("werner_colors.csv")
    with path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    for row in rows:
        row["id"] = int(row["id"])
    return rows


@lru_cache(maxsize=1)
def load_palettes() -> Dict[str, List[str]]:
    path = files("wernercolors.data").joinpath("palettes.json")
    with path.open("r", encoding="utf-8") as handle:
        raw = json.load(handle)
    return {name: list(colors) for name, colors in raw.items()}
