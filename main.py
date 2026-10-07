from nicegui import ui

@ui.page('/')
def home():
    ui.label('Pristine Pools')
    with ui.card():
        ui.label('Quick Actions')
        with ui.row():
            ui.button('New Water Test')
            ui.button('Log Problem')
            ui.button('Add Customer')
ui.run()