import wernercolors as wc


def test_resolve_exact_name():
    assert wc.resolve_names(["Scotch Blue"]) == ["#281f3f"]


def test_resolve_normalised_name():
    assert wc.resolve_names(["ash gray"]) == ["#cbc8b7"]


def test_resolve_fuzzy_name():
    assert wc.resolve_names(["Vermillion Red"])[0] == "#b5493a"


def test_exact_closest_color():
    result = wc.closest_color("#281f3f")
    assert result["name"] == "Scotch Blue"
    assert result["exact"] is True
    assert result["delta_e"] == 0.0


def test_closest_color_top_k():
    result = wc.closest_color("#53658f", top_k=3)
    assert len(result) == 3
    assert result[0]["delta_e"] <= result[1]["delta_e"] <= result[2]["delta_e"]


def test_color_table_has_110_rows():
    assert len(wc.colors()) == 110
