from nicegui import ui

# ---------- Themes ----------
# Color options to show the client so she can pick one.
THEMES = {
    'pool': {'primary': '#0369a1', 'secondary': '#0d9488', 'accent': '#38bdf8'},
    'aqua': {'primary': '#1e3a8a', 'secondary': '#06b6d4', 'accent': '#f59e0b'},
    'ocean': {'primary': '#0f172a', 'secondary': '#22d3ee', 'accent': '#a78bfa'},
}
CUSTOMERS = {  # hardcoded sample customers for the demo UI
    1: 'Nick McArdle · (989) 555-0142',
    2: 'Manish Shrestha · (989) 555-0185',
    3: 'Marcelino J. Chapa · (989) 555-0136',
    4: 'Keith Ho · (989) 555-0164',
    5: 'Sarah Johnson · (989) 555-0118',
    6: 'Mike Kowalski · (989) 555-0127',
    7: 'Emily Rivera · (989) 555-0133',
    8: 'Dave Thompson · (989) 555-0149',
    9: 'Jessica Nguyen · (989) 555-0156',
    10: 'Tom Brennan · (989) 555-0161',
    11: 'Amanda Schultz · (989) 555-0172',
    12: 'Chris Patel · (989) 555-0184',
    13: 'Linda Kaminski · (989) 555-0190',
    14: 'Ryan O\'Connell · (989) 555-0103',
    15: 'Megan Fischer · (989) 555-0115',
    16: 'Jake Wojcik · (989) 555-0138',
}
CURRENT_THEME = 'pool'  # hardcoded: only one theme will be chosen in the end


def page_layout():
    ui.add_css('.customer-menu { max-height: 200px !important; }')
    ui.query('body').classes('bg-slate-100')
    ui.colors(**THEMES[CURRENT_THEME])

    # ---------- Left Drawer ----------

    with ui.left_drawer(value=False) as drawer:
        ui.label('Recent customers').classes('text-xs font-semibold text-gray-500 uppercase px-4 pt-2')
        with ui.list().props('dense').classes('w-full'):
            with ui.item(on_click=lambda: None):
                with ui.item_section():
                    ui.item_label('Nick McArdle')
                    ui.item_label('(989) 555-0142 · Last test: Oct 6').props('caption')
            with ui.item(on_click=lambda: None):
                with ui.item_section():
                    ui.item_label('Manish Shrestha')
                    ui.item_label('(989) 537-7385 · Last test: Oct 10').props('caption')
            with ui.item(on_click=lambda: None):
                with ui.item_section():
                    ui.item_label('Marcelino J. Chapa')
                    ui.item_label('(989) 548-9736 · Last test: Oct 19').props('caption')
            with ui.item(on_click=lambda: None):
                with ui.item_section():
                    ui.item_label('Keith Ho')
                    ui.item_label('(989) 723-9264 · Last test: Sept 22').props('caption')

    # ---------- Header ----------

    with ui.header().classes('items-center justify-between'):  # spreads the three groups across the header
        with ui.row().classes('items-center'):
            ui.button(icon='menu',on_click=drawer.toggle).props('flat color=white')  # opens/closes the left drawer

            # ---------- Logo (Home link) ----------

            with ui.row().classes('items-center gap-2 cursor-pointer') as logo:  # icon + title act as one clickable Home link
                ui.icon('pool')
                ui.label('Pristine Pools').classes('text-2xl font-extrabold tracking-wide')
            logo.on('click', lambda:ui.navigate.to('/'))  # navigate to Home

        # ---------- Customer Search ----------

        search = ui.select(CUSTOMERS,with_input=True,label='Find customer',on_change=lambda e: ui.navigate.to(f'/customer/{e.value}') if e.value else None).props('dense dark standout popup-content-class="customer-menu"').classes('w-96')
        with search.add_slot('prepend'):
            ui.icon('search')

        # ---------- Action Buttons ----------

        with ui.row().classes('items-center'):
            ui.button('New Customer', icon='group_add').props('flat color=white')
            ui.button(icon='settings',on_click=lambda: ui.navigate.to('/settings')).props('flat round color=white')  # opens the Settings page