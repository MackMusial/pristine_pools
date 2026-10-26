from nicegui import ui
import store

# ---------- Themes ----------
# Color options to show the client so she can pick one.
THEMES = {
    'pool': {'primary': '#0369a1', 'secondary': '#0d9488', 'accent': '#38bdf8'},
    'aqua': {'primary': '#1e3a8a', 'secondary': '#06b6d4', 'accent': '#f59e0b'},
    'ocean': {'primary': '#0f172a', 'secondary': '#22d3ee', 'accent': '#a78bfa'},
}

CURRENT_THEME = 'pool'  # hardcoded: only one theme will be chosen in the end
def needs_attention():
    cust = []
    for cid, c in store.customers.items():
        if c['retest'] is not None:
            cust.append((cid, c))  #one (id,customer) tuple 
    due = sorted(cust, key=lambda pair: pair[1]['retest']['due'])  #oldest due date first 
    open_list = []
    for cid, c in store.customers.items():
        open_p = None
        for p in c["problems"]:
            if p['fix'] is None:
                open_p = p 
                break
        if open_p:
            open_list.append((cid, c, open_p))
    return due, open_list
def page_layout():
    ui.add_css('@media print { * { print-color-adjust: exact; -webkit-print-color-adjust: exact; } }')  #allows colors when printing
    ui.add_css('.customer-menu { max-height: 200px !important; }')
    ui.query('body').classes('bg-slate-100 print:bg-white')
    ui.colors(**THEMES[CURRENT_THEME])

    #---------- Left Drawer ----------
    drawer = ui.left_drawer(value=False).props('overlay bordered').classes('print:hidden')
    @ui.refreshable
    def drawer_content():
        due, open_list = needs_attention()
        with ui.row().classes('items-center gap-2'):
            ui.icon('notifications_active', color='red')
            ui.label('Needs attention').classes('text-lg font-semibold')
        ui.label('Retests due').classes('text-sm uppercase tracking-wide text-gray-500 mt-4')
        with ui.list():
            for cid, c in due:
                r = c['retest']
                if r['due'] < store.TODAY:
                    when = 'Overdue'
                elif r['due'] == store.TODAY:
                    when = 'Today'
                else:
                    when = f"{r['due']:%b} {r['due'].day}"

                with ui.item(on_click=lambda cid=cid: ui.navigate.to(f'/customer/{cid}')):  #opens this customer on Water Tests
                    with ui.item_section():
                        ui.item_label(c['name'])
                        ui.item_label(when).props('caption').classes('text-red-9' if when == 'Overdue' else '') 
                        if when == 'Overdue':
                            ui.item_label(c['phone']).props('caption')
        ui.label('Open problems').classes('text-sm uppercase tracking-wide text-gray-500 mt-4')
        with ui.list():
            for cid, c, p in open_list:
                with ui.item(on_click=lambda cid=cid: ui.navigate.to(f"/customer/{cid}?tab=problems")):
                    with ui.item_section():
                        ui.item_label(c['name'])
                        ui.item_label(p['title']).props('caption')
    with drawer:
        drawer_content()

    # ---------- Header ----------

    with ui.header().classes('items-center justify-between print:hidden'):  # spreads the three groups across the header. Print:hidden hides the header from the print screen 
        with ui.row().classes('items-center'):
            with ui.button(icon='menu',on_click=drawer.toggle).props('flat color=white'):
                @ui.refreshable
                def badge():
                    due, open_list = needs_attention()  #get fresh data
                    due_now = [cid for cid, c in due if c['retest']['due'] <= store.TODAY]  #keep only the ones that are due today or overdue
                    count = len(due_now) + len(open_list)  #total number of due now and open problems
                    if count:
                        ui.badge(str(count)).props('floating color=red')
                badge()
                if False:
                    ui.badge(str(False)).props('floating color=red')
            # ---------- Logo (Home link) ----------

            with ui.row().classes('items-center gap-2 cursor-pointer') as logo:  # icon + title act as one clickable Home link
                ui.icon('pool')
                ui.label('Pristine Pools').classes('text-2xl font-extrabold tracking-wide')
            logo.on('click', lambda:ui.navigate.to('/'))  # navigate to Home

        # ---------- Customer Search ----------

        search = ui.select(store.search_options(),with_input=True,label='Find customer',on_change=lambda e: ui.navigate.to(f'/customer/{e.value}') if e.value else None).props('dense dark standout popup-content-class="customer-menu"').classes('w-96')
        with search.add_slot('prepend'):
            ui.icon('search')

        # ---------- Action Buttons ----------

        with ui.row().classes('items-center'):
            ui.button('New Customer', icon='group_add').props('flat color=white')
            ui.button(icon='settings',on_click=lambda: ui.navigate.to('/settings')).props('flat round color=white')  # opens the Settings panel