from nicegui import ui
import logging
from core.config import Config
from core.settings import SettingPaths




def render():
    config = Config().get_config()
    
    logger = logging.getLogger(f"{config['appName']}.{__name__}")
    logger.info("Dashboard avviata")
  
    with ui.row().classes(
        "w-[60vw] justify-center items-center border-3 border-blue-600 bg-gray-300 p-4"):
        ui.label("Saluti da Dashboard")


    image_path = "img/quasar-breakpoints.png"
    source = SettingPaths.get_asset(image_path)
    logger.debug(source)
   
    ui.label("logging da dashboard")
    
       


    with ui.card().tight():
        ui.label("logging da dashboard")
        ui.image(source)
        with ui.card_section():
            ui.label('Lorem ipsum dolor sit amet, consectetur adipiscing elit, ...')
        with ui.card_actions():
            ui.button('Invia Info', on_click=lambda: logger.info("Un messaggio informativo da dashboard"))
            ui.button('Invia Errore', on_click=lambda: logger.error("Qualcosa è andato storto! da dashboard"))

    
