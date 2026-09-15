"""Lookup Werner colour names and find perceptually close colours."""

from __future__ import annotations

import difflib
import re
import unicodedata
from typing import Iterable

import matplotlib.colors as mcolors
import numpy as np

from ._data import load_color_table


def _normalise_name(value: str) -> str:
    value = unicodedata.normalize("NFKD", str(value)).encode("ascii", "ignore").decode("ascii")
    value = value.lower().strip().replace("grey", "gray")
    value = re.sub(r"[^a-z0-9]+", " ", value)
    value = re.sub(r"\bcolou?red\b", "colored", value)
    return re.sub(r"\s+", " ", value).strip()


def _normalise_hex(value: str) -> str:
    try:
        return mcolors.to_hex(value).upper()
    except ValueError as exc:
        raise ValueError(f"Invalid colour value: {value!r}") from exc


def colors(as_dataframe: bool = False):
    """Return the 110 Werner colours.

    By default a list of dictionaries is returned. Set ``as_dataframe=True``
    to obtain a pandas DataFrame; pandas is an optional dependency.
    """
    rows = [dict(row) for row in load_color_table()]
    if not as_dataframe:
        return rows
    try:
        import pandas as pd
    except ImportError as exc:
        raise ImportError(
            "pandas is required for as_dataframe=True; install wernercolors[dataframe]"
        ) from exc
    return pd.DataFrame(rows)


def resolve_names(
    names: Iterable[str],
    *,
    fuzzy: bool = True,
    cutoff: float = 0.6,
) -> list[str]:
    """Resolve Werner colour names to hex strings.

    Matching ignores case, punctuation, accents, and ``grey``/``gray``.
    With ``fuzzy=True``, close misspellings are accepted.
    """
    table = load_color_table()
    by_norm = {_normalise_name(row["name"]): row for row in table}
    valid = list(by_norm)
    result: list[str] = []

    for name in names:
        key = _normalise_name(name)
        row = by_norm.get(key)
        if row is None and fuzzy:
            matches = difflib.get_close_matches(key, valid, n=1, cutoff=cutoff)
            if matches:
                row = by_norm[matches[0]]
        if row is None:
            suggestions = difflib.get_close_matches(key, valid, n=5, cutoff=max(0.35, cutoff - 0.2))
            labels = [by_norm[item]["name"] for item in suggestions]
            suffix = f" Close matches: {', '.join(labels)}" if labels else ""
            raise KeyError(f"Unknown Werner colour name {name!r}.{suffix}")
        result.append(row["hex"])
    return result


def palette_from_names(names: Iterable[str], *, fuzzy: bool = True, cutoff: float = 0.6) -> list[str]:
    """Build a discrete palette from Werner colour names."""
    return resolve_names(names, fuzzy=fuzzy, cutoff=cutoff)


def _srgb_to_linear(rgb: np.ndarray) -> np.ndarray:
    return np.where(rgb <= 0.04045, rgb / 12.92, ((rgb + 0.055) / 1.055) ** 2.4)


def _rgb_to_lab(color: str) -> np.ndarray:
    rgb = np.asarray(mcolors.to_rgb(color), dtype=float)
    linear = _srgb_to_linear(rgb)
    matrix = np.array(
        [
            [0.4124564, 0.3575761, 0.1804375],
            [0.2126729, 0.7151522, 0.0721750],
            [0.0193339, 0.1191920, 0.9503041],
        ]
    )
    x, y, z = matrix @ linear
    x, y, z = x / 0.95047, y / 1.0, z / 1.08883
    epsilon = 216 / 24389
    kappa = 24389 / 27

    def f(value: float) -> float:
        return float(np.cbrt(value) if value > epsilon else (kappa * value + 16) / 116)

    fx, fy, fz = f(x), f(y), f(z)
    return np.array([116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)])


def closest_color(color: str, top_k: int = 1):
    """Find the closest Werner colour(s) using CIE76 (Delta E*ab).

    Returns one result dictionary when ``top_k=1`` and a list otherwise.
    Exact matches have ``delta_e == 0``.
    """
    if top_k <= 0:
        raise ValueError("top_k must be a positive integer")

    query_hex = _normalise_hex(color)
    query_lab = _rgb_to_lab(query_hex)
    ranked = []
    for row in load_color_table():
        delta_e = float(np.linalg.norm(query_lab - _rgb_to_lab(row["hex"])))
        ranked.append(
            {
                "query_hex": query_hex,
                "name": row["name"],
                "group": row["group"],
                "id": row["id"],
                "hex": row["hex"].upper(),
                "delta_e": delta_e,
                "exact": delta_e < 1e-12,
            }
        )
    ranked.sort(key=lambda item: item["delta_e"])
    result = ranked[:top_k]
    return result[0] if top_k == 1 else result


def werner_label_from_hex(hex_code: str, top_k: int = 3) -> dict:
    """Compatibility wrapper matching the structure used in the prototype notebook."""
    matches = closest_color(hex_code, top_k=top_k)
    matches = [matches] if isinstance(matches, dict) else matches
    first = matches[0]
    if first["exact"]:
        exact = (first["name"], first["group"], first["id"], first["hex"])
        return {"exact": exact, "nearest": []}
    nearest = [
        (m["name"], m["group"], m["id"], m["hex"], m["delta_e"])
        for m in matches
    ]
    return {"exact": None, "nearest": nearest}


def werner_labels_for_list(hex_list, top_k: int = 1, as_dataframe: bool = True):
    """Resolve multiple colours, optionally returning a pandas DataFrame."""
    rows = []
    for query in hex_list:
        matches = closest_color(query, top_k=top_k)
        matches = [matches] if isinstance(matches, dict) else matches
        for match in matches:
            rows.append(
                {
                    "query_hex": match["query_hex"],
                    "match_type": "exact" if match["exact"] else "nearest",
                    "Name": match["name"],
                    "Group": match["group"],
                    "ID": match["id"],
                    "Hex": match["hex"],
                    "deltaE": match["delta_e"],
                }
            )
    if not as_dataframe:
        return rows
    try:
        import pandas as pd
    except ImportError as exc:
        raise ImportError(
            "pandas is required for as_dataframe=True; install wernercolors[dataframe]"
        ) from exc
    return pd.DataFrame(rows)
