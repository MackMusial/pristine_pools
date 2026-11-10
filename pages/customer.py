from fastapi.responses import RedirectResponse
from nicegui import ui
from layout import page_layout
from datetime import date, timedelta, datetime
import store
import rules

SUGGESTIONS = [
    'Lower pH first: add about 1.5 lbs of pH reducer (sodium bisulfate), circulate 4 hours, retest. Target pH 7.4–7.6.',
    'Shock tonight with 3 lbs of cal-hypo (73%), then brush the walls and floor. Run the filter 24 hours straight.',
    'Add a dose of algaecide after shocking, then backwash the sand filter once the water clears. Retest in 2 days.',
]

@ui.page('/')
def start():
    cid = store.last_customer_id if store.last_customer_id is not None else min(store.customers)  #select the last customer viewed. else select the first customer in the datebase
    return RedirectResponse(f'/customer/{cid}')
@ui.page('/customer/{customer_id}')
def customer(customer_id: int, tab: str = ''):
    refresh_attention = page_layout()
    if customer_id not in store.customers:
        with ui.column().classes('w-full justify-center items-center min-h-[calc(100vh-10rem)]'):
            ui.icon('warning',color='orange',size='md')
            ui.label('Customer does not exist').classes('text-gray-500 text-lg')
        return  #handle if an employee tries to find an employee that does not exist. This simply displays that no customer exists and the return stops anything else from loading
    c = store.customers[customer_id]
    store.last_customer_id = customer_id

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
                refresh_attention()
                retest_chip.refresh()  #refresh the retest chip to show the new date and color
                dialog.close()  #close the dialog box 
            with ui.row().classes('w-full justify-end'):
                ui.button('Skip', on_click=dialog.close).props('flat')
                ui.button('Schedule',on_click=save)  #save with no () lets save run when the button is clicked not when the page is being built. 
        dialog.open()

    def reschedule():
        schedule_retest(7, c['retest']['reason'])

    def clear_retest():
        c['retest'] = None
        refresh_attention()
        retest_chip.refresh()

    def confirm_clear():
        with ui.dialog() as dialog, ui.card():
            ui.label('Cancel this retest?').classes('text-lg font-semibold')
            def confirmed():
                clear_retest()
                dialog.close()
            with ui.row().classes('w-full justify-end'):
                ui.button('Keep', on_click=dialog.close).props('flat')
                ui.button('Cancel retest', color='red-9', on_click=confirmed).mark('confirm-clear')
        dialog.open()

    #---------- Retest Chip Func ----------
    @ui.refreshable
    def retest_chip():
        '''Displays a chip on the customer page that shows the retest date if one is scheduled. 
        
        If the retest is overdue, the chip is red.'''
        r = c['retest']
        if r is None:
            return
        with ui.row().classes('group items-center gap-1'):
            if r['due'] < store.TODAY:
                ui.chip(f"Retest overdue: {r['due']:%b} {r['due'].day}", icon='event', color='red-9', text_color='white', on_click=reschedule).classes('print:hidden').mark('retest-chip')
            else:
                ui.chip(f"Retest due {r['due']:%b} {r['due'].day}",icon='event', color='grey-3', text_color='black', on_click=reschedule).classes('print:hidden').mark('retest-chip')
            ui.button(icon='close', on_click=confirm_clear).mark('clear-retest').props('flat round dense size=sm aria-label="Cancel retest"').classes('print:hidden opacity-0 group-hover:opacity-100 focus-visible:opacity-100 transition-opacity').tooltip('Cancel retest')

    # ---------- Title row ----------
    with ui.column().classes('w-full max-w-screen-2xl mx-auto px-6 py-3 gap-4 print:p-0'):  # centered page column with padding (py-3 / gap-4 keep it short enough that the page doesn't scroll)
        with ui.row().classes('w-full items-center justify-between'):
            with ui.row().classes('items-center gap-3'):
                ui.label(c['name']).classes('text-2xl font-bold')
                retest_chip()
            with ui.tabs().props('inline-label dense no-caps').classes('print:hidden') as tabs:
                test_tab = ui.tab('Water Tests', icon='science')
                problems_tab = ui.tab('Problems', icon='report_problem')
                purchases_tab = ui.tab('Purchases',icon='shopping_cart')
        with ui.row().classes('w-full no-wrap gap-6 items-stretch print:flex-col print:gap-3 md:min-h-[calc(100vh-11.5rem)] print:min-h-0'):  # items-stretch: both columns get the same height (the row's)
            with ui.column().classes('w-1/3 print:w-full print:flex-row'):  # the info cards set the row's height

                def open_edit_customer_dialog():
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

                        edit_cust_dialog.on('hide', edit_cust_dialog.delete)  # remove the dialog from the page once it closes
                        edit_cust_dialog.open()

                #---------- Contact Card ----------
                with ui.card().classes('w-full gap-1 print:flex-1'):
                    with ui.row().classes('gap-0 items-center justify-between w-full'):
                        ui.label('Contact').classes('text-lg font-semibold')
                        ui.button(icon='edit',on_click=open_edit_customer_dialog).props('flat round dense size=sm').classes('-my-1 print:hidden').tooltip('Edit customer')  # size=sm + -my-1: the button doesn't make the title row taller
                    ui.label('Address').classes('text-xs text-gray-500')
                    ui.label(c['address'])
                    ui.label('Phone').classes('text-xs text-gray-500')
                    ui.label(c['phone'])
                    ui.label('Customer since').classes('text-xs text-gray-500')
                    ui.label(c['since'])

                #---------- Add Pool Dialog ----------
                #TODO: Merge Add and Edit into one form (blank for Add, filled for Edit) so a new field is only added once. Volume stays editable
                def open_add_pool():  
                    with ui.dialog() as add_pool_dialog, ui.card().classes('p-0 gap-0 no-wrap').style('width: 640px; max-width: 95vw; max-height: 90vh'):
                        with ui.column().classes('w-full px-5 pt-5 pb-3 gap-3'):
                            ui.label('New Pool').classes('font-semibold text-lg w-full')
                            shape = ui.toggle(['Round', 'Oval', 'Rectangle'], value='Round')

                        with ui.column().classes('w-full px-5 gap-3 overflow-y-auto').style('flex: 1 1 auto; min-height: 0'):
                            ui.label('Pool').classes('text-xs font-medium text-grey-7 uppercase tracking-wide')
                            with ui.row().classes('w-full gap-3 no-wrap'):
                                name = ui.input(label='Pool Name').props('outlined dense hide-bottom-space').classes('w-full').style('flex: 1')
                                address = ui.input(label='Pool Address').props('outlined dense hide-bottom-space').classes('w-full').style('flex: 2')
                            with ui.row().classes('w-full gap-3 no-wrap'):
                                pool_type = ui.select(label='Type', options=['Above-Ground', 'In-Ground']).props('outlined dense hide-bottom-space').classes('w-full')
                                floor = ui.select(label='Floor Material', options=['Sand']).props('outlined dense hide-bottom-space').classes('w-full')
                                wall = ui.select(label='Wall Type', options=['Hard Sided']).props('outlined dense hide-bottom-space').classes('w-full')

                            ui.label('Dimensions').classes('text-xs font-medium text-grey-7 uppercase tracking-wide mt-2')
                            with ui.row().classes('w-full gap-3 no-wrap'):
                                length = ui.number(label='Length (ft)', min=0).props('outlined dense hide-bottom-space').classes('w-full')
                                width = ui.number(label='Width (ft)', min=0).props('outlined dense hide-bottom-space').classes('w-full')
                                wall_height = ui.number(label='Wall Height (in)', min=0).props('outlined dense hide-bottom-space').classes('w-full')
                            with ui.row().classes('w-full gap-3 no-wrap'):
                                depth = ui.number(label='Water Depth (in)', min=0).props('outlined dense hide-bottom-space').classes('w-full').style('flex: 1')
                                volume = ui.number(label='Volume (gal)', min=0).props('outlined dense hide-bottom-space readonly').classes('w-full').style('flex: 2')

                            ui.label('Manufacturer').classes('text-xs font-medium text-grey-7 uppercase tracking-wide mt-2')
                            with ui.row().classes('w-full gap-3 no-wrap'):
                                manufacturer = ui.input(label='Manufacturer').props('outlined dense hide-bottom-space').classes('w-full')
                                model_no = ui.input(label='Model No.').props('outlined dense hide-bottom-space').classes('w-full')
                            with ui.row().classes('w-full gap-3 no-wrap'):
                                serial_no = ui.input(label='Serial No.').props('outlined dense hide-bottom-space').classes('w-full')
                                warranty_end = ui.input(label='Warranty End').props('outlined dense hide-bottom-space').classes('w-full')

                            ui.label('Liner').classes('text-xs font-medium text-grey-7 uppercase tracking-wide mt-2')
                            with ui.row().classes('w-full gap-3 no-wrap'):
                                liner_manufacturer = ui.input(label='Liner Manufacturer').props('outlined dense hide-bottom-space').classes('w-full')
                                liner_model_no = ui.input(label='Liner Model No.').props('outlined dense hide-bottom-space').classes('w-full')
                            with ui.row().classes('w-full gap-3 no-wrap'):
                                liner_serial_no = ui.input(label='Liner Serial No.').props('outlined dense hide-bottom-space').classes('w-full')
                                liner_size = ui.input(label='Liner Size').props('outlined dense hide-bottom-space').classes('w-full')

                            ui.label('Filter').classes('text-xs font-medium text-grey-7 uppercase tracking-wide mt-2')
                            with ui.row().classes('w-full gap-3 no-wrap'):
                                filter_brand = ui.input(label='Filter Brand').props('outlined dense hide-bottom-space').classes('w-full')
                                filter_type = ui.select(label='Filter Type', options=['Cartridge', 'Sand', 'DE']).props('outlined dense hide-bottom-space').classes('w-full')
                                filter_model_no = ui.input(label='Filter Model No.').props('outlined dense hide-bottom-space').classes('w-full')
                            with ui.row().classes('w-full gap-3 no-wrap'):
                                cartridge_no = ui.input(label='Replacement Cartridge No.').props('outlined dense hide-bottom-space').classes('w-full')
                                flow_rate = ui.number(label='Flow Rate (GPM)', min=0).props('outlined dense hide-bottom-space').classes('w-full')
                                filter_size = ui.number(label='Filter Size (sq ft)', min=0).props('outlined dense hide-bottom-space').classes('w-full')

                            ui.label('Chlorinator').classes('text-xs font-medium text-grey-7 uppercase tracking-wide mt-2')
                            with ui.row().classes('w-full gap-3 items-center'):
                                ui.label('Automatic chlorinator?').classes('text-sm')
                                auto_chlorinator = ui.radio(['Yes', 'No']).props('inline dense')
                            with ui.row().classes('w-full gap-3 no-wrap'):
                                chlorinator_brand = ui.input(label='Chlorinator Brand').props('outlined dense hide-bottom-space').classes('w-full')
                                chlorinator_model_no = ui.input(label='Chlorinator Model No.').props('outlined dense hide-bottom-space').classes('w-full')

                            ui.label('Installation').classes('text-xs font-medium text-grey-7 uppercase tracking-wide mt-2')
                            with ui.row().classes('w-full gap-3 no-wrap'):
                                installer_name = ui.input(label='Installer Name').props('outlined dense hide-bottom-space').classes('w-full').style('flex: 1')
                                installer_address = ui.input(label='Installer Address').props('outlined dense hide-bottom-space').classes('w-full').style('flex: 2')
                            with ui.row().classes('w-full gap-3 no-wrap'):
                                installer_email = ui.input(label='Installer Email').props('outlined dense hide-bottom-space').classes('w-full')
                                installer_phone = ui.input(label='Installer Phone').props('outlined dense hide-bottom-space').classes('w-full')
                            with ui.row().classes('w-full gap-3 no-wrap pb-2'):
                                purchase_date = ui.input(label='Purchase Date').props('outlined dense hide-bottom-space').classes('w-full')
                                install_date = ui.input(label='Install Date').props('outlined dense hide-bottom-space').classes('w-full')

                        ui.separator()
                        with ui.row().classes('w-full justify-end px-5 py-3'):
                            ui.button('Cancel', on_click=add_pool_dialog.close).props('flat')
                             #TODO: Save isn't connected yet. Wait for the shared form so it isn't built twice
                            ui.button('Save', icon='check')
                    add_pool_dialog.on('hide', add_pool_dialog.delete)  # remove the dialog from the page once it closes
                    add_pool_dialog.open()

                #---------- Edit Pool Dialog ----------
                def open_edit_pool(i):    
                    b = c['bodies'][i]  #i represents the individual pool / hottub the customer has. i will allow us to display more than one pool without hardcoding 
                    with ui.dialog() as edit_pool_dialog, ui.card().classes('p-0 gap-0 no-wrap').style('width: 640px; max-width: 95vw; max-height: 90vh'):
                        with ui.column().classes('w-full px-5 pt-5 pb-3 gap-3'):
                            ui.label(f"Edit {b['type']}").classes('font-semibold text-lg w-full')
                            if b['type'] == 'Pool':  # pools: size comes from numbers so gallons can be calculated
                                shape = ui.toggle(['Round', 'Oval', 'Rectangle'], value=b['shape']).mark('pool-shape')  #TODO: 

                        with ui.column().classes('w-full px-5 gap-3 overflow-y-auto').style('flex: 1 1 auto; min-height: 0'):
                            ui.label('Pool').classes('text-xs font-medium text-grey-7 uppercase tracking-wide')
                            with ui.row().classes('w-full gap-3 no-wrap'):
                                name = ui.input(value=b['name'],label='Pool Name').props('outlined dense hide-bottom-space').classes('w-full').style('flex: 1')
                                address = ui.input(value=b['address'],label='Pool Address').props('outlined dense hide-bottom-space').classes('w-full').style('flex: 2')
                            with ui.row().classes('w-full gap-3 no-wrap'):
                                pool_type = ui.select(value=b['pool_type'],label='Type', options=['Above-Ground', 'In-Ground']).props('outlined dense hide-bottom-space').classes('w-full')
                                floor = ui.select(value=b['floor'],label='Floor Material', options=store.floor_options).props('outlined dense hide-bottom-space').classes('w-full')
                                wall_type = ui.select(value=b['wall_type'],label='Wall Type', options=store.wall_type_options).props('outlined dense hide-bottom-space').classes('w-full')

                            ui.label('Dimensions').classes('text-xs font-medium text-grey-7 uppercase tracking-wide mt-2')
                            with ui.row().classes('w-full gap-3 no-wrap'):
                                length = ui.number(value=b['length'], label='Length (ft)', min=0, validation={'Required': lambda v: bool(v)}).props('outlined dense hide-bottom-space').classes('w-full')
                                width = ui.number(value=b['width'],label='Width (ft)', min=0, validation={'Required': lambda v: bool(v)}).props('outlined dense hide-bottom-space').classes('w-full')
                                wall_height = ui.number(value=b['wall'],label='Wall Height (in)', min=0, validation={'Required': lambda v: bool(v)}).props('outlined dense hide-bottom-space').classes('w-full')
                            with ui.row().classes('w-full gap-3 no-wrap'):
                                depth = ui.number(value=b['depth'],label='Water Depth (in)', min=0).props('outlined dense hide-bottom-space').classes('w-full').style('flex: 1')
                                volume = ui.number(value=b['gallons'],label='Volume (gal)', min=0, validation={'Required': lambda v: bool(v)}).props('outlined dense hide-bottom-space').classes('w-full').style('flex: 2')


                            ui.label('Manufacturer').classes('text-xs font-medium text-grey-7 uppercase tracking-wide mt-2')
                            with ui.row().classes('w-full gap-3 no-wrap'):
                                manufacturer = ui.input(value=b['manufacturer'],label='Manufacturer').props('outlined dense hide-bottom-space').classes('w-full')
                                model_no = ui.input(value=b['model_no'],label='Model No.').props('outlined dense hide-bottom-space').classes('w-full')
                            with ui.row().classes('w-full gap-3 no-wrap'):
                                serial_no = ui.input(value=b['serial_no'],label='Serial No.').props('outlined dense hide-bottom-space').classes('w-full')
                                warranty_end = ui.input(value=b['warranty_end'],label='Warranty End').props('outlined dense hide-bottom-space').classes('w-full')

                            ui.label('Liner').classes('text-xs font-medium text-grey-7 uppercase tracking-wide mt-2')
                            with ui.row().classes('w-full gap-3 no-wrap'):
                                liner_manufacturer = ui.input(value=b['liner_manufacturer'],label='Liner Manufacturer').props('outlined dense hide-bottom-space').classes('w-full')
                                liner_model_no = ui.input(value=b['liner_model_no'],label='Liner Model No.').props('outlined dense hide-bottom-space').classes('w-full')
                            with ui.row().classes('w-full gap-3 no-wrap'):
                                liner_serial_no = ui.input(value=b['liner_serial_no'],label='Liner Serial No.').props('outlined dense hide-bottom-space').classes('w-full')
                                liner_size = ui.input(value=b['liner_size'],label='Liner Size').props('outlined dense hide-bottom-space').classes('w-full')

                            ui.label('Filter').classes('text-xs font-medium text-grey-7 uppercase tracking-wide mt-2')
                            with ui.row().classes('w-full gap-3 no-wrap'):
                                filter_brand = ui.input(value=b['filter_brand'],label='Filter Brand').props('outlined dense hide-bottom-space').classes('w-full')
                                filter_type = ui.select(value=b['filter_type'],label='Filter Type', options=['Cartridge', 'Sand', 'DE']).props('outlined dense hide-bottom-space').classes('w-full')
                                filter_model_no = ui.input(value=b['filter_model_no'],label='Filter Model No.').props('outlined dense hide-bottom-space').classes('w-full')
                            with ui.row().classes('w-full gap-3 no-wrap'):
                                cartridge_no = ui.input(value=b['cartridge_no'],label='Replacement Cartridge No.').props('outlined dense hide-bottom-space').classes('w-full')
                                flow_rate = ui.number(value=b['flow_rate'],label='Flow Rate (GPM)', min=0).props('outlined dense hide-bottom-space').classes('w-full')
                                filter_size = ui.number(value=b['filter_size'],label='Filter Size (sq ft)', min=0).props('outlined dense hide-bottom-space').classes('w-full')

                            ui.label('Chlorinator').classes('text-xs font-medium text-grey-7 uppercase tracking-wide mt-2')
                            with ui.row().classes('w-full gap-3 items-center'):
                                ui.label('Automatic chlorinator?').classes('text-sm')
                                auto_chlorinator = ui.radio(['Yes', 'No'],value=b['auto_chlorinator']).props('inline dense')
                            with ui.row().classes('w-full gap-3 no-wrap'):
                                chlorinator_brand = ui.input(value=b['chlorinator_brand'],label='Chlorinator Brand').props('outlined dense hide-bottom-space').classes('w-full')
                                chlorinator_model_no = ui.input(value=b['chlorinator_model_no'],label='Chlorinator Model No.').props('outlined dense hide-bottom-space').classes('w-full')

                            ui.label('Installation').classes('text-xs font-medium text-grey-7 uppercase tracking-wide mt-2')
                            with ui.row().classes('w-full gap-3 no-wrap'):
                                installer_name = ui.input(value=b['installer_name'],label='Installer Name').props('outlined dense hide-bottom-space').classes('w-full').style('flex: 1')
                                installer_address = ui.input(value=b['installer_address'],label='Installer Address').props('outlined dense hide-bottom-space').classes('w-full').style('flex: 2')
                            with ui.row().classes('w-full gap-3 no-wrap'):
                                installer_email = ui.input(value=b['installer_email'],label='Installer Email').props('outlined dense hide-bottom-space').classes('w-full')
                                installer_phone = ui.input(value=b['installer_phone'],label='Installer Phone').props('outlined dense hide-bottom-space').classes('w-full')
                            with ui.row().classes('w-full gap-3 no-wrap pb-2'):
                                purchase_date = ui.input(value=b['purchase_date'],label='Purchase Date').props('outlined dense hide-bottom-space').classes('w-full')
                                install_date = ui.input(value=b['install_date'],label='Install Date').props('outlined dense hide-bottom-space').classes('w-full')

                        def recalc_volume():  # runs whenever shape, length, width, or wall changes
                            factor = 7.5 if shape.value == 'Rectangle' else 5.9
                            w = length.value if shape.value == 'Round' else width.value  # round pool: width = diameter
                            if length.value and w and wall_height.value:  # skip while a box is blank
                                volume.set_value(int(round(length.value * w * (wall_height.value / 12) * factor, -2)))  # ft × ft × depth in ft × 5.9, to the nearest 100
                        
                        for box in [shape, length, width, wall_height]:
                            box.on_value_change(recalc_volume)  # after volume exists, so it's never called too early ... This is what calls the funcation that recalcs the volume
                                
                        #---------- Edit Pool Func ----------
                        def edit_pool():
                            boxes = [length, wall_height, volume] + ([width] if shape.value != 'Round' else [])
                            if not all([box.validate() for box in boxes]):
                                return
                            
                            b['gallons'] = int(volume.value)  # whatever is in the box: calculated or typed over
                            if b['type'] == 'Pool':
                                fields = {
                                    'name': name,
                                    'address': address, 
                                    'pool_type': pool_type,
                                    'wall_type': wall_type,
                                    'depth': depth,
                                    'manufacturer': manufacturer,
                                    'model_no': model_no,
                                    'serial_no': serial_no,
                                    'warranty_end': warranty_end,
                                    'liner_manufacturer': liner_manufacturer,
                                    'liner_model_no': liner_model_no,
                                    'liner_serial_no': liner_serial_no,
                                    'liner_size': liner_size,
                                    'filter_brand': filter_brand,
                                    'filter_type': filter_type,
                                    'filter_model_no': filter_model_no,
                                    'cartridge_no': cartridge_no,
                                    'flow_rate': flow_rate,
                                    'filter_size': filter_size,
                                    'auto_chlorinator': auto_chlorinator,
                                    'chlorinator_brand': chlorinator_brand,
                                    'chlorinator_model_no': chlorinator_model_no,
                                    'installer_name': installer_name,
                                    'installer_address': installer_address,
                                    'installer_email': installer_email,
                                    'installer_phone': installer_phone,
                                    'purchase_date': purchase_date,
                                    'install_date': install_date,
                                }
                                for key, box in fields.items():
                                    b[key] = box.value

                                b['wall_liner'] = f"{wall_type.value} · {liner_manufacturer.value} liner"  #TODO: Remove wall_liner, chlorinator and these rebuilt strings once the card reads the new fields. Saving drops detail like '150 lbs sand'. Hot tubs still use filter + installed

                                b['filter'] = f"{filter_brand.value} {filter_type.value} filter"
                                b['chlorinator'] = chlorinator_brand.value or 'None'
                                b['installed'] = f"{install_date.value} · {installer_name.value}"
                                b['floor'] = floor.value
                                b['shape'] = shape.value
                                b['length'] = length.value
                                b['width'] = length.value if shape.value == 'Round' else width.value  # round pool: width = diameter
                                b['wall'] = wall_height.value
                                if shape.value == 'Round':
                                    b['size'] = f"{b['length']:g} ft round · {b['wall']:g} in wall"  # :g drops the .0 from ui.number values
                                elif shape.value == 'Rectangle':
                                    b['size'] = f"{b['width']:g} x {b['length']:g} ft rectangle · {b['wall']:g} in wall"
                                else:
                                    b['size'] = f"{b['width']:g} x {b['length']:g} ft oval · {b['wall']:g} in wall"
                            edit_pool_dialog.close()  #Close the dialog after everything is properly saved
                            ui.navigate.reload()  #TODO: Add a @ui.refreshable to only refresh what is needed. .reload reloads the entire screen which is not needed
                    
                        ui.separator()      
                        with ui.row().classes('w-full justify-end px-5 py-3'):
                            ui.button('Cancel',on_click=edit_pool_dialog.close).props('flat')
                            ui.button('Save',icon='check', on_click=edit_pool).mark('save-pool')
                    edit_pool_dialog.on('hide', edit_pool_dialog.delete)
                    edit_pool_dialog.open()
                    
                    
                #TODO: Show the most useful fields on the card (filter type + replacement cartridge no., warranty end). Ask Kara what staff look up. Serials and installer contact stay in the dialog

                #---------- Pool Card ----------
                with ui.card().classes('w-full gap-1 print:flex-1'):
                    with ui.row().classes('w-full items-center justify-between'):
                        if len(c['bodies']) > 1:  #if there is more than one pool on file, display the dropdown
                            search = ui.select(store.search_pools(), value=c['bodies'][0]['type']).props('dense').classes('w-96 text-lg font-semibold')
                            #TODO: Implement the logic to switch between pools based on the dropdown selection
                        else: 
                            ui.label(c['bodies'][0]['type'] if c['bodies'] else 'Pool').classes('text-lg font-semibold').mark('pool-title')   
                        with ui.row().classes('gap-0'):
                            if c['bodies'] and c['bodies'][0]['type'] == 'Pool': #TODO and c['bodies'][0]['type'] == 'Pool' this is being used so edit button is removed for hottubs because that code is not written
                                ui.button(icon='edit',on_click=lambda: open_edit_pool(0)).mark('edit-pool').props('flat round dense size=sm').classes('-my-1 print:hidden').tooltip(f"Edit {c['bodies'][0]['type']}")  #TODO Unhardcode 0 when adding funcationality for multiple pools. onclick is what calls the dialogbox to appear
                            ui.button(icon='add', on_click=open_add_pool).props('flat round dense size=sm').classes('-my-1').tooltip('Add pool or hottub').classes('print:hidden')

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
            def test_date(t): 
                '''Returns a datetime.date object from the test's date string'''
                return datetime.strptime(t['date'], '%b %d, %Y').date()  #convert the test's date string into a date object so it can be sorted 

            def table_row(t):
                return{**t, **rules.test_colors(t), **rules.reading_arrows(t)}
            
            with ui.column().classes('flex-1 md:[contain:size] md:overflow-y-auto gap-0 print:[contain:none]'):  # contain:size: this column's content doesn't make the row taller, so it matches the info cards and scrolls inside
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
                                table.rows.insert(0,table_row(test))      
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
                                retest_chip.refresh()  #refresh the retest chip to show the new retest date if one was scheduled

                            with ui.grid(columns=2).classes('w-full gap-3'):
                                for key, label in [('fc', 'FC'), ('tc', 'TC'), ('ph', 'pH'), ('ta', 'Alk'), ('ch', 'Hardness'), ('cya', 'CYA'), ('phos', 'Phosphates'),]:
                                    inputs[key] = ui.number(label=label, min=0, step=0.1).props('outlined dense').on('keydown.enter', save_test)
                                    inputs['fc'].props('autofocus')
                            with ui.row().classes('w-full justify-end'):
                                ui.button('Cancel', on_click=test_dialog.close).props('flat')
                                ui.button('Save', icon='check',on_click=save_test)  #don't put () because that will cause the func to fire as initalization time. we only want the func to fire up when the button is clicked

                        no_tests_msg = {30: 'No tests in the last 30 days',
                                        90: 'No tests in the last 90 days',
                                        180: 'No tests in the last 180 days',
                                        365: 'No tests in the last year',
                                        0: 'No tests yet'} 

                        def filter_tests(e):
                            days = e.value
                            cutoff = store.TODAY - timedelta(days=days)
                            table.rows = [table_row(t) for t in c['tests']
                                          if days == 0 or test_date(t) >= cutoff]  #if days == 0, show all tests. otherwise only show tests that are newer than the cutoff  
                            table.props(f'no-data-label="{no_tests_msg[days]}"')

                        #---------- Latest Test Card ----------
                        with ui.card().classes('w-full'):  #latest test card
                            with ui.row().classes('w-full items-center justify-between'):
                                latest = ui.label(f"Latest test · {c['tests'][0]['date']}" if c['tests'] else 'No tests yet').classes('text-lg font-semibold')
                                with ui.row().classes('items-center gap-2 print:hidden'):
                                    ui.button(icon='print',on_click=lambda: ui.run_javascript('window.print()')).props('flat round')  #Print button
                                    ui.button('New Test',icon='add',on_click=test_dialog.open)
                                    ui.select({30: '30 days', 90: '90 days', 180: '180 days', 365: '1 year', 0: 'All'}, value=0, on_change=filter_tests).props('outlined dense rounded').classes('w-32')
                      
                        # ---------- Legend ----------
                        with ui.row().classes('items-center gap-2 text-sm text-gray-8'):
                            ui.badge('In range',color='green-9',text_color='white')
                            ui.badge('Borderline', color='amber-7', text_color='black')
                            ui.badge('Out of range', color='red-9', text_color='white')
                            ui.icon('arrow_upward', size='14px')
                            ui.label('high')
                            ui.icon('arrow_downward', size='14px')
                            ui.label('low')

                        # ---------- Table ----------
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
                        rows = [table_row(t) for t in c['tests']] #** ** merges two dicts into a new one. 
                        table = ui.table(columns=columns, rows=rows).classes('w-full').props('no-data-label="No tests yet"')
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
                        # <span v-else>          -> no color key = date or blank reading
                        # phase 2: rules.py adds the _color keys by comparing each reading to the ranges in Settings
                        table.add_slot('body-cell', r'''
                            <q-td :props="props">
                                <q-badge v-if="['orange', 'red'].includes(props.row[props.col.field + '_color'])"
                                        :color="props.row[props.col.field + '_color'] === 'red' ? 'red-9' : 'amber-7'"
                                        :text-color="props.row[props.col.field + '_color'] === 'red' ? 'white' : 'black'">
                                    {{ props.value }}
                                    <q-icon v-if="props.row[props.col.field + '_arrow']"
                                            :name="props.row[props.col.field + '_arrow'] === '↑' ? 'arrow_upward' : 'arrow_downward'"
                                            size="14px" class="q-ml-xs" />
                                </q-badge>
                                <q-badge  v-else-if="props.row[props.col.field + '_color'] === 'green'" 
                                color="green-9" text-color="white">{{ props.value }}</q-badge>
                                <span v-else>{{ props.value }}</span>
                            </q-td>
                        ''')

                        #---------- Water Test Chart Dialog ----------
                        COLORS = {'green': '#2e9e44', 'orange': '#f59e0b', 'red': '#d32f2f'} 

                        def show_chart(test):
                            labels = {col['field']: col['label'] for col in columns}
                            with ui.dialog() as chart_dialog, ui.card().classes('w-[36rem] max-w-[95vw] single-page-print'):
                                ui.label(f"Water test · {test['date']}").classes('text-lg font-semibold')
                                for field, (red_below, green_from, green_to, red_above) in rules.BANDS.items():
                                    value = test.get(field)
                                    if value is None:  #reading wasn't taken
                                        continue
                                    pad = (red_above - red_below) * 0.25  #show a bit of red past each red line
                                    low = max(0, red_below - pad)
                                    high = red_above + pad
                                    def pct(x):
                                        return max(0, min(100, (x - low) / (high - low) * 100))  #position on the line as a %, clamped to the edges
                                    flag = COLORS[rules.color_for(field, value)]  #flag matches the badge color

                                    with ui.row().classes('w-full items-center no-wrap gap-4'):
                                        ui.label(labels[field]).classes('w-24 font-medium')
                                        with ui.element('div').classes('relative flex-1 mx-4').style('height: 52px'):
                                            ui.element('div').classes('absolute left-0 right-0').style(f'top: 26px; height: 4px; background: {COLORS["red"]}')  #red = the whole line
                                            ui.element('div').classes('absolute').style(  #green = the good range
                                                f'top: 26px; height: 4px; background: {COLORS["green"]}; left: {pct(green_from)}%; width: {pct(green_to) - pct(green_from)}%')
                                            for edge in (green_from, green_to):  #numbers under each end of the green
                                                ui.label(f'{edge:g}').classes('absolute text-xs').style(f'top: 31px; left: {pct(edge)}%; transform: translateX(-50%)')
                                            with ui.column().classes('absolute items-center gap-0').style(f'top: 0; left: {pct(value)}%; transform: translateX(-50%)'):  #the flag
                                                ui.label(f'{value:g}').classes('text-white font-bold text-xs').style(f'background: {flag}; padding: 1px 8px; border-radius: 3px; line-height: 18px')
                                                ui.element('div').style(  #little triangle under the flag pointing at the line
                                                    f'width: 0; height: 0; border-left: 6px solid transparent; border-right: 6px solid transparent; border-top: 6px solid {flag}')
                                with ui.row().classes('w-full justify-end mt-2'):
                                    ui.button('Close', on_click=chart_dialog.close).props('flat').classes('print:hidden')
                                    ui.button('Print', icon='print',on_click=lambda: ui.run_javascript('window.print()')).classes('print:hidden')  #Print button

                            chart_dialog.on('hide', chart_dialog.delete)  #remove the dialog from the page once it closes
                            chart_dialog.open()

                        table.on('rowClick', lambda e: show_chart(e.args[1])) 
                        table.classes('cursor-pointer')
                        
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
