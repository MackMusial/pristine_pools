from nicegui import ui


def header():
    with ui.header():
        ui.label('Pristine Pools')

@ui.page('/')
def home():
    header()
    ui.button('Customers Page',on_click=lambda: ui.navigate.to('/customers'))
    with ui.card():
        ui.label('Quick Actions')
        with ui.row():
            ui.button('New Water Test')
            ui.button('Log Problem')
            ui.button('Add Customer')


@ui.page('/customers')
def customers():
    header()
    ui.label('Customers')
    ui.button('Back to home',on_click=lambda: ui.navigate.to('/'))

ui.run(show=False)