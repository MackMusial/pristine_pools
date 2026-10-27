from nicegui import ui
from layout import page_layout
import store

@ui.page('/')
def home():
    page_layout(show_search=False)  # the big search below replaces the header one

    #---------- Find a Customer ----------
    with ui.column().classes('w-full items-center justify-center min-h-[calc(100vh-10rem)] gap-2'):  # centered on the screen
        ui.label('Find a customer').classes('text-4xl font-bold')
        ui.label('Search by name or phone').classes('text-gray-500')
        search = ui.select(store.search_options(), with_input=True, label='Customer', on_change=lambda e: ui.navigate.to(f'/customer/{e.value}') if e.value else None).props('outlined autofocus').classes('w-full max-w-xl pt-4')  # autofocus: staff can start typing right away
        with search.add_slot('prepend'):
            ui.icon('search')
