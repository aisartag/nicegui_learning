from nicegui import ui
import logging
from core.log_loader import configExtra



logger = logging.getLogger(f"{configExtra['root_name']}.{__name__}")


def AboutView():
    logger.info(f"Settings avviata:{ui.context.client.id}")
    
  
    with ui.row().classes(
        "w-[60vw] justify-center items-center border-3 border-blue-600  p-4"):
        ui.label("About")


    with ui.card():
        # ui.label("scheda dashboard").classes("font-bold text-xl")
        # ui.image(source)
        with ui.card_section():
            ui.label('Lorem ipsum dolor sit amet, consectetur adipiscing elit, ...')
        with ui.card_actions():
            ui.button('Invia Info', on_click=lambda: logger.info(f"Un messaggio informativo da about:{ui.context.client.id}"))
            ui.button('Invia Errore', on_click=lambda: logger.error(f"Qualcosa è andato storto! da about:{ui.context.client.id}"))

    
