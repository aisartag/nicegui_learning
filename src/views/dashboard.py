from nicegui import ui
import logging
from core.log_loader import configExtra
# from routing import ROUTES



logger = logging.getLogger(f"{configExtra['root_name']}.{__name__}")


def DashboardView():
    logger.info(f"Dashboard avviata:{ui.context.client.id}")
    
<<<<<<< HEAD
    with ui.column().classes("items-center"):
        with ui.row().classes(
            "w-[60vw] justify-center items-center border-1 p-4"):
            ui.label("Dashboard")

        with ui.card():
            # ui.label("scheda dashboard").classes("font-bold text-xl")
            # ui.image(source)
            with ui.card_section():
                ui.label('Lorem ipsum dolor sit amet, consectetur adipiscing elit, ...')
            with ui.card_actions():
                ui.button('Invia Info', on_click=lambda: logger.info(f"Un messaggio informativo da dashboard:{ui.context.client.id}"))
                ui.button('Invia Errore', on_click=lambda: logger.error(f"Qualcosa è andato storto! da dashboard:{ui.context.client.id}"))
=======
  
    with ui.row().classes(
        "w-[60vw] justify-center items-center border-3 border-blue-600 p-4"):
        ui.label("Dashboard")

    # route = next(r for r in ROUTES if r["path"] == "/dashboard")
    # sub_links = route.get("links", [])
>>>>>>> dev

    # if sub_links:
    #     ui.sub_pages({r['path']: r['component'] for r in sub_links})
   
                
    
