from nicegui import ui
from layout import page_layout

@ui.page('/customers')
def customers():
    page_layout()
    ui.label('Customers')

    
