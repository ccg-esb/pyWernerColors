import matplotlib.colors as mcolors
import pytest

import wernercolors as wc


def test_firebirds_exact_palette():
    assert wc.palette("Firebirds") == [
        "#f3e9ca", "#f3daa7", "#ebbc71", "#d17c3f",
        "#864735", "#613936", "#4d3635",
    ]


def test_component_palette_is_available():
    assert len(wc.palette("Blues")) == 11
    assert len(wc.palette("blues")) == 11


def test_werner110_has_110_colors():
    assert len(wc.palette("Werner110")) == 110


def test_interpolation_when_requesting_more_colors():
    result = wc.palette("Rocks", n=11)
    assert len(result) == 11
    assert result[0] == wc.palette("Rocks")[0]
    assert result[-1] == wc.palette("Rocks")[-1]


def test_reverse_direction():
    assert wc.palette("Leaves", direction=-1) == list(reversed(wc.palette("Leaves")))


def test_discrete_rgb_output():
    result = wc.werner_brewer("Firebirds", n=3)
    assert len(result) == 3
    assert all(len(rgb) == 3 for rgb in result)


def test_continuous_cmap():
    result = wc.cmap("Bugs")
    assert isinstance(result, mcolors.Colormap)


def test_invalid_direction():
    with pytest.raises(ValueError):
        wc.palette("Rocks", direction=0)
