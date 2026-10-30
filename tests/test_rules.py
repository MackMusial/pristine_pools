import pytest
import rules  # not `from rules import test_colors`: pytest would think that function is a test


# ---------- color_for ----------
@pytest.mark.parametrize('field, value, expected', [
    ('fc', 2.0, 'green'),   # middle of the green band
    ('fc', 1, 'green'),     # green edges count as green
    ('fc', 3, 'green'),
    ('fc', 0.8, 'orange'),  # between red and green
    ('fc', 4.0, 'orange'),
    ('fc', 0.6, 'orange'),  # red edges are still orange (red is strictly below / above)
    ('fc', 5, 'orange'),
    ('fc', 0.5, 'red'),
    ('fc', 5.1, 'red'),
    ('ph', 7.4, 'green'),   # pH edges: green 7.4–7.6, orange 7.2–7.3 / 7.7–7.8
    ('ph', 7.6, 'green'),
    ('ph', 7.3, 'orange'),
    ('ph', 7.7, 'orange'),
    ('ph', 7.2, 'orange'),
    ('ph', 7.8, 'orange'),
    ('ph', 7.1, 'red'),
    ('ph', 7.9, 'red'),
    ('ta', 100, 'green'),
    ('ta', 59, 'red'),
    ('ch', 450, 'orange'),
    ('cya', 0, 'red'),      # a brand-new pool with no stabilizer
    ('phos', 0, 'green'),   # phosphates: lower is better, so 0 is green
    ('phos', 100, 'green'),
    ('phos', 200, 'orange'),
    ('phos', 450, 'red'),
])
def test_color_for(field, value, expected):
    assert rules.color_for(field, value) == expected


def test_every_band_is_in_order():
    for field, (red_below, green_from, green_to, red_above) in rules.BANDS.items():
        assert red_below <= green_from <= green_to <= red_above, field


def test_unknown_field_raises():
    with pytest.raises(KeyError):
        rules.color_for('salt', 3000)


# ---------- test_colors ----------
def test_colors_for_a_full_row():
    row = {'fc': 0.5, 'tc': 0.7, 'ph': 7.9, 'ta': 100, 'ch': 180, 'cya': 40, 'phos': 450}
    assert rules.test_colors(row) == {
        'fc_color': 'red', 'tc_color': 'orange', 'ph_color': 'red', 'ta_color': 'green',
        'ch_color': 'orange', 'cya_color': 'green', 'phos_color': 'red',
    }


def test_blank_readings_get_no_color():
    colors = rules.test_colors({'fc': 2.0, 'tc': None, 'ph': 7.5})
    assert colors == {'fc_color': 'green', 'ph_color': 'green'}


def test_empty_row_gets_no_colors():
    assert rules.test_colors({}) == {}


def test_extra_keys_are_ignored():
    colors = rules.test_colors({'date': 'Oct 15, 2026', 'body': 0, 'ph': 7.5})
    assert colors == {'ph_color': 'green'}


@pytest.mark.parametrize('fc, tc, expected', [
    (1.8, 2.3, 'orange'),  # TC - FC = 0.5: combined chlorine, so a green TC turns orange
    (1.5, 2.0, 'orange'),  # 0.5 again
    (2.1, 2.6, 'orange'),  # 0.5 again, but float math gives 0.4999...; the round() must catch it
    (1.8, 2.2, 'green'),   # TC - FC = 0.4: fine
    (2.0, 2.0, 'green'),
])
def test_combined_chlorine_rule(fc, tc, expected):
    assert rules.test_colors({'fc': fc, 'tc': tc})['tc_color'] == expected


def test_combined_chlorine_never_hides_red():
    assert rules.test_colors({'fc': 0.1, 'tc': 6.0})['tc_color'] == 'red'


def test_combined_chlorine_skipped_without_fc():
    assert rules.test_colors({'tc': 2.5})['tc_color'] == 'green'
