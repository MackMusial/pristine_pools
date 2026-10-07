from nicegui import ui
from layout import page_layout

@ui.page('/')
def home():
    page_layout()
    ui.button('Customers Page',on_click=lambda: ui.navigate.to('/customers'))
    with ui.card():
        ui.label('Quick Actions')
        with ui.row():
            ui.button('New Water Test')
            ui.button('Log Problem')
            ui.button('Add Customer')


@ui.page('/customers')
def customers():
    page_layout()
    ui.label('Customers')
    ui.button('Back to home',on_click=lambda: ui.navigate.to('/'))


ui.run()