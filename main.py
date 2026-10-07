from nicegui import ui
from layout import page_layout
import pages.home # runs home.py so its '/' gets registered
import pages.customers #runs customers.py so its '/' gets registered

ui.run()