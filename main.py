from nicegui import ui

@ui.page('/')
def home():
    ui.label('Pristine Pools')
    with ui.column():
        ui.button('New Water Test')
        ui.button('Log Problem')
        ui.button('Add Customer')
    ui.button('Click me!', on_click=lambda: ui.notify("Welcome to Pristine Pools!"))
ui.run()