from nicegui import ui
from layout import page_layout
from datetime import date, timedelta
import tabular_store as store
import rules

SUGGESTIONS = [
    'Lower pH first: add about 1.5 lbs of pH reducer (sodium bisulfate), circulate 4 hours, retest. Target pH 7.4–7.6.',
    'Shock tonight with 3 lbs of cal-hypo (73%), then brush the walls and floor. Run the filter 24 hours straight.',
    'Add a dose of algaecide after shocking, then backwash the sand filter once the water clears. Retest in 2 days.',
]

@ui.page('/customer/tabular/{customer_id}')
def customer(customer_id: int, tab: str = ''):
    refresh_attention = page_layout()
    if customer_id not in store.customers:
        with ui.column().classes('w-full justify-center items-center min-h-[calc(100vh-10rem)]'):
            ui.icon('warning',color='orange',size='md')
            ui.label('Customer does not exist').classes('text-gray-500 text-lg')
        return  #handle if an employee tries to find an employee that does not exist. This simply displays that no customer exists and the return stops anything else from loading
    c = store.customers[customer_id]

    # ---------- Title row ----------
    with ui.column().classes('w-full max-w-screen-2xl mx-auto px-6 py-3 gap-4 print:p-0'):  # centered page column with padding (py-3 / gap-4 keep it short enough that the page doesn't scroll)
        with ui.row().classes('w-full items-center justify-between'):
            ui.label(c['name']).classes('text-2xl font-bold')
            
        with ui.row().classes('w-full no-wrap gap-6 items-stretch print:flex-col print:gap-3 md:min-h-[calc(100vh-11.5rem)] print:min-h-0'):  # items-stretch: both columns get the same height (the row's)
            with ui.column().classes('w-3/3 print:w-full print:flex-row'):  # the info cards set the row's height

                #---------- Edit Customer Dialog ----------
                def open_edit_customer_dialog():
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
                        ui.button(icon='edit',on_click=open_edit_customer_dialog).props('flat round dense size=sm').classes('-my-1').tooltip('Edit customer')  # size=sm + -my-1: the button doesn't make the title row taller
                    ui.label('Address').classes('text-xs text-gray-500')
                    ui.label(c['address'])
                    ui.label('Phone').classes('text-xs text-gray-500')
                    ui.label(c['phone'])
                    ui.label('Customer since').classes('text-xs text-gray-500')
                    ui.label(c['since'])

                #---------- Add Pool Dialog ----------
                def open_add_pool_dialog():
                    with ui.dialog() as add_pool_dialog, ui.card().classes('w-96'):
                        ui.label('Add Pool').classes('w-full text-lg font-semibold')
                        add_pool_dialog.open()  # open the dialog immediately after creating it

                #---------- Pools Card ----------
                with ui.card().classes('w-full gap-1 print:flex-1'):
                    with ui.row().classes('gap-0 items-center justify-between w-full'):
                        with ui.row().classes('w-full items-center justify-between pb-5'):
                            ui.label('Pools').classes('text-lg font-semibold')
                            ui.button('Add Pool',icon='add',on_click=open_add_pool_dialog)                                            
                        columns = [
                            {'name': 'pool', 'label': 'Pool',     'field': 'pool', 'align': 'left'},
                            {'name': 'address', 'label': 'Address', 'field': 'address', 'align': 'left'},
                            {'name': 'typesize', 'label': 'Type/Size', 'field': 'typesize', 'align': 'left'},
                            {'name': 'lasttest', 'label': 'Last Test', 'field': 'lasttest', 'align': 'left'},
                            {'name': 'problems', 'label': 'Problems', 'field': 'problems', 'align': 'left'},
                        ]

                        rows = []
                        for pool in c['bodies']:
                            rows.append({
                                'pool': pool['name'],
                                'address': pool['address'],
                                'typesize': f"{pool['type']} / {pool['size']}",
                                'lasttest': pool['tests'][0]['date'] if pool['tests'] else 'No tests',
                                'problems': len(pool['problems']),
                            })

                        table = ui.table(columns=columns, rows=rows).classes('w-full').on('row-click', lambda e: ui.navigate.to(f'/customer/{customer_id}'))  # e.args contains the row data