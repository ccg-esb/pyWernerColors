import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import wernercolors as wc


def test_set_color_cycle():
    fig, ax = plt.subplots()
    colors = wc.set_color_cycle(ax, "Firebirds", n=4)
    assert len(colors) == 4
    plt.close(fig)


def test_plot_palette_strip():
    fig, ax = wc.plot_palette_strip(["#000000", "#ffffff"], show=False)
    assert fig is not None
    assert ax is not None
    plt.close(fig)
