from nicegui import ui

@ui.page('/')
def home():
    ui.label('Pristine Pools')
    ui.button('Click me', on_click=lambda: ui.notify('It works!'))


ui.run()