BANDS = {  # red below, green from, green to, red above
    'fc': (0.6, 1, 3, 5),
    'tc': (0.6, 1, 3, 5),
    'ph': (7.2, 7.4, 7.6, 7.8),
    'ta': (60, 80, 120, 150),
    'ch': (150, 200, 400, 500),
    'cya': (20, 30, 50, 80),
    'phos': (0, 0, 100, 300),
}

def color_for(field, value):
    red_below, green_from, green_to, red_above = BANDS[field]
    if value < red_below or value > red_above:
        return 'red'
    if green_from <= value <= green_to:
        return 'green'
    return 'orange'

