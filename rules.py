# ---------- Water-test ranges ----------
# Placeholder bands (Kara's real ranges still TBD; Phase 2 reads these from Settings).
# field: (red below, green from, green to, red above). Anything else is orange.
BANDS = {
    'fc':   (0.6, 1,   3,   5),
    'tc':   (0.6, 1,   3,   5),
    'ph':   (7.2, 7.4, 7.6, 7.8),
    'ta':   (60,  80,  120, 150),
    'ch':   (150, 200, 400, 500),
    'cya':  (20,  30,  50,  80),
    'phos': (0,   0,   100, 300),
}

def color_for(field, value):
    red_below, green_from, green_to, red_above = BANDS[field]
    if value < red_below or value > red_above:
        return 'red'
    if green_from <= value <= green_to:
        return 'green'
    return 'orange'

def test_colors(readings):
    """readings = {'fc': 0.5, 'ph': 7.9, ...}; blank (None) readings are skipped."""
    colors = {field: color_for(field, value) for field, value in readings.items() if value is not None}
    fc, tc = readings.get('fc'), readings.get('tc')
    if fc is not None and tc is not None and tc - fc >= 0.5 and colors['tc'] == 'green':
        colors['tc'] = 'orange'  # combined chlorine is high
    return colors
