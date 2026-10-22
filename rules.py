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

def test_colors(row):
    colors =  {f'{field}_color': color_for(field, row[field]) for field in BANDS if row.get(field) is not None}
    
    if 'tc_color' in colors and row.get('fc') is not None and round(row['tc'] - row['fc'], 1) >= 0.5 and colors['tc_color'] == 'green':
        colors['tc_color'] = 'orange'
    return colors

if __name__ == '__main__':
    print(test_colors({'fc': 0.5, 'tc': 0.7, 'ph': 7.9, 'ta': 100, 'ch': 180, 'cya': 40, 'phos': 450}))
    print(test_colors({'fc': 1.8, 'tc': 2.3, 'ph': 7.5, 'ta': 100, 'ch': 250, 'cya': 40, 'phos': 50}))