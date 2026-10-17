from nicegui import ui
import pages.home  # runs home.py so its '/' page gets registered
import pages.settings  # runs settings.py so its '/settings' page gets registered
import pages.customer  # runs customer.py so its '/customer/{id}' page gets registered

ui.run()