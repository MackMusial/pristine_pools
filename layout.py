from datetime import date, timedelta
from nicegui import ui
import store

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


# ---------- Needs Attention (live) ----------
# @ui.refreshable: calling .refresh() rebuilds just this part of the page from the current store data.

def customer_name(cid):
    return CUSTOMERS[cid].split(' · ')[0]


def customer_phone(cid):
    return CUSTOMERS[cid].split(' · ')[1]


#---------- Red Number on the hamburger ----------
@ui.refreshable
def attention_badge():
    count = len(store.retests_due) + len(store.open_problems)
    if count > 0:  # no badge at 0
        ui.badge(str(count), color='red').props('floating')

#---------- Drawer lists rebuilt from store everyime they're drawn ----------
@ui.refreshable
def attention_lists():
    today = date.today()

    ui.label('Retests due').classes('text-xs uppercase font-bold text-gray-500')
    if not store.retests_due:
        ui.label('Nothing due 🎉').classes('text-sm text-gray-400 px-4 py-2')
    with ui.list().props('dense').classes('w-full'):
        for r in sorted(store.retests_due, key=lambda r: r['due']):  # soonest first
            if r['due'] < today:
                when, color = 'Overdue', 'text-red-600'
            elif r['due'] == today:
                when, color = 'Today', 'text-orange-600'
            else:
                when, color = r['due'].strftime('%b %d'), ''
            with ui.item(on_click=lambda cid=r['cid']: ui.navigate.to(f'/customer/{cid}')):  #naviate to the customers data if their card is clicked
                with ui.item_section():
                    ui.item_label(customer_name(r['cid']))
                    ui.item_label(f"{when} · {r['reason']}").props('caption').classes(color)
                    if r['due'] < today:  # overdue: show the phone so staff can call
                        with ui.row().classes('items-center gap-1 text-xs text-red-600'):
                            ui.icon('call', size='xs')
                            ui.label(customer_phone(r['cid']))

    ui.separator()
    ui.label('Open problems').classes('text-xs uppercase font-bold text-gray-500')
    if not store.open_problems:
        ui.label('Nothing open 🎉').classes('text-sm text-gray-400 px-4 py-2')
    with ui.list().props('dense').classes('w-full'):
        for p in store.open_problems:
            with ui.item(on_click=lambda cid=p['cid']: ui.navigate.to(f'/customer/{cid}')):
                with ui.item_section():
                    ui.item_label(customer_name(p['cid']))
                    ui.item_label(f"{p['logged'].strftime('%b %d')} · {p['text']}").props('caption')


def refresh_attention():
    attention_badge.refresh()  #updates badge and draws it again. without it, the badge would only update when the page is reloaded
    attention_lists.refresh()


def schedule_retest(cid, days, reason):
    """Opens a 'Schedule retest?' dialog with the date pre-filled to today + days."""
    with ui.dialog() as dialog, ui.card():
        ui.label('Schedule a retest?').classes('text-lg font-semibold')
        ui.label(f'{customer_name(cid)} · {reason}').classes('text-gray-500')
        picker = ui.date(value=(date.today() + timedelta(days=days)).isoformat())  # ui.date uses 'YYYY-MM-DD' text

        def save():
            store.set_retest(cid, date.fromisoformat(picker.value), reason)
            refresh_attention()
            dialog.close()

        with ui.row().classes('w-full justify-end'):
            ui.button('Skip', on_click=dialog.close).props('flat')
            ui.button('Schedule', icon='event', on_click=save)
    dialog.open()


def page_layout():
    ui.add_css('@media print { * { print-color-adjust: exact; -webkit-print-color-adjust: exact; } }')  #allows colors when printing
    ui.add_css('.customer-menu { max-height: 200px !important; }')
    ui.query('body').classes('bg-slate-100 print:bg-white')
    ui.colors(**THEMES[CURRENT_THEME])

    # ---------- Needs Attention Drawer ----------
    # Created before the header so the ☰ button can use drawer.toggle.

    with ui.left_drawer(value=False).props('overlay bordered').classes('bg-white print:hidden') as drawer:  # starts closed, floats over the page
        attention_lists()

    # ---------- Header ----------

    with ui.header().classes('items-center justify-between print:hidden'):  # spreads the three groups across the header. Print:hidden hides the header from the print screen
        with ui.row().classes('items-center'):
            with ui.button(icon='menu', on_click=drawer.toggle).props('flat round color=white'):  # opens/closes the left drawer
                attention_badge()
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
