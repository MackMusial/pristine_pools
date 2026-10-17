from nicegui import ui
from layout import page_layout

@ui.page('/')
def home():
    page_layout()
    # ---------- Right Drawer ----------
    with ui.right_drawer():
        ui.label('Customer').classes('text-lg font-semibold')
        ui.label('Nick McArdle').classes('font-medium')
        ui.label('(989) 555-0142').classes('text-sm text-gray-500')
        ui.separator()
        ui.label('Pool').classes('text-lg font-semibold')
        ui.label('24 ft round · hard sided').classes('font-medium')
        ui.label('15000 gal').classes('text-sm text-gray-500')
        ui.separator()
        ui.label("Latest test · October 15").classes('text-lg font-semibold')
        with ui.row().classes('gap-2'):
            ui.badge('pH 7.9',color='red')
            ui.badge('FC 0.5',color='red')
            ui.badge('Alk 100',color='green')
    # ---------- Chat Bar (footer) ----------
    with ui.footer().classes('bg-slate-100'):
        with ui.row().classes('w-full max-w-3xl mx-auto justify-center items-center'):
            chat = ui.input(placeholder='Ask about a pool problem...').classes('flex-1').props('outlined rounded')
            with chat.add_slot('prepend'):
                ui.button(icon='add').props('flat round dense')
            with chat.add_slot('append'):
                ui.button(icon='send').props('flat round dense')
    # ---------- Chat Messages ----------
    with ui.column().classes('w-full max-w-3xl mx-auto'):
        ui.chat_message("Customer's pool turned green overnight. 15,000 gal, free chlorine 0.5, pH 7.9. What should I recommend?",name='Staff',sent=True)
        ui.chat_message('Recommend shocking the pool tonight with 3 lbs of cal-hypo, then lower pH to 7.4–7.6 with pH reducer. Run the filter 24 hours and retest in 2 days.', name='Pool Assistant', sent=False)

