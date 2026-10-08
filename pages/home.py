from nicegui import ui
from layout import page_layout

@ui.page('/')
def home():
    page_layout()
    with ui.column().classes('w-full max-w-6x1 mx-auto p-6 gap-6'):
        with ui.row():
                    with ui.card().classes('flex-1'):
                        ui.label('Customers:').classes('text-sm text-gray-500')
                        ui.label('42').classes('text-4xl font-bold')
                    with ui.card().classes('flex-1'):
                        ui.label('Tests this week:').classes('text-sm text-gray-500')
                        ui.label('7').classes('text-4xl font-bold')
                    with ui.card().classes('flex-1'):
                        ui.label('Open problems:').classes('text-sm text-gray-500')
                        ui.label('3').classes('text-4xl font-bold')

        with ui.card():
            ui.label('Quick Actions')
            with ui.row():
                ui.button('New Water Test', icon='science').classes('w-48 h-24').props('stack')
                ui.button('Log Problem', icon='report_problem').classes('w-48 h-24').props('stack')
                ui.button('Add Customer', icon='person_add').classes('w-48 h-24').props('stack')
        
