from nicegui import ui
from layout import page_layout
import store

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
        with ui.tab_panels(tabs, value='Products').classes('w-full'):

            #---------- Products Tab ----------
            with ui.tab_panel('Products'):
                columns = [
                    {'name': 'name', 'label': 'Product', 'field': 'name', 'align': 'left'},
                    {'name': 'brand', 'label': 'Brand', 'field': 'brand', 'align': 'left'},
                    {'name': 'size', 'label': 'Size', 'field': 'size', 'align': 'left'},
                ]
                table = ui.table(rows=store.products, columns=columns, row_key='name').classes('w-full').props('flat bordered')

            #---------- Backup Tab ----------
            with ui.tab_panel('Backup'):
                ui.label('Backups go here')

            #---------- Water-test ranges Tab ----------
            with ui.tab_panel('Water-test ranges'):
                ui.label('Water-test Ranges go here')