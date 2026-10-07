from nicegui import ui

@ui.page('/')
def home():
    ui.label('Pristine Pools')
    with ui.card():
        ui.label('Quick Actions')
        ui.button('Customers Page',on_click=lambda: ui.navigate.to('/customers'))
        with ui.row():
            ui.button('New Water Test')
            ui.button('Log Problem')
            ui.button('Add Customer')
@ui.page('/customers')
def customers():
    ui.label('Customers')
    ui.button('Back to home', on_click=lambda: ui.navigate.to('/'))


ui.run()