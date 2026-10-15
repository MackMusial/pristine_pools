from nicegui import ui
from layout import page_layout

@ui.page('/')
def home():
    page_layout()
    with ui.footer().classes('bg-slate-100'):
        with ui.row().classes('w-full max-w-3xl mx-auto justify-center items-center'):
            chat = ui.input(placeholder='Ask about a pool problem...').classes('flex-1').props('outlined rounded')
            with chat.add_slot('prepend'):
                ui.button(icon='add').props('flat round dense')
            with chat.add_slot('append'):
                ui.button(icon='send').props('flat round dense')

