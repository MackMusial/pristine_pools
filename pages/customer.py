from nicegui import ui
from layout import page_layout, CUSTOMERS


@ui.page('/customer/{customer_id}')
def customer(customer_id: int):
    page_layout()
    with ui.column().classes('w-full max-w-6xl mx-auto p-6 gap-6'):  # centered page column with padding
        with ui.row().classes('w-full items-center justify-between'):
            ui.label(CUSTOMERS[customer_id]).classes('text-2xl font-bold')

        #---------- Contact Card ----------
        with ui.card().classes('flex-1 w-full'):
            ui.label('Contact').classes('text-lg font-semibold')
            ui.label('Address').classes('text-xs text-gray-500')
            ui.label('4127 Bay Rd, Saginaw, MI 48603')
            ui.label('Phone').classes('text-xs text-gray-500')
            ui.label('(989) 555-0142')
            ui.label('Customer since').classes('text-xs text-gray-500')
            ui.label('May 2026')

        #---------- Pool Card ----------
        with ui.card().classes('flex-1 w-full'):
            ui.label('Pool').classes('text-lg font-semibold')
            ui.label('Size').classes('text-xs text-gray-500')
            ui.label('24 ft round · 52 in wall · 15,000 gal')
            ui.label('Wall / liner').classes('text-xs text-gray-500')
            ui.label('Hard-sided steel · 25 mil overlap liner')
            ui.label('Floor').classes('text-xs text-gray-500')
            ui.label('Sand base')
            ui.label('Filter').classes('text-xs text-gray-500')
            ui.label('Sand filter · 150 lbs sand')
            ui.label('Chlorinator').classes('text-xs text-gray-500')
            ui.label('None')
            ui.label('Installed').classes('text-xs text-gray-500')
            ui.label('June 2026 · Great Lakes Pool Install')

        with ui.tabs() as tabs:
            test_tab = ui.tab('Water Tests', icon='science')
            problems_tab = ui.tab('Problems', icon='report_problem')
            purchases_tab = ui.tab('Purchases',icon='shopping_cart')
        with ui.tab_panels(tabs, value=test_tab).classes('w-full'):
            with ui.tab_panel(test_tab):
                with ui.card().classes('w-full'):
                    with ui.row().classes('w-full items-center justify-between'):
                        ui.label('Latest test · Oct 15').classes('text-lg font-semibold')
                        ui.button(icon='print')
                    with ui.row().classes('gap-2'):
                        ui.badge('pH 7.9',color='red')
                        ui.badge('FC 0.5',color='red')
                        ui.badge('Alk 100',color='green')
                columns = [
                    {'name': 'date', 'label': 'Date', 'field': 'date'},
                    {'name': 'ph',   'label': 'pH',   'field': 'ph'},
                    {'name': 'fc',   'label': 'FC',   'field': 'fc'},
                ]
                rows = [
                    {'date': 'Oct 15', 'ph': 7.9, 'fc': 0.5},
                    {'date': 'Oct 1',  'ph': 7.5, 'fc': 3.0},
                    {'date': 'Sep 17', 'ph': 7.4, 'fc': 2.8},
                ]
                ui.table(columns=columns, rows=rows).classes('w-full')
            #---------- Problems Tab ----------
            with ui.tab_panel(problems_tab):
                with ui.card().classes('w-full'):
                    ui.label('Log a Problem').classes('text-lg font-semibold')
                    ui.button('Get Suggestion')
                    problem_description = ui.textarea(placeholder="Describe the customers problem...").props('outlined').classes('w-full')
            #---------- Purchases Tab ----------
            with ui.tab_panel(purchases_tab):
                ui.label('Purchases go here')
