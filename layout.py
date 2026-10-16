from nicegui import ui

#-----Different themes we can present to the customer and see what they like the most-----
THEMES = {
    'pool': {'primary': '#0369a1', 'secondary': '#0d9488', 'accent': '#38bdf8'},
    'aqua': {'primary': '#1e3a8a', 'secondary': '#06b6d4', 'accent': '#f59e0b'},
    'ocean': {'primary': '#0f172a', 'secondary': '#22d3ee', 'accent': '#a78bfa'},
}
CUSTOMERS = {#customers dict Hardcoded for example UI 
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
CURRENT_THEME = 'pool'#current theme selection... Hardcoded because only one will be selected in the future

def page_layout():
    ui.query('body').classes('bg-slate-100')
    ui.colors(**THEMES[CURRENT_THEME])

#--------------------Hamburger Drawer--------------------

    with ui.left_drawer(value=False) as drawer:
        ui.button('Home',icon='home',on_click=lambda: ui.navigate.to('/')).props('flat align=left').classes('w-full')#button to navigate to home page
        ui.button('Settings',icon='build',on_click=lambda: ui.navigate.to('/settings')).props('flat align=left').classes('w-full')#button to navigate to settings page
        ui.separator()
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

#--------------------Header-------------------------

    with ui.header().classes('items-center justify-between'):#spreads header out 
        with ui.row().classes('items-center'):
            ui.button(icon='menu',on_click=drawer.toggle).props('flat color=white')#hamburger for navigation between pages
            ui.icon('pool')
            ui.label('Pristine Pools').classes('text-xl font-bold')#increase text size and bold characters      
        search = ui.select(CUSTOMERS,with_input=True,label='Find customer',on_change=lambda e: ui.navigate.to(f'/customer/{e.value}')).props('dense dark standout clearable').classes('w-96')
        with search.add_slot('prepend'):
            ui.icon('search')
        with ui.row().classes('items-center'):
            ui.button('New Water Test',icon='science').props('flat color=white')
            ui.button('Add Customer', icon='person_add').props('flat color=white')