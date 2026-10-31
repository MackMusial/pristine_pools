from datetime import date, timedelta
#CLAUDE WROTE THIS. I WAS NOT WRITING 300 LINES OF SAMPLE DATA FOR A SAMPLE UI
# In-memory sample data for the Phase 1 GUI. Phase 2 swaps this for PostgreSQL.
# Display dates are strings ('Oct 15, 2026'). Retest due dates are real date
# objects, relative to TODAY, so overdue / due today still works on demo day.

TODAY = date.today()

products = [  # the store's product list (Settings > Products, Log Purchase)
    {'name': 'Cal-hypo shock (73%)',       'brand': 'HTH',               'size': '1 lb bag'},
    {'name': 'pH reducer',                 'brand': 'HTH',               'size': '5 lb tub'},
    {'name': 'pH increaser',               'brand': 'HTH',               'size': '5 lb tub'},
    {'name': 'Alkalinity increaser',       'brand': 'Arm & Hammer',      'size': '1 lb box'},
    {'name': 'Calcium hardness increaser', 'brand': 'Leslie\'s',         'size': '8 lb bag'},
    {'name': 'Algaecide 60',               'brand': 'BioGuard',          'size': '1 qt'},
    {'name': 'Clarifier',                  'brand': 'Natural Chemistry', 'size': '1 qt'},
    {'name': '3" chlorine tabs',           'brand': 'HTH',               'size': '5 lb tub'},
    {'name': 'Stabilizer (CYA)',           'brand': 'BioGuard',          'size': '4 lb jug'},
    {'name': 'Phosphate remover',          'brand': 'Natural Chemistry', 'size': '1 qt'},
    {'name': 'Floating chlorinator',       'brand': 'Pool Time',         'size': '—'},
    {'name': 'Opening kit',                'brand': 'HTH',               'size': '15k gal kit'},
    {'name': 'Spa shock (MPS)',            'brand': 'Leisure Time',      'size': '2 lb jar'},
    {'name': 'Spa defoamer',               'brand': 'Leisure Time',      'size': '1 pt'},
    {'name': 'Bromine tabs',               'brand': 'Leisure Time',      'size': '1.5 lb jar'},
]

# Each customer: contact info, bodies of water (Pool / Hot tub), and their history.
# tests['body'] = index into that customer's 'bodies' list.
# problems: 'fix' is None while the problem is still OPEN.
# retest: {'due': date, 'reason': str} or None (one retest per customer).
customers = {
    1: {
        'name': 'Nick McArdle', 'phone': '(989) 555-0142',
        'address': '4127 Bay Rd, Saginaw, MI 48603', 'since': 'May 2026',
        'bodies': [
            {'type': 'Pool', 'size': '24 ft round · 52 in wall', 'gallons': 15000,
             'wall_liner': 'Hard-sided steel · 25 mil overlap liner', 'floor': 'Sand base',
             'filter': 'Sand filter · 150 lbs sand', 'chlorinator': 'None',
             'installed': 'June 2026 · Great Lakes Pool Install', 'changes': []},
        ],
        'tests': [
            {'date': 'Oct 15, 2026', 'body': 0, 'fc': 0.5, 'tc': 0.7, 'ph': 7.9, 'ta': 100, 'ch': 180, 'cya': 40, 'phos': 450},
            {'date': 'Oct 1, 2026',  'body': 0, 'fc': 3.0, 'tc': 3.2, 'ph': 7.5, 'ta': 100, 'ch': 190, 'cya': 40, 'phos': 200},
            {'date': 'Sep 17, 2026', 'body': 0, 'fc': 2.8, 'tc': 3.0, 'ph': 7.4, 'ta': 95,  'ch': 190, 'cya': 35, 'phos': 150},
            {'date': 'Sep 2, 2026',  'body': 0, 'fc': 1.5, 'tc': 2.0, 'ph': 7.6, 'ta': 90,  'ch': 200, 'cya': 35, 'phos': 300},
            {'date': 'Aug 14, 2026', 'body': 0, 'fc': 2.5, 'tc': 2.7, 'ph': 7.5, 'ta': 100, 'ch': 200, 'cya': 30, 'phos': 100},
            {'date': 'Jul 20, 2026', 'body': 0, 'fc': 0.8, 'tc': 1.1, 'ph': 7.6, 'ta': 110, 'ch': 210, 'cya': 30, 'phos': 100},
            {'date': 'Jun 28, 2026', 'body': 0, 'fc': 0.0, 'tc': 0.0, 'ph': 7.8, 'ta': 60,  'ch': 220, 'cya': 0,  'phos': 50},
        ],
        'problems': [
            {'date': 'Oct 15, 2026', 'title': 'Green water',
             'text': 'Pool turned green overnight. Customer shocked 2 days ago but it came back.',
             'fix': 'Lowered pH with 1.5 lbs pH reducer, then shocked with 2 lbs of cal-hypo. Brushed walls.'},
            {'date': 'Sep 2, 2026', 'title': 'Cloudy water',
             'text': 'Water cloudy after a heavy swim weekend.',
             'fix': 'Backwashed sand filter, added clarifier. Ran filter 24 hrs. Cleared in 2 days.'},
            {'date': 'Aug 26, 2026', 'title': 'Broken filter',
             'text': 'Multiport valve leaking from the waste line.',
             'fix': 'Replaced the spider gasket and lubed the valve. Filter back online same day.'},
            {'date': 'Jul 20, 2026', 'title': 'Low chlorine',
             'text': 'Chlorine keeps dropping between visits.',
             'fix': 'Raised FC with 1 lb cal-hypo. Recommended adding a floating chlorinator.'},
            {'date': 'Jun 28, 2026', 'title': 'Opening startup',
             'text': 'New pool, first fill.',
             'fix': 'Balanced alkalinity to 100 ppm with 3 lbs baking soda, initial shock with 3 lbs cal-hypo.'},
        ],
        'purchases': [
            {'date': 'Oct 15, 2026', 'product': 'Cal-hypo shock (73%)', 'brand': 'HTH',               'qty': 2, 'size': '1 lb bag'},
            {'date': 'Oct 15, 2026', 'product': 'pH reducer',           'brand': 'HTH',               'qty': 1, 'size': '5 lb tub'},
            {'date': 'Oct 15, 2026', 'product': 'Algaecide 60',         'brand': 'BioGuard',          'qty': 1, 'size': '1 qt'},
            {'date': 'Sep 2, 2026',  'product': 'Clarifier',            'brand': 'Natural Chemistry', 'qty': 1, 'size': '1 qt'},
            {'date': 'Jul 20, 2026', 'product': 'Floating chlorinator', 'brand': 'Pool Time',         'qty': 1, 'size': '—'},
            {'date': 'Jul 20, 2026', 'product': '3" chlorine tabs',     'brand': 'HTH',               'qty': 1, 'size': '5 lb tub'},
            {'date': 'Jun 28, 2026', 'product': 'Alkalinity increaser', 'brand': 'Arm & Hammer',      'qty': 3, 'size': '1 lb box'},
            {'date': 'Jun 28, 2026', 'product': 'Opening kit',          'brand': 'HTH',               'qty': 1, 'size': '15k gal kit'},
        ],
        'retest': {'due': TODAY - timedelta(days=5), 'reason': 'Green water'},  # overdue
    },
    2: {
        'name': 'Manish Shrestha', 'phone': '(989) 555-0185',
        'address': '2210 Tittabawassee Rd, Saginaw, MI 48604', 'since': 'June 2026',
        'bodies': [
            {'type': 'Pool', 'size': '18 ft round · 48 in wall', 'gallons': 7600,
             'wall_liner': 'Soft-sided · built-in liner', 'floor': 'Ground cloth',
             'filter': 'Cartridge filter', 'chlorinator': 'Floating chlorinator',
             'installed': 'June 2026 · self-installed', 'changes': []},
            {'type': 'Hot tub', 'size': '7 ft square · 6 seats', 'gallons': 400,
             'shell': 'Acrylic', 'filter': '2 cartridge filters', 'cover': 'Hard cover (2025)',
             'installed': 'Aug 2025 · came with the house', 'changes': []},
        ],
        'tests': [
            {'date': 'Oct 10, 2026', 'body': 1, 'fc': 3.5, 'tc': 3.8, 'ph': 7.8, 'ta': 90,  'ch': 160, 'cya': 20, 'phos': 100},
            {'date': 'Sep 20, 2026', 'body': 0, 'fc': 2.0, 'tc': 2.2, 'ph': 7.4, 'ta': 85,  'ch': 210, 'cya': 45, 'phos': 150},
        ],
        'problems': [],
        'purchases': [
            {'date': 'Oct 10, 2026', 'product': 'Spa shock (MPS)', 'brand': 'Leisure Time', 'qty': 1, 'size': '2 lb jar'},
            {'date': 'Sep 20, 2026', 'product': '3" chlorine tabs', 'brand': 'HTH',         'qty': 1, 'size': '5 lb tub'},
        ],
        'retest': None,
    },
    3: {
        'name': 'Marcelino J. Chapa', 'phone': '(989) 555-0136',
        'address': '5530 Shattuck Rd, Saginaw, MI 48603', 'since': 'May 2026',
        'bodies': [
            {'type': 'Pool', 'size': '15 x 30 ft oval · 52 in wall', 'gallons': 13500,
             'wall_liner': 'Hard-sided steel · 20 mil beaded liner', 'floor': 'Foam pad',
             'filter': 'Sand filter · 200 lbs sand', 'chlorinator': 'Inline chlorinator',
             'installed': 'May 2026 · Great Lakes Pool Install', 'changes': []},
        ],
        'tests': [
            {'date': 'Oct 19, 2026', 'body': 0, 'fc': 0.8, 'tc': 1.0, 'ph': 7.9, 'ta': 130, 'ch': 240, 'cya': 60, 'phos': 150},
            {'date': 'Sep 28, 2026', 'body': 0, 'fc': 2.0, 'tc': 2.1, 'ph': 7.5, 'ta': 110, 'ch': 230, 'cya': 50, 'phos': 100},
            {'date': 'Aug 30, 2026', 'body': 0, 'fc': 2.5, 'tc': 2.6, 'ph': 7.6, 'ta': 100, 'ch': 220, 'cya': 45, 'phos': 50},
        ],
        'problems': [
            {'date': 'Oct 19, 2026', 'title': 'pH creeping up',
             'text': 'pH keeps rising every week even after adding reducer.',
             'fix': 'Lowered alkalinity with 2 lbs pH reducer, aerate with the return jets pointed up. Retest pH in a week.'},
        ],
        'purchases': [
            {'date': 'Oct 19, 2026', 'product': 'pH reducer', 'brand': 'HTH', 'qty': 2, 'size': '5 lb tub'},
        ],
        'retest': {'due': TODAY, 'reason': 'pH creeping up'},  # due today
    },
    4: {
        'name': 'Keith Ho', 'phone': '(989) 555-0164',
        'address': '890 Midland Rd, Freeland, MI 48623', 'since': 'July 2026',
        'bodies': [
            {'type': 'Pool', 'size': '27 ft round · 54 in wall', 'gallons': 19000,
             'wall_liner': 'Hard-sided steel · 25 mil overlap liner', 'floor': 'Sand base',
             'filter': 'Sand filter · 250 lbs sand', 'chlorinator': 'Inline chlorinator',
             'installed': 'July 2026 · Great Lakes Pool Install', 'changes': []},
        ],
        'tests': [
            {'date': 'Sep 22, 2026', 'body': 0, 'fc': 2.2, 'tc': 2.4, 'ph': 7.5, 'ta': 95,  'ch': 250, 'cya': 40, 'phos': 80},
            {'date': 'Aug 18, 2026', 'body': 0, 'fc': 1.8, 'tc': 2.0, 'ph': 7.4, 'ta': 90,  'ch': 240, 'cya': 35, 'phos': 100},
        ],
        'problems': [],
        'purchases': [
            {'date': 'Aug 18, 2026', 'product': '3" chlorine tabs', 'brand': 'HTH', 'qty': 2, 'size': '5 lb tub'},
        ],
        'retest': None,
    },
    5: {
        'name': 'Sarah Johnson', 'phone': '(989) 555-0118',
        'address': '312 Center Rd, Saginaw, MI 48638', 'since': 'May 2026',
        'bodies': [
            {'type': 'Pool', 'size': '21 ft round · 52 in wall', 'gallons': 11500,
             'wall_liner': 'Hard-sided resin · 25 mil overlap liner', 'floor': 'Foam pad',
             'filter': 'Cartridge filter', 'chlorinator': 'Floating chlorinator',
             'installed': 'May 2026 · Great Lakes Pool Install', 'changes': []},
        ],
        'tests': [
            {'date': 'Oct 22, 2026', 'body': 0, 'fc': 2.0, 'tc': 2.2, 'ph': 7.5, 'ta': 100, 'ch': 250, 'cya': 40, 'phos': 50},
            {'date': 'Sep 24, 2026', 'body': 0, 'fc': 2.5, 'tc': 2.6, 'ph': 7.4, 'ta': 95,  'ch': 240, 'cya': 40, 'phos': 80},
            {'date': 'Aug 27, 2026', 'body': 0, 'fc': 3.0, 'tc': 3.1, 'ph': 7.6, 'ta': 100, 'ch': 230, 'cya': 35, 'phos': 100},
        ],
        'problems': [],
        'purchases': [
            {'date': 'Oct 22, 2026', 'product': '3" chlorine tabs', 'brand': 'HTH',      'qty': 1, 'size': '5 lb tub'},
            {'date': 'Aug 27, 2026', 'product': 'Stabilizer (CYA)', 'brand': 'BioGuard', 'qty': 1, 'size': '4 lb jug'},
        ],
        'retest': None,
    },
    6: {
        'name': 'Mike Kowalski', 'phone': '(989) 555-0127',
        'address': '7741 Gratiot Rd, Saginaw, MI 48609', 'since': 'June 2026',
        'bodies': [
            {'type': 'Pool', 'size': '24 ft round · 48 in wall', 'gallons': 13500,
             'wall_liner': 'Hard-sided steel · 20 mil beaded liner', 'floor': 'Sand base',
             'filter': 'Sand filter · 150 lbs sand', 'chlorinator': 'None',
             'installed': 'June 2026 · Kowalski Bros. Construction', 'changes': []},
        ],
        'tests': [
            {'date': 'Oct 20, 2026', 'body': 0, 'fc': 1.0, 'tc': 1.6, 'ph': 7.7, 'ta': 120, 'ch': 200, 'cya': 55, 'phos': 250},
            {'date': 'Sep 15, 2026', 'body': 0, 'fc': 2.0, 'tc': 2.2, 'ph': 7.5, 'ta': 110, 'ch': 210, 'cya': 50, 'phos': 100},
        ],
        'problems': [
            {'date': 'Oct 20, 2026', 'title': 'Cloudy water',
             'text': 'Water went cloudy after the leaves started falling. Filter pressure is high.',
             'fix': 'Backwashed the filter, added phosphate remover and clarifier. Skim leaves daily.'},
        ],
        'purchases': [
            {'date': 'Oct 20, 2026', 'product': 'Phosphate remover', 'brand': 'Natural Chemistry', 'qty': 1, 'size': '1 qt'},
            {'date': 'Oct 20, 2026', 'product': 'Clarifier',         'brand': 'Natural Chemistry', 'qty': 1, 'size': '1 qt'},
        ],
        'retest': {'due': TODAY, 'reason': 'Cloudy water'},  # due today
    },
    7: {
        'name': 'Emily Rivera', 'phone': '(989) 555-0133',
        'address': '1508 Weiss St, Saginaw, MI 48602', 'since': 'October 2026',
        'bodies': [
            {'type': 'Pool', 'size': '15 ft round · 42 in wall', 'gallons': 4400,
             'wall_liner': 'Soft-sided · built-in liner', 'floor': 'Ground cloth',
             'filter': 'Cartridge filter', 'chlorinator': 'None',
             'installed': 'October 2026 · self-installed', 'changes': []},
        ],
        'tests': [],  # brand-new customer: no tests yet
        'problems': [],
        'purchases': [],
        'retest': None,
    },
    8: {
        'name': 'Dave Thompson', 'phone': '(989) 555-0149',
        'address': '622 Pierce Rd, Saginaw, MI 48604', 'since': 'August 2026',
        'bodies': [
            {'type': 'Hot tub', 'size': '8 ft square · 7 seats', 'gallons': 450,
             'shell': 'Acrylic', 'filter': '3 cartridge filters', 'cover': 'Hard cover (2024)',
             'installed': 'Aug 2024 · bought used', 'changes': []},
        ],
        'tests': [
            {'date': 'Oct 20, 2026', 'body': 0, 'fc': 1.5, 'tc': 2.4, 'ph': 8.0, 'ta': 140, 'ch': 120, 'cya': 0, 'phos': 200},
            {'date': 'Sep 12, 2026', 'body': 0, 'fc': 3.0, 'tc': 3.2, 'ph': 7.6, 'ta': 110, 'ch': 150, 'cya': 0, 'phos': 100},
        ],
        'problems': [
            {'date': 'Oct 20, 2026', 'title': 'Foamy water',
             'text': 'Hot tub gets a layer of foam when the jets are on. Customer uses lotion before soaking.',
             'fix': None},  # OPEN
        ],
        'purchases': [
            {'date': 'Sep 12, 2026', 'product': 'Bromine tabs', 'brand': 'Leisure Time', 'qty': 1, 'size': '1.5 lb jar'},
        ],
        'retest': None,
    },
    9: {
        'name': 'Jessica Nguyen', 'phone': '(989) 555-0156',
        'address': '3345 McCarty Rd, Saginaw, MI 48603', 'since': 'June 2026',
        'bodies': [
            {'type': 'Pool', 'size': '16 ft round · 48 in wall', 'gallons': 5800,
             'wall_liner': 'Soft-sided · built-in liner', 'floor': 'Ground cloth',
             'filter': 'Cartridge filter', 'chlorinator': 'Floating chlorinator',
             'installed': 'June 2026 · self-installed', 'changes': []},
        ],
        'tests': [
            {'date': 'Oct 16, 2026', 'body': 0, 'fc': 0.3, 'tc': 0.5, 'ph': 7.6, 'ta': 80,  'ch': 180, 'cya': 90, 'phos': 100},
            {'date': 'Sep 10, 2026', 'body': 0, 'fc': 1.5, 'tc': 1.7, 'ph': 7.5, 'ta': 85,  'ch': 190, 'cya': 70, 'phos': 50},
        ],
        'problems': [
            {'date': 'Oct 16, 2026', 'title': 'Low chlorine',
             'text': 'Chlorine reads near zero even with tabs in the floater.',
             'fix': 'CYA too high (90), so the chlorine is locked up. Drained and refilled 1/3 of the pool, then shocked with 1 lb cal-hypo.'},
        ],
        'purchases': [
            {'date': 'Oct 16, 2026', 'product': 'Cal-hypo shock (73%)', 'brand': 'HTH', 'qty': 1, 'size': '1 lb bag'},
        ],
        'retest': {'due': TODAY + timedelta(days=1), 'reason': 'Low chlorine'},
    },
    10: {
        'name': 'Tom Brennan', 'phone': '(989) 555-0161',
        'address': '4402 Mackinaw Rd, Saginaw, MI 48603', 'since': 'May 2026',
        'bodies': [
            {'type': 'Pool', 'size': '30 ft round · 54 in wall', 'gallons': 23000,
             'wall_liner': 'Hard-sided steel · 25 mil overlap liner', 'floor': 'Sand base',
             'filter': 'Sand filter · 300 lbs sand', 'chlorinator': 'Inline chlorinator',
             'installed': 'May 2026 · Great Lakes Pool Install', 'changes': []},
        ],
        'tests': [
            {'date': 'Oct 5, 2026',  'body': 0, 'fc': 2.5, 'tc': 2.7, 'ph': 7.4, 'ta': 100, 'ch': 280, 'cya': 45, 'phos': 100},
            {'date': 'Sep 1, 2026',  'body': 0, 'fc': 2.0, 'tc': 2.1, 'ph': 7.5, 'ta': 105, 'ch': 270, 'cya': 40, 'phos': 150},
        ],
        'problems': [],
        'purchases': [
            {'date': 'Oct 5, 2026', 'product': '3" chlorine tabs', 'brand': 'HTH', 'qty': 2, 'size': '5 lb tub'},
        ],
        'retest': None,
    },
    11: {
        'name': 'Amanda Schultz', 'phone': '(989) 555-0172',
        'address': '918 State St, Saginaw, MI 48602', 'since': 'July 2026',
        'bodies': [
            {'type': 'Pool', 'size': '12 x 24 ft oval · 52 in wall', 'gallons': 8500,
             'wall_liner': 'Hard-sided steel · 20 mil beaded liner', 'floor': 'Foam pad',
             'filter': 'Cartridge filter', 'chlorinator': 'None',
             'installed': 'July 2026 · Great Lakes Pool Install', 'changes': []},
        ],
        'tests': [
            {'date': 'Sep 30, 2026', 'body': 0, 'fc': 1.2, 'tc': 1.4, 'ph': 7.3, 'ta': 75,  'ch': 190, 'cya': 30, 'phos': 100},
        ],
        'problems': [],
        'purchases': [],
        'retest': None,
    },
    12: {
        'name': 'Chris Patel', 'phone': '(989) 555-0184',
        'address': '2675 Hemmeter Rd, Saginaw, MI 48603', 'since': 'June 2026',
        'bodies': [
            {'type': 'Pool', 'size': '24 ft round · 52 in wall', 'gallons': 15000,
             'wall_liner': 'Hard-sided steel · 25 mil overlap liner', 'floor': 'Sand base',
             'filter': 'Sand filter · 150 lbs sand', 'chlorinator': 'None',
             'installed': 'June 2026 · Great Lakes Pool Install', 'changes': []},
        ],
        'tests': [
            {'date': 'Oct 22, 2026', 'body': 0, 'fc': 0.4, 'tc': 0.9, 'ph': 7.9, 'ta': 130, 'ch': 200, 'cya': 30, 'phos': 600},
            {'date': 'Sep 18, 2026', 'body': 0, 'fc': 1.5, 'tc': 1.7, 'ph': 7.6, 'ta': 115, 'ch': 210, 'cya': 35, 'phos': 300},
        ],
        'problems': [
            {'date': 'Oct 22, 2026', 'title': 'Algae on walls',
             'text': 'Green-black spots on the walls near the steps. Brushing helps for a day, then they come back.',
             'fix': None},  # OPEN
        ],
        'purchases': [],
        'retest': None,
    },
    13: {
        'name': 'Linda Kaminski', 'phone': '(989) 555-0190',
        'address': '1120 Davis Rd, Saginaw, MI 48604', 'since': 'May 2026',
        'bodies': [
            {'type': 'Pool', 'size': '21 ft round · 52 in wall', 'gallons': 11500,
             'wall_liner': 'Hard-sided steel · 25 mil overlap liner', 'floor': 'Sand base',
             'filter': 'Cartridge filter', 'chlorinator': 'Inline chlorinator',
             'installed': 'May 2026 · Great Lakes Pool Install', 'changes': []},
            {'type': 'Hot tub', 'size': '6 ft round · 4 seats', 'gallons': 300,
             'shell': 'Rotomolded', 'filter': '1 cartridge filter', 'cover': 'Soft cover',
             'installed': 'Sept 2026 · Pristine Pools', 'changes': []},
        ],
        'tests': [
            {'date': 'Oct 12, 2026', 'body': 1, 'fc': 3.0, 'tc': 3.1, 'ph': 7.5, 'ta': 90,  'ch': 160, 'cya': 0,  'phos': 50},
            {'date': 'Oct 12, 2026', 'body': 0, 'fc': 2.5, 'tc': 2.6, 'ph': 7.4, 'ta': 95,  'ch': 220, 'cya': 40, 'phos': 100},
            {'date': 'Sep 14, 2026', 'body': 0, 'fc': 2.0, 'tc': 2.2, 'ph': 7.5, 'ta': 100, 'ch': 215, 'cya': 40, 'phos': 150},
        ],
        'problems': [],
        'purchases': [
            {'date': 'Oct 12, 2026', 'product': 'Spa shock (MPS)',  'brand': 'Leisure Time', 'qty': 1, 'size': '2 lb jar'},
            {'date': 'Sep 14, 2026', 'product': '3" chlorine tabs', 'brand': 'HTH',          'qty': 1, 'size': '5 lb tub'},
        ],
        'retest': None,
    },
    14: {
        'name': "Ryan O'Connell", 'phone': '(989) 555-0103',
        'address': '5016 Bay Rd, Saginaw, MI 48604', 'since': 'June 2026',
        'bodies': [
            {'type': 'Pool', 'size': '18 x 33 ft oval · 54 in wall', 'gallons': 18000,
             'wall_liner': 'Hard-sided steel · 25 mil overlap liner', 'floor': 'Foam pad',
             'filter': 'Sand filter · 250 lbs sand', 'chlorinator': 'Inline chlorinator',
             'installed': 'June 2026 · Great Lakes Pool Install', 'changes': []},
        ],
        'tests': [
            {'date': 'Oct 19, 2026', 'body': 0, 'fc': 2.0, 'tc': 2.2, 'ph': 7.4, 'ta': 90,  'ch': 140, 'cya': 45, 'phos': 100},
        ],
        'problems': [
            {'date': 'Oct 19, 2026', 'title': 'Liner stains',
             'text': 'Brown stains on the liner floor where leaves sat. Customer worried it is metal staining.',
             'fix': None},  # OPEN
        ],
        'purchases': [],
        'retest': None,
    },
    15: {
        'name': 'Megan Fischer', 'phone': '(989) 555-0115',
        'address': '73 Oakwood Ct, Bay City, MI 48706', 'since': 'October 2026',
        'bodies': [],  # just added: no pool on file yet
        'tests': [],
        'problems': [],
        'purchases': [],
        'retest': None,
    },
    16: {
        'name': 'Jake Wojcik', 'phone': '(989) 555-0138',
        'address': '2901 Eastman Ave, Midland, MI 48640', 'since': 'May 2026',
        'bodies': [
            {'type': 'Pool', 'size': '28 ft round · 52 in wall', 'gallons': 20000,
             'wall_liner': 'Hard-sided steel · 25 mil overlap liner', 'floor': 'Sand base',
             'filter': 'Sand filter · 250 lbs sand', 'chlorinator': 'Floating chlorinator',
             'installed': 'May 2026 · Great Lakes Pool Install', 'changes': []},
        ],
        'tests': [
            {'date': 'Oct 13, 2026', 'body': 0, 'fc': 1.5, 'tc': 1.7, 'ph': 7.5, 'ta': 100, 'ch': 230, 'cya': 45, 'phos': 800},
            {'date': 'Sep 8, 2026',  'body': 0, 'fc': 2.0, 'tc': 2.1, 'ph': 7.5, 'ta': 100, 'ch': 225, 'cya': 40, 'phos': 400},
        ],
        'problems': [
            {'date': 'Oct 13, 2026', 'title': 'High phosphates',
             'text': 'Phosphates at 800 ppb; chlorine use has doubled.',
             'fix': 'Added a full quart of phosphate remover, ran the filter 48 hrs, then backwashed.'},
        ],
        'purchases': [
            {'date': 'Oct 13, 2026', 'product': 'Phosphate remover', 'brand': 'Natural Chemistry', 'qty': 1, 'size': '1 qt'},
        ],
        'retest': {'due': TODAY - timedelta(days=2), 'reason': 'High phosphates'},  # overdue
    },
}

def search_options():
    options = {}
    for cid, c in customers.items():
        options[cid] = f"{c['name']} · {c['phone']}" 
    return options

def search_pools():
    pools = {}
    for cid, c in customers.items():
        for body in c['bodies']:
            pools[body['type']] = f"{body['type']}"
    return pools

if __name__ == '__main__':
    print(search_options())