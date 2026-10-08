from nicegui import ui
from layout import page_layout

@ui.page('/')
def home():
    page_layout()
#--------------------SEARCH------------------------------
    with ui.column().classes('w-full max-w-6xl mx-auto p-6 gap-6'):#centers the content and adds padding and gap between elements
        with ui.input(placeholder='Search by name or phone...').classes('w-full').props('outlined clearable autofocus').add_slot('prepend'):
            ui.icon('search')
#--------------------Today's stats-------------------------
        with ui.row().classes('w-full'):#creates a row for the cards to be displayed in for the quick actions
            with ui.card().classes('flex-1'):#tests today card
                with ui.row().classes('items-center gap-4'):
                    ui.icon('science').classes('text-4xl text-accent')
                    ui.label('Tests today').classes('text-sm text-gray-500')
                    ui.label('7').classes('text-4xl font-bold')
            with ui.card().classes('flex-1'):#open problems card
                with ui.row().classes('items-center gap-4'):
                    ui.icon('warning').classes('text-4xl text-orange-500')#warning icon next to open problems card
                    ui.label('Open problems').classes('text-sm text-gray-500')
                    ui.label('3').classes('text-4xl font-bold')

#--------------------QUICK ACTIONS--------------------

        with ui.card().classes('w-full'):
            ui.label('Quick Actions').classes('text-lg font-semibold')
            with ui.row().classes('w-full'):
                ui.button('New Water Test', icon='science').classes('flex-1 h-24').props('stack')
                ui.button('Add Customer', icon='person_add').classes('flex-1 h-24').props('stack')

#--------------------RECENT CUSTOMERS--------------------
#future GUI will have a forloop to iterate through recent customer but for demo GUI copy and pasting works just fine 
        with ui.card().classes('w-full'):
            ui.label('Recent Customers').classes('text-lg font-semibold')
            with ui.list().props('separator'):
                
                with ui.item():
                    with ui.item_section():
                        ui.item_label('Nick McArdle')
                        ui.item_label('(989) 555-0142 · Last test: Oct 6').props('caption')

                with ui.item():
                    with ui.item_section():
                        ui.item_label('Keith Ho')
                        ui.item_label('(989) 555-0142 · Last test: Oct 6').props('caption')

                with ui.item():
                    with ui.item_section():
                        ui.item_label('Manish Shrestha')
                        ui.item_label('(989) 555-0142 · Last test: Oct 6').props('caption')

                with ui.item():
                    with ui.item_section():
                        ui.item_label('Marcelino Chapa')
                        ui.item_label('(989) 555-0142 · Last test: Oct 6').props('caption')
