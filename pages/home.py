from nicegui import ui
from layout import page_layout

@ui.page('/')
def home():
    page_layout()
    def show_chat():
        welcome.set_visibility(False)
        messages.set_visibility(True)
    
    # ---------- Chat Bar (footer) ----------
    with ui.footer().classes('bg-slate-100'):
        with ui.row().classes('w-full max-w-3xl mx-auto justify-center items-center'):
            chat = ui.input(placeholder='Ask about a pool problem...').classes('flex-1').props('outlined rounded')
            with chat.add_slot('prepend'):
                ui.button(icon='add').props('flat round dense')
            with chat.add_slot('append'):
                ui.button(icon='send',on_click=show_chat).props('flat round dense')

    #---------- Welcome ----------

    with ui.column().classes(' w-full items-center justify-center min-h-[calc(100vh-10rem)] gap-2') as welcome:
        ui.label('How can I help today?').classes('text-4xl font-bold')
        ui.label("Describe a customer's pool problem, or attach a customer with +").classes('text-gray-500')
        with ui.row().classes('gap-2 justify-center pt-4'):
            ui.chip('Green water', icon='eco').props('outline clickable')
            ui.chip('Cloudy water', icon='cloud').props('outline clickable')
            ui.chip('Low chlorine', icon='science').props('outline clickable')
            ui.chip('Opening a pool', icon='pool').props('outline clickable')

    # ---------- Chat Messages ----------
    with ui.column().classes('w-full max-w-3xl mx-auto') as messages:
        ui.chat_message("Customer's pool turned green overnight. 15,000 gal, free chlorine 0.5, pH 7.9. What should I recommend?", name='Staff', sent=True).props('bg-color=primary text-color=white')
        ui.chat_message('Recommend shocking the pool tonight with 3 lbs of cal-hypo, then lower pH to 7.4–7.6 with pH reducer. Run the filter 24 hours and retest in 2 days.', name='Pool Assistant', sent=False).props('bg-color=white')
    messages.set_visibility(False)
