from nicegui import ui
# from layout import page_layout
import pages.home # runs home.py so its '/' gets registered
import pages.settings #runs customers.py so its '/customers' gets registered
import pages.customer

ui.run()