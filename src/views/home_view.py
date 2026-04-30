from nicegui import ui
import logging
from core.log_loader import configExtra

NAME= 'Home'

logger = logging.getLogger(f"{configExtra['root_name']}.{__name__}")


def HomeView():
    logger.info(f"{NAME} avviata:{ui.context.client.id}")
    
  
    with ui.row().classes("w-full justify-center items-center border-2 border-red-600"):
        with ui.card().classes("m-auto"):
            with ui.card_section():
                with ui.row().classes(
                    "w-[60vw] justify-center items-center border-3 border-blue-600 p-4"):
                    ui.label(NAME)
                
            with ui.card_actions():
                ui.button('Invia Info', on_click=lambda: logger.info(f"Un messaggio informativo da {NAME}"))
                ui.button('Invia Errore', on_click=lambda: logger.error(f"Qualcosa è andato storto! da {NAME}"))


    
