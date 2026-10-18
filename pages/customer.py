from nicegui import ui
from layout import page_layout, CUSTOMERS


@ui.page('/customer/{customer_id}')
def customer(customer_id: int):
    page_layout()
    with ui.column().classes('w-full max-w-screen-2xl mx-auto p-6 gap-6 md:h-[calc(100vh-7rem)]'):  # centered page column with padding
        with ui.row().classes('w-full items-center justify-between'):
            ui.label(CUSTOMERS[customer_id]).classes('text-2xl font-bold')
        with ui.row().classes('w-full no-wrap gap-6 items-start md:flex-1 md:min-h-0'):
            with ui.column().classes('w-1/3 md:h-full'):

                #---------- Contact Card ----------
                with ui.card().classes('w-full gap-1'):
                    ui.label('Contact').classes('text-lg font-semibold')
                    #with ui.grid(columns='auto 1fr').classes('items-baseline w-full gap-x-4 gap-y-1'):  #items-baseline moves the text to the bottom of the line. without it the Contact header would be slightly higher than the actual data
                    ui.label('Address').classes('text-xs text-gray-500')
                    ui.label('4127 Bay Rd, Saginaw, MI 48603')
                    ui.label('Phone').classes('text-xs text-gray-500')
                    ui.label('(989) 555-0142')
                    ui.label('Customer since').classes('text-xs text-gray-500')
                    ui.label('May 2026')

                #---------- Pool Card ----------
                with ui.card().classes('w-full gap-1'):
                    ui.label('Pool').classes('text-lg font-semibold')
                    #with ui.grid(columns='auto 1fr').classes('items-baseline w-full gap-x-4 gap-y-1'):    
                    ui.label('Size').classes('text-xs text-gray-500')
                    ui.label('24 ft round · 52 in wall · 15,000 gal')
                    ui.label('Wall / liner').classes('text-xs text-gray-500')
                    ui.label('Hard-sided steel · 25 mil overlap liner')
                    ui.label('Floor').classes('text-xs text-gray-500')
                    ui.label('Sand base')
                    ui.label('Filter').classes('text-xs text-gray-500')
                    ui.label('Sand filter · 150 lbs sand')
                    ui.label('Chlorinator').classes('text-xs text-gray-500')
                    ui.label('None')
                    ui.label('Installed').classes('text-xs text-gray-500')
                    ui.label('June 2026 · Great Lakes Pool Install')

            with ui.column().classes('flex-1 md:h-full md:overflow-y-auto'):
                with ui.tabs() as tabs:
                    test_tab = ui.tab('Water Tests', icon='science')
                    problems_tab = ui.tab('Problems', icon='report_problem')
                    purchases_tab = ui.tab('Purchases',icon='shopping_cart')
                with ui.tab_panels(tabs, value=test_tab).classes('w-full'):
                    with ui.tab_panel(test_tab):
                        with ui.card().classes('w-full'):
                            with ui.row().classes('w-full items-center justify-between'):
                                ui.label('Latest test · Oct 15').classes('text-lg font-semibold')
                                ui.button(icon='print')
                            with ui.row().classes('gap-2'):
                                ui.badge('pH 7.9',color='red')
                                ui.badge('FC 0.5',color='red')
                                ui.badge('Alk 100',color='green')
                        columns = [
                            {'name': 'date', 'label': 'Date', 'field': 'date'},
                            {'name': 'ph',   'label': 'pH',   'field': 'ph'},
                            {'name': 'fc',   'label': 'FC',   'field': 'fc'},
                        ]
                        rows = [
                            {'date': 'Oct 15', 'ph': 7.9, 'fc': 0.5},
                            {'date': 'Oct 1',  'ph': 7.5, 'fc': 3.0},
                            {'date': 'Sep 17', 'ph': 7.4, 'fc': 2.8},
                        ]
                        ui.table(columns=columns, rows=rows).classes('w-full')

                    #---------- Log a Problem ----------
                    with ui.tab_panel(problems_tab):
                        suggestions = [
                            'Lower pH first: add about 1.5 lbs of pH reducer (sodium bisulfate), circulate 4 hours, retest. Target pH 7.4–7.6.',
                            'Shock tonight with 3 lbs of cal-hypo (73%), then brush the walls and floor. Run the filter 24 hours straight.',
                            'Add a dose of algaecide after shocking, then backwash the sand filter once the water clears. Retest in 2 days.',
                        ]
                        with ui.row().classes('w-full no-wrap gap-4 items-start'):
                            with ui.card().classes('w-1/3'):
                                ui.label('Log a Problem').classes('text-lg font-semibold')
                                ui.button('Get Suggestion')
                                problem_description = ui.textarea(placeholder="Describe the customers problem...").props('outlined autogrow').classes('w-full')#autogrow starts the box at one line and grows on as the user types

                    #---------- Suggestion ----------
                            with ui.card().classes('flex-1'):
                                ui.label('Suggestions').classes('text-lg font-semibold')
                                selection = ui.radio(suggestions,on_change=lambda e: fix_box.set_value(e.value))#e.value is the suggestion text that was picked. .set value is how you change an elements value from code
                                fix_box = ui.textarea(label='Fix applied').props('outlined clearable autogrow').classes('w-full')
                                with ui.row().classes('w-full justify-end'):
                                    ui.button('Save Fix').classes('justify-end')


                    #---------- Purchases Tab ----------
                    with ui.tab_panel(purchases_tab):
                        ui.label('Purchases go here')
