from nicegui import ui
import logging
from core.log_loader import configExtra
from routing.root_children import ROUTES_ROOT_CHILDREN

NAME="Settings"

logger = logging.getLogger(f"{configExtra['root_name']}.{__name__}")


def SettingsView():
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


    route = next((r for r in ROUTES_ROOT_CHILDREN if r["root"] == '/settings'), None)
    childrens = route["childrens"] if route is not None else []
    
    if len(childrens) > 0:
        sub_pages = {r["path"]: r["component"] for r in childrens if r["path"]}
        ui.sub_pages(sub_pages)

    
