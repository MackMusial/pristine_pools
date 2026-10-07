from nicegui import ui
from layout import page_layout

@ui.page('/')
def home():
    page_layout()
    with ui.card():
        ui.label('Quick Actions')
        with ui.row():
            ui.button('New Water Test')
            ui.button('Log Problem')
            ui.button('Add Customer')