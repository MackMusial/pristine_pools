from nicegui import ui

def page_layout():
    with ui.left_drawer() as drawer:
        ui.button('Home',on_click=lambda: ui.navigate.to('/'))
        ui.button('Customers Page',on_click=lambda: ui.navigate.to('/customers'))
    with ui.header():
        ui.button(icon='menu',on_click=drawer.toggle)
        ui.label('Pristine Pools')
        ui.input(placeholder='Search customers...')
        