from nicegui import ui
from layout import page_layout
from datetime import date 
import store
import rules


@ui.page('/customer/{customer_id}')
def customer(customer_id: int):
    c = store.customers[customer_id]
    page_layout()
    with ui.column().classes('w-full max-w-screen-2xl mx-auto px-6 py-3 gap-4 print:p-0'):  # centered page column with padding (py-3 / gap-4 keep it short enough that the page doesn't scroll)
        with ui.row().classes('w-full items-center justify-between'):
            ui.label(c['name']).classes('text-2xl font-bold')
            with ui.tabs().props('inline-label dense').classes('print:hidden') as tabs:
                test_tab = ui.tab('Water Tests', icon='science')
                problems_tab = ui.tab('Problems', icon='report_problem')
                purchases_tab = ui.tab('Purchases',icon='shopping_cart')
        with ui.row().classes('w-full no-wrap gap-6 items-stretch print:flex-col print:gap-3 md:min-h-[calc(100vh-11.5rem)] print:min-h-0'):  # items-stretch: both columns get the same height (the row's)
            with ui.column().classes('w-1/3 print:w-full print:flex-row'):  # the info cards set the row's height

                #---------- Contact Card ----------
                with ui.card().classes('w-full gap-1 print:flex-1'):
                    ui.label('Contact').classes('text-lg font-semibold')
                    ui.label('Address').classes('text-xs text-gray-500')
                    ui.label(c['address'])
                    ui.label('Phone').classes('text-xs text-gray-500')
                    ui.label(c['phone'])
                    ui.label('Customer since').classes('text-xs text-gray-500')
                    ui.label(c['since'])

                #---------- Pool Card ----------
                with ui.card().classes('w-full gap-1 print:flex-1'):
                    if not c['bodies']:
                        ui.label('Pool').classes('text-lg font-semibold')
                        ui.label('No pool on file').classes('text-gray-500')
                    else:
                        b = c['bodies'][0]  # first body for now (switcher comes in step E)
                        ui.label(b['type']).classes('text-lg font-semibold')  # 'Pool' or 'Hot tub'
                        ui.label('Size').classes('text-xs text-gray-500')
                        ui.label(f"{b['size']} · {b['gallons']:,} gal")  # :, adds the thousands comma
                        if b['type'] == 'Pool':  # pools and hot tubs have different fields
                            ui.label('Wall / liner').classes('text-xs text-gray-500')
                            ui.label(b['wall_liner'])
                            ui.label('Floor').classes('text-xs text-gray-500')
                            ui.label(b['floor'])
                            ui.label('Chlorinator').classes('text-xs text-gray-500')
                            ui.label(b['chlorinator'])
                        else:
                            ui.label('Shell').classes('text-xs text-gray-500')
                            ui.label(b['shell'])
                            ui.label('Cover').classes('text-xs text-gray-500')
                            ui.label(b['cover'])
                        ui.label('Filter').classes('text-xs text-gray-500')
                        ui.label(b['filter'])
                        ui.label('Installed').classes('text-xs text-gray-500')
                        ui.label(b['installed'])

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
                                ui.label(f"Latest test · {c['tests'][0]['date']}" if c['tests'] else 'No tests yet').classes('text-lg font-semibold')
                                with ui.row().classes('items-center gap-2 print:hidden'):
                                    ui.button(icon='print',on_click=lambda: ui.run_javascript('window.print()')).props('flat round')  #Print button
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
                        rows = [{**t, **rules.test_colors(t)} for t in c['tests']] #** ** merges two dicts into a new one. 
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

                        with ui.row().classes('w-full no-wrap gap-4 items-stretch'):
                            with ui.card().classes('w-1/3'):
                                ui.label('Log a Problem').classes('text-lg font-semibold')
                                problem_description = ui.textarea(placeholder="Describe the customer's problem...").props('outlined rows=5 input-style="max-height: 8rem"').classes('w-full')#autogrow starts the box at one line and grows on as the user types. input-style="max-height: 8rem allows a scroll bar within the textbox so if the description of the problem becomes that long it will stay contained within that card and not flow outside causing the screen to want to scroll.
                                with ui.row().classes('w-full justify-end mt-auto'): #mt-auto pushes the button the the bottom of the card
                                    ui.button('Get Suggestion',on_click=lambda: suggestion_box.set_visibility(True))

                    #---------- Suggestion ----------
                            with ui.card().classes('flex-1'):
                                ui.label('Fix').classes('text-lg font-semibold')
                                with ui.column().classes('w-full') as suggestion_box:
                                    ui.label('Suggestions').classes('text-lg text-gray-500')
                                    selection = ui.radio(suggestions,on_change=lambda e: fix_box.set_value(e.value))#e.value is the suggestion text that was picked. .set value is how you change an elements value from code
                                suggestion_box.set_visibility(False)
                                fix_box = ui.textarea(label='Fix applied').props('outlined clearable autogrow input-style="max-height: 8rem"').classes('w-full')
                                with ui.row().classes('w-full justify-end mt-auto'):
                                    ui.button('Save Fix',icon='check')

                        with ui.card().classes('w-full min-h-0'):
                            ui.label('Problem history').classes('text-lg font-semibold')
                            with ui.list().props('separator').classes('w-full flex-1 min-h-0 overflow-y-auto'):  #this allows the problem history to scroll and not making the entire screen want to scroll when data starts to get longer than the screen
                                for p in c['problems']:  #each problem dict
                                    if p['fix'] is None:
                                        continue
                                    with ui.item():
                                        with ui.item_section():
                                            ui.item_label(f"{p['date']} · {p['title']}")
                                            ui.item_label(p['fix']).props('caption')


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
                            {'date': 'Oct 15, 2026', 'product': 'Cal-hypo shock (73%)',     'brand': 'HTH',               'qty': 2, 'size': '1 lb bag'},
                            {'date': 'Oct 15, 2026', 'product': 'pH reducer',               'brand': 'HTH',               'qty': 1, 'size': '5 lb tub'},
                            {'date': 'Oct 15, 2026', 'product': 'Algaecide 60',             'brand': 'BioGuard',          'qty': 1, 'size': '1 qt'},
                            {'date': 'Sep 2, 2026',  'product': 'Clarifier',                'brand': 'Natural Chemistry', 'qty': 1, 'size': '1 qt'},
                            {'date': 'Jul 20, 2026', 'product': 'Floating chlorinator',     'brand': 'Pool Time',         'qty': 1, 'size': '—'},
                            {'date': 'Jul 20, 2026', 'product': '3" chlorine tabs',         'brand': 'HTH',               'qty': 1, 'size': '5 lb tub'},
                            {'date': 'Jun 28, 2026', 'product': 'Alkalinity increaser',     'brand': 'Arm & Hammer',      'qty': 3, 'size': '1 lb box'},
                            {'date': 'Jun 28, 2026', 'product': 'Opening kit',              'brand': 'HTH',               'qty': 1, 'size': '15k gal kit'},
                        ]
                        products = [
                            'Cal-hypo shock (73%)', 'pH reducer', 'pH increaser', 'Alkalinity increaser',
                            'Calcium hardness increaser', 'Algaecide 60', 'Clarifier', '3" chlorine tabs',
                            'Stabilizer (CYA)', 'Phosphate remover', 'Floating chlorinator', 'Opening kit',
                        ]

                        #---------- Purchase Dialog ----------
                        
                        with ui.dialog() as purchase_dialog, ui.card().classes('w-96'):
                            ui.label('Log Purchase').classes('w-full font-semibold text-lg')
                            ui.select(products,with_input=True, label='Product').classes('w-full').props('outlined dense')
                            with ui.grid(columns=2).classes('w-full gap-3'):
                                ui.input(label='Date',value=date.today().strftime('%b %d, %Y')).props('outlined dense')
                                ui.number(label='Qty', value=1, min=1).props('outlined dense')
                            with ui.row().classes('w-full justify-end'):
                                ui.button('Cancel', on_click=purchase_dialog.close).props('flat')
                                ui.button('Save', icon='check',on_click=purchase_dialog.close)
                        #-------------------------------------
                        with ui.card().classes('w-full'):
                            with ui.row().classes('w-full items-center justify-between'):
                                ui.label('Purchases').classes('text-lg font-semibold')
                                ui.button('Log Purchase', icon='add', on_click=purchase_dialog.open)
                            ui.table(columns=purchase_columns, rows=purchase_rows).classes('w-full').props('flat bordered')
