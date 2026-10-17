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
