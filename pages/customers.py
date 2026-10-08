from nicegui import ui
from layout import page_layout

@ui.page('/customers')
def customers():
    page_layout()
    with ui.column().classes('w-full max-w-6xl mx-auto p-6 gap-6'):#centers the content and adds padding and gap between elements
        with ui.row().classes('w-full items-center justify-between'):
            ui.label('Customers').classes('text-2xl font-bold')
            with ui.row():
                ui.button('Add Customer')
                ui.icon='person_add'

    
