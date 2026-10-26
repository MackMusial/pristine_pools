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
    def show_chat():
        pass
    def send_message():
        pass
    def ask_chip(text):
        pass
    # ---------- Ai Drawer ----------
    ai_drawer = ui.right_drawer(value=False).props('overlay bordered width=400').classes('print:hidden')
    with ai_drawer:
        with ui.row().classes('w-full items-center justify-between'):  #but x button on the right
            ui.label('Pool assistant').classes('text-lg font-semibold')
            ui.button(icon='close', on_click=ai_drawer.hide).props('flat round dense')  #button to escape the AI Agent

    #---------- Sticky AI Button ----------
    with ui.page_sticky(position='bottom-right', x_offset=24, y_offset=24):
        ui.button(icon='auto_awesome', on_click=ai_drawer.toggle).props('fab color=primary').classes('print:hidden').tooltip('Pool Assistant')  

    #---------- New Customer Dialog ----------
    with ui.dialog() as new_cust_dialog, ui.card().classes('w-96'):
        ui.label('New Customer').classes('w-full text-lg font-semibold')

        name = ui.input(label='Name', validation={'Required': lambda v: bool(v.strip())}).props('outlined dense autofocus hide-bottom-space').classes('w-full')  #the lambda: v: bool(v.strip()) forces the employee to enter a name. even if the name is full of spaces
        phone = ui.input(label='Phone', validation={'Required': lambda v: bool(v.strip())}).props('outlined dense hide-bottom-space').classes('w-full')
        address = ui.input(label='Address').props('outlined dense').classes('w-full')
        zip_code = ui.input(label='Zipcode').props('outlined dense').classes('w-full')

        def save_customer():
            if not all ([name.validate(), phone.validate()]):  # validate() runs the check shows the red error under the box, and returns False when it fails. 
                return
            full_address = f"{address.value}, {zip_code.value}" if zip_code.value else address.value  #add the zipcode only if one was typed, otherwise you get a trailing comma.  
            new_id = max(store.customers) + 1  #max() of a dict, looks at its keys, which are customer ID's
            store.customers[new_id] = {
                'name': name.value.strip(), 'phone': phone.value.strip(), 'address': full_address,
                'since': f"{store.TODAY:%B %Y}",          # 'October 2026'
                'bodies': [], 'tests': [], 'problems': [], 'purchases': [],
                'retest': None,
            }
            search.set_options(store.search_options())  #set_options replaces the list of choices that a ui.select shows in its dropdown
            ui.navigate.to(f'/customer/{new_id}')
        with ui.row().classes('w-full justify-end'):  #row for save and cancel buttons 
            ui.button('Cancel', on_click=new_cust_dialog.close).props('flat')
            ui.button('Save', icon='check', on_click=save_customer)

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
            ui.button('New Customer', icon='group_add', on_click=lambda: new_cust_dialog.open()).props('flat color=white')
            ui.button(icon='settings',on_click=lambda: ui.navigate.to('/settings')).props('flat round color=white')  # opens the Settings panel


    def refresh_attention():
        drawer_content.refresh()
        badge.refresh()
    return refresh_attention