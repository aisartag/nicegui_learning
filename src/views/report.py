from nicegui import ui
import logging
from core.log_loader import configExtra

NAME= 'REPORT'

logger = logging.getLogger(f"{configExtra['root_name']}.{__name__}")


def ReportView():
    logger.info(f"{NAME} avviata:{ui.context.client.id}")
    
  
    with ui.row().classes(
        "w-[60vw] justify-center items-center border-3 border-blue-600 p-4"):
        ui.label(NAME)


    with ui.card():
        # ui.label("scheda dashboard").classes("font-bold text-xl")
        # ui.image(source)
        with ui.card_section():
            ui.label('Lorem ipsum dolor sit amet, consectetur adipiscing elit, ...')
        with ui.card_actions():
            ui.button('Invia Info', on_click=lambda: logger.info(f"Un messaggio informativo da {NAME}:{ui.context.client.id}"))
            ui.button('Invia Errore', on_click=lambda: logger.error(f"Qualcosa è andato storto! da {NAME}:{ui.context.client.id}"))

    
