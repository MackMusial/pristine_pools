from nicegui import ui
from layout import page_layout

@ui.page('/')
def home():
    page_layout()
    with ui.right_drawer():
        ui.label('Customer').classes('text-lg font-semibold')
        ui.label('Nick McArdle').classes('font-medium')
        ui.label('(989) 555-0142').classes('text-sm text-grey-500')
    with ui.footer().classes('bg-slate-100'):
        with ui.row().classes('w-full max-w-3xl mx-auto justify-center items-center'):
            chat = ui.input(placeholder='Ask about a pool problem...').classes('flex-1').props('outlined rounded')
            with chat.add_slot('prepend'):
                ui.button(icon='add').props('flat round dense')
            with chat.add_slot('append'):
                ui.button(icon='send').props('flat round dense')
#------------------------- CHAT BOX -------------------------
    with ui.column().classes('w-full max-w-3xl mx-auto'):
        ui.chat_message("Customer's pool turned green overnight. 15,000 gal, free chlorine 0.5, pH 7.9. What should I recommend?",name='Staff',sent=True)
        ui.chat_message('Recommend shocking the pool tonight with 3 lbs of cal-hypo, then lower pH to 7.4–7.6 with pH reducer. Run the filter 24 hours and retest in 2 days.', name='Pool Assistant', sent=False)

