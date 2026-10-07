from nicegui import ui

def page_layout():
    with ui.header():
        ui.label('Pristine Pools')
        ui.input(placeholder='Search customers...')