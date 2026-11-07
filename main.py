from nicegui import ui
import pages.home  # runs home.py so its '/' page gets registered
import pages.settings  # runs settings.py so its '/settings' page gets registered
import pages.customer  # runs customer.py so its '/customer/{id}' page gets registered
import pages.tabular_pools  # runs tabular_pools.py so its '/customer/{id}/tabular_pools' page gets registered

ui.run(title='Pristine Pools')  # browser tab title (was 'NiceGUI')