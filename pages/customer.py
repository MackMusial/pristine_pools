from nicegui import ui
from layout import page_layout, CUSTOMERS


@ui.page('/customer/{customer_id}')
def customer(customer_id: int):
    name, phone = CUSTOMERS[customer_id].split(' · ')
    page_layout()
    with ui.column().classes('w-full max-w-screen-2xl mx-auto px-6 py-3 gap-4'):  # centered page column with padding (py-3 / gap-4 keep it short enough that the page doesn't scroll)
        with ui.row().classes('w-full items-center justify-between'):
            ui.label(name).classes('text-2xl font-bold')
            with ui.tabs().props('inline-label dense') as tabs:
                test_tab = ui.tab('Water Tests', icon='science')
                problems_tab = ui.tab('Problems', icon='report_problem')
                purchases_tab = ui.tab('Purchases',icon='shopping_cart')
        with ui.row().classes('w-full no-wrap gap-6 items-stretch'):  # items-stretch: both columns get the same height (the row's)
            with ui.column().classes('w-1/3'):  # the info cards set the row's height

                #---------- Contact Card ----------
                with ui.card().classes('w-full gap-1'):
                    ui.label('Contact').classes('text-lg font-semibold')
                    ui.label('Address').classes('text-xs text-gray-500')
                    ui.label('4127 Bay Rd, Saginaw, MI 48603')
                    ui.label('Phone').classes('text-xs text-gray-500')
                    ui.label(phone)
                    ui.label('Customer since').classes('text-xs text-gray-500')
                    ui.label('May 2026')

                #---------- Pool Card ----------
                with ui.card().classes('w-full gap-1'):
                    ui.label('Pool').classes('text-lg font-semibold')
                    ui.label('Size').classes('text-xs text-gray-500')
                    ui.label('24 ft round · 52 in wall · 15,000 gal')
                    ui.label('Wall / liner').classes('text-xs text-gray-500')
                    ui.label('Hard-sided steel · 25 mil overlap liner')
                    ui.label('Floor').classes('text-xs text-gray-500')
                    ui.label('Sand base')
                    ui.label('Filter').classes('text-xs text-gray-500')
                    ui.label('Sand filter · 150 lbs sand')
                    ui.label('Chlorinator').classes('text-xs text-gray-500')
                    ui.label('None')
                    ui.label('Installed').classes('text-xs text-gray-500')
                    ui.label('June 2026 · Great Lakes Pool Install')

            #----------  Water Tests ----------

            with ui.column().classes('flex-1 md:[contain:size] md:overflow-y-auto gap-0'):  # contain:size: this column's content doesn't make the row taller, so it matches the info cards and scrolls inside
                with ui.tab_panels(tabs, value=test_tab).classes('w-full flex-1 bg-transparent'):  # flex-1: the white panel fills down to the bottom of the info cards
                    with ui.tab_panel(test_tab).classes('p-1'):

                        #---------- New Test Dialog ----------
                        with ui.dialog() as test_dialog, ui.card().classes('w-96'):  #Create Dialog box for when user wants to create a new water test
                            ui.label('New Water Test').classes('text-lg font-semibold')
                            with ui.grid(columns=2).classes('w-full gap-3'):
                                ui.number(label='FC').props('outlined dense')
                                ui.number(label='TC').props('outlined dense')
                                ui.number(label='pH').props('outlined dense')
                                ui.number(label='Alk').props('outlined dense')
                                ui.number(label='Hardness').props('outlined dense')
                                ui.number(label='CYA').props('outlined dense')
                                ui.number(label='Phosphates').props('outlined dense')
                            with ui.row().classes('w-full justify-end'):
                                ui.button('Cancel', on_click=test_dialog.close).props('flat')
                                ui.button('Save', icon='check',on_click=test_dialog.close)
                                    


                        #---------- Latest Test Card ----------
                        with ui.card().classes('w-full'):  #latest test card
                            with ui.row().classes('w-full items-center justify-between'):
                                ui.label('Latest test · Oct 15').classes('text-lg font-semibold')
                                with ui.row().classes('items-center gap-2'):
                                    ui.button(icon='print').props('flat round')  #Print button
                                    ui.button('New Test',icon='add',on_click=test_dialog.open)
                        columns = [
                            {'name': 'date', 'label': 'Date',     'field': 'date', 'align': 'left'},
                            {'name': 'fc',   'label': 'FC',       'field': 'fc',   'align': 'center'},
                            {'name': 'tc',   'label': 'TC',       'field': 'tc',   'align': 'center'},
                            {'name': 'ph',   'label': 'pH',       'field': 'ph',   'align': 'center'},
                            {'name': 'ta',   'label': 'Alk',      'field': 'ta',   'align': 'center'},
                            {'name': 'ch',   'label': 'Hardness', 'field': 'ch',   'align': 'center'},
                            {'name': 'cya',  'label': 'CYA',      'field': 'cya',  'align': 'center'},
                            {'name': 'phos', 'label': 'Phos',     'field': 'phos', 'align': 'center'},
                        ]
                        rows = [
                            {'date': 'Oct 15', 'fc': 0.5, 'tc': 0.7, 'ph': 7.9, 'ta': 100, 'ch': 180, 'cya': 40, 'phos': 450,
                             'fc_color': 'red', 'tc_color': 'red', 'ph_color': 'red', 'ta_color': 'green', 'ch_color': 'orange', 'cya_color': 'green', 'phos_color': 'red'},
                            {'date': 'Oct 1',  'fc': 3.0, 'tc': 3.2, 'ph': 7.5, 'ta': 100, 'ch': 190, 'cya': 40, 'phos': 200,
                             'fc_color': 'green', 'tc_color': 'green', 'ph_color': 'green', 'ta_color': 'green', 'ch_color': 'orange', 'cya_color': 'green', 'phos_color': 'orange'},
                            {'date': 'Sep 17', 'fc': 2.8, 'tc': 3.0, 'ph': 7.4, 'ta': 95,  'ch': 190, 'cya': 35, 'phos': 150,
                             'fc_color': 'green', 'tc_color': 'green', 'ph_color': 'green', 'ta_color': 'green', 'ch_color': 'orange', 'cya_color': 'green', 'phos_color': 'orange'},
                            {'date': 'Sep 2',  'fc': 1.5, 'tc': 2.0, 'ph': 7.6, 'ta': 90,  'ch': 200, 'cya': 35, 'phos': 300,
                             'fc_color': 'green', 'tc_color': 'orange', 'ph_color': 'green', 'ta_color': 'green', 'ch_color': 'green', 'cya_color': 'green', 'phos_color': 'orange'},
                            {'date': 'Aug 14', 'fc': 2.5, 'tc': 2.7, 'ph': 7.5, 'ta': 100, 'ch': 200, 'cya': 30, 'phos': 100,
                             'fc_color': 'green', 'tc_color': 'green', 'ph_color': 'green', 'ta_color': 'green', 'ch_color': 'green', 'cya_color': 'green', 'phos_color': 'green'},
                            {'date': 'Jul 20', 'fc': 0.8, 'tc': 1.1, 'ph': 7.6, 'ta': 110, 'ch': 210, 'cya': 30, 'phos': 100,
                             'fc_color': 'orange', 'tc_color': 'orange', 'ph_color': 'green', 'ta_color': 'green', 'ch_color': 'green', 'cya_color': 'green', 'phos_color': 'green'},
                            {'date': 'Jun 28', 'fc': 0.0, 'tc': 0.0, 'ph': 7.8, 'ta': 60,  'ch': 220, 'cya': 0,  'phos': 50,
                             'fc_color': 'red', 'tc_color': 'red', 'ph_color': 'orange', 'ta_color': 'orange', 'ch_color': 'green', 'cya_color': 'red', 'phos_color': 'green'},
                        ]
                        table = ui.table(columns=columns, rows=rows).classes('w-full')
                        #---------- Colored cells ----------
                        # 'body-cell' slot = a custom template used for EVERY cell in the table body
                        # the template is Vue (the browser's template language), not Python, so comments can't go inside the string.
                        #   a '#' in there gets sent to the browser as text and breaks the whole page
                        # <q-td :props="props">  -> a table cell. passing props keeps the column's alignment ('align' in columns)
                        # <q-badge v-if="...">   -> only draw a badge if this row has a color key for this column
                        #                           e.g. the FC cell looks up row['fc_color'] -> 'red'
                        # :color="..."           -> the ':' means evaluate it, so the badge color comes from the row data
                        # {{ props.value }}      -> the cell's number
                        # </q-badge>             -> closing tag: slash first, same name as the opening tag
                        # <span v-else>          -> no color key = just show the plain number
                        # phase 2: rules.py adds the _color keys by comparing each reading to the ranges in Settings
                        table.add_slot('body-cell', r'''
                            <q-td :props="props">
                                <q-badge v-if="props.row[props.col.field + '_color']"
                                        :color="props.row[props.col.field + '_color']">
                                    {{ props.value }}  
                                </q-badge>
                                <span v-else>{{ props.value }}</span>
                            </q-td>
                        ''')

                    #---------- Problems ----------
                    with ui.tab_panel(problems_tab).classes('p-1'):
                        suggestions = [
                            'Lower pH first: add about 1.5 lbs of pH reducer (sodium bisulfate), circulate 4 hours, retest. Target pH 7.4–7.6.',
                            'Shock tonight with 3 lbs of cal-hypo (73%), then brush the walls and floor. Run the filter 24 hours straight.',
                            'Add a dose of algaecide after shocking, then backwash the sand filter once the water clears. Retest in 2 days.',
                        ]
                        history = [ 
                            ('Oct 15 · Green water', 'Lowered pH with 1.5 lbs pH reducer, then shocked with 2 lbs of cal-hypo (customer shocked 2 days earlier). Brushed walls'),
                            ('Sep 2 · Cloudy water', 'Backwashed sand filter, added clarifier. Ran filter 24 hrs. Cleared in 2 days'),
                            ('Jul 20 · Low chlorine', 'Raised FC with 1 lb cal-hypo. Recommended adding a floating chlorinator.'),
                            ('Jun 28 · Opening startup', 'Balanced alkalinity to 100 ppm with 3 lbs baking soda, initial shock with 3 lbs cal-hypo'),
                        ]
                        with ui.row().classes('w-full no-wrap gap-4 items-stretch'):
                            with ui.card().classes('w-1/3'):
                                ui.label('Log a Problem').classes('text-lg font-semibold')
                                problem_description = ui.textarea(placeholder="Describe the customer's problem...").props('outlined rows=5 input-style="max-height: 8rem"').classes('w-full')#autogrow starts the box at one line and grows on as the user types. input-style="max-height: 8rem allows a scroll bar within the textbox so if the description of the problem becomes that long it will stay contained within that card and not flow outside causing the screen to want to scroll.
                                with ui.row().classes('w-full justify-end mt-auto'): #mt-auto pushes the button the the bottom of the card
                                    ui.button('Get Suggestion')

                    #---------- Suggestion ----------
                            with ui.card().classes('flex-1'):
                                ui.label('Suggestions').classes('text-lg font-semibold')
                                selection = ui.radio(suggestions,on_change=lambda e: fix_box.set_value(e.value))#e.value is the suggestion text that was picked. .set value is how you change an elements value from code
                                fix_box = ui.textarea(label='Fix applied').props('outlined clearable autogrow input-style="max-height: 8rem"').classes('w-full')
                                with ui.row().classes('w-full justify-end'):
                                    ui.button('Save Fix',icon='check')

                        with ui.card().classes('w-full'):
                            ui.label('Problem history').classes('text-lg font-semibold')
                            with ui.list().props('separator').classes('w-full max-h-48 overflow-y-auto'):  #this allows the problem history to scroll and not making the entire screen want to scroll when data starts to get longer than the screen
                                for problem, fix in history:  #forloop to iterate through each tuple in history
                                    with ui.item():
                                        with ui.item_section():
                                            ui.item_label(problem)
                                            ui.item_label(fix).props('caption')


                    #---------- Purchases Tab ----------
                    with ui.tab_panel(purchases_tab).classes('p-1'): #p-1 removes the padding down to 4px (tailwind's spacing scale is x4)
                        purchase_columns = [
                            {'name': 'date',    'label': 'Date',    'field': 'date', 'align': 'left'},
                            {'name': 'product', 'label': 'Product', 'field': 'product', 'align': 'left'},
                            {'name': 'brand',   'label': 'Brand',   'field': 'brand', 'align': 'left'},
                            {'name': 'qty',     'label': 'Qty',     'field': 'qty', 'align': 'center'},
                            {'name': 'size',    'label': 'Size',    'field': 'size', 'align': 'center'},
                        ]
                        purchase_rows = [
                            {'date': 'Oct 15', 'product': 'Cal-hypo shock (73%)',     'brand': 'HTH',               'qty': 2, 'size': '1 lb bag'},
                            {'date': 'Oct 15', 'product': 'pH reducer',               'brand': 'HTH',               'qty': 1, 'size': '5 lb tub'},
                            {'date': 'Oct 15', 'product': 'Algaecide 60',             'brand': 'BioGuard',          'qty': 1, 'size': '1 qt'},
                            {'date': 'Sep 2',  'product': 'Clarifier',                'brand': 'Natural Chemistry', 'qty': 1, 'size': '1 qt'},
                            {'date': 'Jul 20', 'product': 'Floating chlorinator',     'brand': 'Pool Time',         'qty': 1, 'size': '—'},
                            {'date': 'Jul 20', 'product': '3" chlorine tabs',         'brand': 'HTH',               'qty': 1, 'size': '5 lb tub'},
                            {'date': 'Jun 28', 'product': 'Alkalinity increaser',     'brand': 'Arm & Hammer',      'qty': 3, 'size': '1 lb box'},
                            {'date': 'Jun 28', 'product': 'Opening kit',              'brand': 'HTH',               'qty': 1, 'size': '15k gal kit'},
                        ]
                        with ui.card().classes('w-full'):
                            with ui.row().classes('w-full items-center justify-between'):
                                ui.label('Purchases').classes('text-lg font-semibold')
                                ui.button('Log Purchase', icon='add')
                            ui.table(columns=purchase_columns, rows=purchase_rows).classes('w-full').props('flat bordered')
