from nicegui import ui
from layout import page_layout
from datetime import date, timedelta
import store
import rules

SUGGESTIONS = [
    'Lower pH first: add about 1.5 lbs of pH reducer (sodium bisulfate), circulate 4 hours, retest. Target pH 7.4–7.6.',
    'Shock tonight with 3 lbs of cal-hypo (73%), then brush the walls and floor. Run the filter 24 hours straight.',
    'Add a dose of algaecide after shocking, then backwash the sand filter once the water clears. Retest in 2 days.',
]

@ui.page('/customer/{customer_id}')
def customer(customer_id: int, tab: str = ''):
    refresh_attention = page_layout()
    if customer_id not in store.customers:
        with ui.column().classes('w-full justify-center items-center min-h-[calc(100vh-10rem)]'):
            ui.icon('warning',color='orange',size='md')
            ui.label('Customer does not exist').classes('text-gray-500 text-lg')
        return  #handle if an employee tries to find an employee that does not exist. This simply displays that no customer exists and the return stops anything else from loading
    c = store.customers[customer_id]

    # ---------- schedule_retest func ----------
    def schedule_retest(days, reason):
        with ui.dialog() as dialog, ui.card():
            ui.label('Schedule retest').classes('text-lg font-semibold')
            ui.label(reason)
            picker = ui.date(value=(store.TODAY + timedelta(days=days)).isoformat())

            # ---------- Save ----------
            def save(): 
                '''Saves the date chosen and reason for the retest to the customers retest dict
                
                This will be used for updating the left drawer's customers retest dates'''
                c['retest'] = {'due': date.fromisoformat(picker.value), 'reason': reason}  #save the retest date and reason to be display in the left drawer
                dialog.close()  #close the dialog box 
            with ui.row().classes('w-full justify-end'):
                ui.button('Skip', on_click=dialog.close).props('flat')
                ui.button('Schedule',on_click=save)  #save with no () lets save run when the button is clicked not when the page is being built. 
            refresh_attention()
        dialog.open()

    # ---------- Title row ----------
    with ui.column().classes('w-full max-w-screen-2xl mx-auto px-6 py-3 gap-4 print:p-0'):  # centered page column with padding (py-3 / gap-4 keep it short enough that the page doesn't scroll)
        with ui.row().classes('w-full items-center justify-between'):
            ui.label(c['name']).classes('text-2xl font-bold')
            with ui.tabs().props('inline-label dense no-caps').classes('print:hidden') as tabs:
                test_tab = ui.tab('Water Tests', icon='science')
                problems_tab = ui.tab('Problems', icon='report_problem')
                purchases_tab = ui.tab('Purchases',icon='shopping_cart')
        with ui.row().classes('w-full no-wrap gap-6 items-stretch print:flex-col print:gap-3 md:min-h-[calc(100vh-11.5rem)] print:min-h-0'):  # items-stretch: both columns get the same height (the row's)
            with ui.column().classes('w-1/3 print:w-full print:flex-row'):  # the info cards set the row's height

                #---------- Edit Customer Dialog ----------
                with ui.dialog() as edit_cust_dialog, ui.card().classes('w-96'):
                    ui.label('Edit Customer').classes('w-full text-lg font-semibold')
                    
                    name = ui.input(label='Name',value=c['name'], validation={'Required': lambda v: bool(v.strip())}).props('outlined dense autofocus hide-bottom-space').classes('w-full')  #the lambda: v: bool(v.strip()) forces the employee to enter a name. even if the name is full of spaces
                    phone = ui.input(label='Phone', value=c['phone'], validation={'Required': lambda v: bool(v.strip())}).props('outlined dense hide-bottom-space').classes('w-full')
                    address = ui.input(label='Address', value=c['address']).props('outlined dense').classes('w-full')

                    def edit_customer():
                        if not all ([name.validate(), phone.validate()]):  # validate() runs the check shows the red error under the box, and returns False when it fails. 
                            return
                        full_address = f"{address.value}" if address.value else ""  #add the zipcode only if one was typed, otherwise you get a trailing comma.  

                        store.customers[customer_id] = {
                            'name': name.value.strip(), 'phone': phone.value.strip(), 'address': full_address,
                            'since': c['since'],
                            'bodies': c['bodies'], 'tests': c['tests'], 'problems': c['problems'], 'purchases': c['purchases'],
                            'retest': c['retest'],
                        }

                        edit_cust_dialog.close()
                        ui.navigate.reload()
                    with ui.row().classes('w-full justify-end'):  #row for save and cancel buttons 
                        ui.button('Cancel', on_click=edit_cust_dialog.close).props('flat')
                        ui.button('Save', icon='check', on_click=edit_customer)

                #---------- Contact Card ----------
                with ui.card().classes('w-full gap-1 print:flex-1'):
                    with ui.row().classes('gap-0 items-center justify-between w-full'):
                        ui.label('Contact').classes('text-lg font-semibold')
                        ui.button(icon='edit',on_click=edit_cust_dialog.open).props('flat round dense size=sm').classes('-my-1').tooltip('Edit customer')  # size=sm + -my-1: the button doesn't make the title row taller
                    ui.label('Address').classes('text-xs text-gray-500')
                    ui.label(c['address'])
                    ui.label('Phone').classes('text-xs text-gray-500')
                    ui.label(c['phone'])
                    ui.label('Customer since').classes('text-xs text-gray-500')
                    ui.label(c['since'])

                #---------- Add Pool Dialog ----------
                with ui.dialog() as add_pool_dialog, ui.card().classes('w-96'):
                    ui.label('Add Pool').classes('font-semibold text-lg w-full')
                    ...

                #---------- Edit Pool Dialog ----------
                def open_edit_pool(i):    
                    b = c['bodies'][i]  #i represents the individual pool / hottub the customer has. i will allow us to display more than one pool without hardcoding 
                    with ui.dialog() as edit_pool_dialog, ui.card().classes('w-96'):
                        ui.label('Edit Pool').classes('font-semibold text-lg w-full')
                        if b['type'] == 'Pool':  # pools: size comes from numbers so gallons can be calculated
                            shape = ui.toggle(['Round', 'Oval'], value=b['shape'])
                            length = ui.number(label='Length / diameter (ft)', value=b['length'], min=0, validation={'Required': lambda v: bool(v)}).props('outlined dense hide-bottom-space').classes('w-full')  # bool(v): blank (None) and 0 both fail
                            width = ui.number(label='Width (ft)', value=b['width'], min=0, validation={'Required': lambda v: bool(v)}).props('outlined dense hide-bottom-space').classes('w-full').bind_visibility_from(shape, 'value', value='Oval')  # only shown for oval pools
                            wall = ui.number(label='Wall height (in)', value=b['wall'], min=0, validation={'Required': lambda v: bool(v)}).props('outlined dense hide-bottom-space').classes('w-full')
                        else:  # hot tubs: size and gallons come from the manufacturer
                            size = ui.input(label="Size",value=b['size'], validation={'Required': lambda v: bool(v.strip())}).props('outlined dense hide-bottom-space').classes('w-full')
                        gallons = ui.number(label='Gallons', value=b['gallons'], min=0, validation={'Required': lambda v: bool(v)}).props('outlined dense hide-bottom-space').classes('w-full')  # pools: filled in by recalc_gallons, but staff can still type over it

                        def recalc_gallons():  # runs whenever shape, length, width, or wall changes
                            w = length.value if shape.value == 'Round' else width.value  # round pool: width = diameter
                            if length.value and w and wall.value:  # skip while a box is blank
                                gallons.set_value(int(round(length.value * w * (wall.value / 12) * 5.9, -2)))  # ft × ft × depth in ft × 5.9, to the nearest 100

                        if b['type'] == 'Pool':
                            for box in [shape, length, width, wall]:
                                box.on_value_change(recalc_gallons)  # hooked up after gallons exists, so it's never called too early
                        filter_box = ui.input(label="Filter",value=b['filter']).props('outlined dense').classes('w-full')  #named filter filter_box because filter is a built in python function
                        installed_date = ui.input(label='Installed',value=b['installed']).props('outlined dense').classes('w-full')
                        if b['type'] == 'Pool':  #if the customer has a pool
                            wall_liner = ui.input(label="Wall / liner",value=b['wall_liner']).props('outlined dense').classes('w-full')
                            floor = ui.input(label="Floor",value=b['floor']).props('outlined dense').classes('w-full')
                            chlorinator = ui.input(label="Chlorinator",value=b['chlorinator']).props('outlined dense').classes('w-full')
                        else:  #customer has a hottub
                            shell = ui.input(label='Shell',value=b['shell']).props('outlined dense').classes('w-full')
                            cover = ui.input(label='Cover',value=b['cover']).props('outlined dense').classes('w-full')
                            
                        #---------- Edit Pool Func ----------
                        def edit_pool():
                            if b['type'] == 'Pool':
                                boxes = [length, wall, gallons] + ([width] if shape.value == 'Oval' else [])  # width is hidden (and ignored) for round pools
                            else:
                                boxes = [size, gallons]
                            if not all([box.validate() for box in boxes]):  # a list, not a generator, so every box shows its error, not just the first
                                return
                            b['filter'] = filter_box.value.strip()
                            b['installed'] = installed_date.value.strip()
                            b['gallons'] = int(gallons.value)  # whatever is in the box: calculated or typed over
                            if b['type'] == 'Pool':
                                b['wall_liner'] = wall_liner.value.strip()
                                b['floor'] = floor.value.strip()
                                b['chlorinator'] = chlorinator.value.strip()
                                b['shape'] = shape.value
                                b['length'] = length.value
                                b['width'] = length.value if shape.value == 'Round' else width.value  # round pool: width = diameter
                                b['wall'] = wall.value
                                if shape.value == 'Round':
                                    b['size'] = f"{b['length']:g} ft round · {b['wall']:g} in wall"  # :g drops the .0 from ui.number values
                                else:
                                    b['size'] = f"{b['width']:g} x {b['length']:g} ft oval · {b['wall']:g} in wall"
                            else:
                                b['shell'] = shell.value.strip()
                                b['cover'] = cover.value.strip()
                                b['size'] = size.value.strip()
                            edit_pool_dialog.close()  #Close the dialog after everything is properly saved
                            ui.navigate.reload()  #TODO: Add a @ui.refreshable to only refresh what is needed. .reload reloads the entire screen which is not needed

                        with ui.row().classes('w-full justify-end'):
                            ui.button('Cancel',on_click=edit_pool_dialog.close).props('flat')
                            ui.button('Save',icon='check', on_click=edit_pool)
                    edit_pool_dialog.open()
                        
                        

                #---------- Pool Card ----------
                with ui.card().classes('w-full gap-1 print:flex-1'):
                    with ui.row().classes('w-full items-center justify-between'):
                        if c['bodies']:
                            ui.label(c['bodies'][0]['type']).classes('text-lg font-semibold')
                        else: 
                            ui.label('Pool').classes('text-lg font-semibold')
                        with ui.row().classes('gap-0'):
                            if c['bodies']:  #ensure there is a pool to edit. if customer has no pool then remove the button to edit 
                                ui.button(icon='edit',on_click=lambda: open_edit_pool(0)).props('flat round dense size=sm').classes('-my-1').tooltip('Edit pool')  #onclick is what calls the dialogbox to appear
                            ui.button(icon='add', on_click=add_pool_dialog.open).props('flat round dense size=sm').classes('-my-1').tooltip('Add pool')

                    if not c['bodies']:
                        ui.label('No pool on file').classes('text-gray-500')
                    else:
                        b = c['bodies'][0]  # first body for now (switcher comes in step E)
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
                with ui.tab_panels(tabs, value=problems_tab if tab == 'problems' else test_tab).classes('w-full flex-1 bg-transparent'):  # flex-1: the white panel fills down to the bottom of the info cards
                    with ui.tab_panel(test_tab).classes('p-1'):

                        #---------- New Test Dialog ----------
                        with ui.dialog() as test_dialog, ui.card().classes('w-96'):  #Create Dialog box for when user wants to create a new water test
                            ui.label('New Water Test').classes('text-lg font-semibold')
                            inputs = {}

                            #---------- Save_test func ----------
                            def save_test():
                                reading = {k: box.value for k, box in inputs.items()}
                                if all(v is None for v in reading.values()):
                                    return
                                test = {'date': f"{store.TODAY:%b} {store.TODAY.day}, {store.TODAY.year}", 'body': 0, **reading}
                                c['tests'].insert(0, test)
                                table.rows.insert(0, {**test, **rules.test_colors(test)})      
                                table.update()
                                latest.set_text(f"Latest test · {test['date']}")
                                for box in inputs.values():  #clear the input box's 
                                    box.set_value(None)
                                c['retest'] = None  #clear the customers retest because this is the retest
                                colors = rules.test_colors(test).values()  #find the worst color
                                test_dialog.close()
                                if 'red' in colors:  #if there is any chemicals that are extreamly off
                                    schedule_retest(2, 'Red reading')
                                elif 'orange' in colors:  #if there is any chemicals that are slightly off
                                    schedule_retest(7, 'Orange reading')
                                refresh_attention()

                            with ui.grid(columns=2).classes('w-full gap-3'):
                                for key, label in [('fc', 'FC'), ('tc', 'TC'), ('ph', 'pH'), ('ta', 'Alk'), ('ch', 'Hardness'), ('cya', 'CYA'), ('phos', 'Phosphates'),]:
                                    inputs[key] = ui.number(label=label, min=0, step=0.1).props('outlined dense').on('keydown.enter', save_test)
                                    inputs['fc'].props('autofocus')
                            with ui.row().classes('w-full justify-end'):
                                ui.button('Cancel', on_click=test_dialog.close).props('flat')
                                ui.button('Save', icon='check',on_click=save_test)  #don't put () because that will cause the func to fire as initalization time. we only want the func to fire up when the button is clicked
                                    
                        #---------- Latest Test Card ----------
                        with ui.card().classes('w-full'):  #latest test card
                            with ui.row().classes('w-full items-center justify-between'):
                                latest = ui.label(f"Latest test · {c['tests'][0]['date']}" if c['tests'] else 'No tests yet').classes('text-lg font-semibold')
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
                                        :color="props.row[props.col.field + '_color'] + '-9'"
                                        :text-color="props.row[props.col.field + '_color'] === 'orange' ? 'black' : 'white'">
                                    {{ props.value }}  
                                </q-badge>
                                <span v-else>{{ props.value }}</span>
                            </q-td>
                        ''')

                    #---------- Problems ----------
                    with ui.tab_panel(problems_tab).classes('p-1'):

                        #check to see if there a fix associated with the problem
                        #if not assign the problem to open_p to be displayed as a problem without a fix 
                        #to alert an employee that there is a problem without a fix
                        open_p = None  
                        for p in c['problems']:
                            if p['fix'] is None:
                                open_p = p
                                break

                        with ui.row().classes('w-full no-wrap gap-4 items-stretch'):
                            with ui.card().classes('w-1/3'):
                                with ui.row().classes('w-full items-center justify-between'):    
                                    ui.label('Log a Problem').classes('text-lg font-semibold')
                                    if open_p:  #if open_p true, there is a problem without a fix so display it
                                        ui.badge(f"Open · logged {open_p['date']}", color='orange',text_color='black')
                                    # value=open_p['text'] if open_p else '' displays the open problem if there is one (thats the if open_p else '') 
                                problem_description = ui.textarea(placeholder="Describe the customer's problem...", value=open_p['text'] if open_p else '').props('outlined rows=5 input-style="max-height: 8rem"').classes('w-full')#input-style="max-height: 8rem allows a scroll bar within the textbox so if the description of the problem becomes that long it will stay contained within that card and not flow outside causing the screen to want to scroll.
                                with ui.row().classes('w-full justify-end mt-auto'): #mt-auto pushes the button the the bottom of the card
                                    ui.button('Get Suggestion',on_click=lambda: suggestion_box.set_visibility(True))

                            #---------- Suggestion ----------
                            with ui.card().classes('flex-1'):
                                ui.label('Fix').classes('text-lg font-semibold')
                                with ui.column().classes('w-full') as suggestion_box:
                                    ui.label('Suggestions').classes('text-lg text-gray-500')
                                    selection = ui.radio(SUGGESTIONS,on_change=lambda e: fix_box.set_value(e.value))#e.value is the suggestion text that was picked. .set value is how you change an elements value from code
                                suggestion_box.set_visibility(False)
                                fix_box = ui.textarea(label='Fix applied').props('outlined clearable autogrow input-style="max-height: 8rem"').classes('w-full')
                                with ui.row().classes('w-full justify-end mt-auto'):
                                    ui.button('Save Fix',icon='check')
                        #---------- Problem History ----------
                        with ui.card().classes('w-full min-h-0'):
                            ui.label('Problem history').classes('text-lg font-semibold')
                            past = [p for p in c['problems'] if p['fix'] is not None]
                            with ui.list().props('separator').classes('w-full flex-1 min-h-0 overflow-y-auto'):  #this allows the problem history to scroll and not making the entire screen want to scroll when data starts to get longer than the screen
                                for p in past:  #each problem dict
                                    with ui.item():
                                        with ui.item_section():
                                            ui.item_label(f"{p['date']} · {p['title']}")
                                            ui.item_label(p['fix']).props('caption')
                            if not past:
                                ui.label('No past problems').classes('text-gray-500')  #if there is no past data: print that there is 'No past data'

                    #---------- Purchases Tab ----------
                    with ui.tab_panel(purchases_tab).classes('p-1'): #p-1 removes the padding down to 4px (tailwind's spacing scale is x4)
                        purchase_columns = [
                            {'name': 'date',    'label': 'Date',    'field': 'date', 'align': 'left'},
                            {'name': 'product', 'label': 'Product', 'field': 'product', 'align': 'left'},
                            {'name': 'brand',   'label': 'Brand',   'field': 'brand', 'align': 'left'},
                            {'name': 'qty',     'label': 'Qty',     'field': 'qty', 'align': 'center'},
                            {'name': 'size',    'label': 'Size',    'field': 'size', 'align': 'center'},
                        ]

                        #---------- Purchase Dialog ----------
                        with ui.dialog() as purchase_dialog, ui.card().classes('w-96'):
                            ui.label('Log Purchase').classes('w-full font-semibold text-lg')
                            product_select = ui.select([p['name'] for p in store.products],with_input=True, label='Product',
                                                       validation={'Pick a product': lambda v: bool(v)}).classes('w-full').props('outlined dense hide-bottom-space')  #p['name'] only pulls the name out of the dict of products the store sells
                            today_text = f"{store.TODAY:%b} {store.TODAY.day}, {store.TODAY.year}"
                            with ui.grid(columns=2).classes('w-full gap-3'):
                                purchase_date = ui.input(label='Date',value=today_text).props('outlined dense')
                                purchase_qty = ui.number(label='Qty', value=1, min=1, step=1).props('outlined dense')

                            #---------- save_purchase func ----------
                            def save_purchase():
                                if not product_select.validate():
                                    return
                                product = {p['name']: p for p in store.products}[product_select.value]  # look up brand + size by name
                                purchase = {'date': purchase_date.value, 'product': product['name'], 'brand': product['brand'],
                                            'qty': int(purchase_qty.value or 1), 'size': product['size']}
                                c['purchases'].insert(0, purchase)  # the data
                                purchase_table.rows.insert(0, purchase)  # the display (the table keeps its own copy)
                                purchase_table.update()
                                no_purchases.set_visibility(False)
                                product_select.set_value(None)  # reset the boxes for next time
                                purchase_date.set_value(today_text)
                                purchase_qty.set_value(1)
                                purchase_dialog.close()

                            with ui.row().classes('w-full justify-end'):
                                ui.button('Cancel', on_click=purchase_dialog.close).props('flat')
                                ui.button('Save', icon='check',on_click=save_purchase)
                      
                        #---------- Purchase History ----------
                        with ui.card().classes('w-full'):
                            with ui.row().classes('w-full items-center justify-between'):
                                ui.label('Purchases').classes('text-lg font-semibold')
                                ui.button('Log Purchase', icon='add', on_click=purchase_dialog.open)
                            purchase_table = ui.table(columns=purchase_columns, rows=c['purchases']).classes('w-full').props('flat bordered hide-no-data')
                            no_purchases = ui.label('No purchases yet').classes('text-gray-500')
                            no_purchases.set_visibility(not c['purchases'])
