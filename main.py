from nicegui import ui
from layout import page_layout
import pages.home #forces compiler to read this file, this file holds home() page


@ui.page('/customers')
def customers():
    page_layout()
    ui.label('Customers')


ui.run()