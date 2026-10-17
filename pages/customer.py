from nicegui import ui
from layout import page_layout, CUSTOMERS


@ui.page('/customer/{customer_id}')
def customer(customer_id: int):
    page_layout()
    with ui.column().classes('w-full max-w-6xl mx-auto p-6 gap-6'):  # centered page column with padding
        with ui.row().classes('w-full items-center justify-between'):
            ui.label(CUSTOMERS[customer_id]).classes('text-2xl font-bold')
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

            with ui.tab_panel(problems_tab):
                ui.label('Problems go here')
            with ui.tab_panel(purchases_tab):
                ui.label('Purchases go here')
