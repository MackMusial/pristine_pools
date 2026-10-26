from nicegui import ui
from layout import page_layout
import store
from datetime import timedelta

@ui.page('/settings')
def settings():
    page_layout()
    with ui.column().classes('w-full max-w-6xl mx-auto p-6 gap-6'):  # centered page column with padding
        with ui.row().classes('w-full items-center justify-between'):
            ui.label('Settings').classes('text-2xl font-bold')
            with ui.tabs().props('no-caps') as tabs:
                ui.tab('Products')
                ui.tab('Backup')
                ui.tab('Water-test ranges')
        with ui.tab_panels(tabs, value='Products').classes('w-full bg-transparent'):

            #---------- Products Tab ----------
            with ui.tab_panel('Products'):
                with ui.row().classes('w-full justify-end'):
                    ui.button('Add product',icon='add', on_click=lambda: add_product_dialog.open()).props('rounded')
                columns = [
                    {'name': 'name', 'label': 'Product', 'field': 'name', 'align': 'left'},
                    {'name': 'brand', 'label': 'Brand', 'field': 'brand', 'align': 'left'},
                    {'name': 'size', 'label': 'Size', 'field': 'size', 'align': 'left'},
                ]
                table = ui.table(rows=store.products, columns=columns, row_key='name').classes('w-full').props('flat bordered')
                with ui.dialog() as add_product_dialog, ui.card().classes('w-full'):
                    new_name = ui.input(label='Name',validation={'Required': lambda v: bool(v.strip())}).classes('w-full').props('outlined dense autofocus hide-bottom-space')
                    new_brand = ui.input(label='Brand').classes('w-full').props('outlined dense hide-bottom-space')
                    new_size = ui.input(label='Size').classes('w-full').props('outlined dense hide-bottom-space')
                    
                    #---------- save_product func -----------
                    def save_product():
                        if not new_name.validate():
                            return
                        product = {'name': new_name.value, 'brand': new_brand.value, 'size': new_size.value}
                        store.products.insert(0, product)  #insert the new product into the database
                        table.rows.insert(0, product)  #insert the new 
                        table.update()  #redraw the table 
                        new_name.set_value('')  #set all the variables back to blank
                        new_brand.set_value('')
                        new_size.set_value('')
                        add_product_dialog.close()  #close the dialog box after saving because otherwise it would say open

                    with ui.row().classes('w-full justify-end'):
                        ui.button('Cancel',on_click=add_product_dialog.close).props('flat')
                        ui.button('Save',on_click=save_product)

            #---------- Backup Tab ----------
            with ui.tab_panel('Backup'):
                with ui.card().classes('w-full'):
                    ui.label('Automatic Backups').classes('text-lg font-semibold text-gray-600')
                    last = store.TODAY - timedelta(days=1)
                    with ui.row().classes('items-center'):
                        ui.icon('check_circle', color='positive')
                        ui.label(f"Last backup: {last:%b} {last.day}, {last.year} at 2:00 AM")
                    ui.label('Backups run automatically every night to the USB drive.').classes('text-gray-600')
                    
                    #---------- Restore Database Dialog ----------
                    with ui.dialog() as restore_dialog, ui.card().classes('w-full'):
                        ui.label(f"Restore the {last:%b} {last.day} backup? Anything entered since then will be lost.")
                        with ui.row().classes('w-full justify-end'):
                            ui.button('Cancel',on_click=restore_dialog.close).props('flat')
                            ui.button('Restore',on_click=restore_dialog.close,color='negative')

                    with ui.row().classes('w-full justify-end'):
                        ui.button('Restore…',on_click=restore_dialog.open).props('flat no-caps')
                

            #---------- Water-test ranges Tab ----------
            with ui.tab_panel('Water-test ranges'):
                ui.label('Water-test Ranges go here')