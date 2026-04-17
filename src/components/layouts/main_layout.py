from nicegui import ui
from logging import Logger
from views.dashboard import render as dashboard_render
from core.logger.logset import LoggerSettings


def layout(logger:Logger):
    with ui.header(elevated=True).classes(
        "bg-slate-800 text-slate-100 items-center px-4 items-center justify-between border-5 border-blue-500"
    ):
        ui.label("Benvenuto nella mia App").classes("font-bold tracking-tight")


    # views place
    ui.sub_pages({"/": dashboard_render})

    with ui.card().tight():
        ui.label("logging da layoutd")
        with ui.card_section():
            ui.label('Lorem ipsum dolor sit amet, consectetur adipiscing elit, ...')
        with ui.card_actions():
            ui.button('Invia Info', on_click=lambda: logger.info("Un messaggio informativo da layout"))
            ui.button('Invia Errore', on_click=lambda: logger.error("Qualcosa è andato storto! da layout"))
    # area display log
   

    
   
    log_ui = ui.log(max_lines=50).classes("w-full h-80 font-mono text-sm overflow-auto")
    LoggerSettings().setup_ui_logging(log_ui)

   