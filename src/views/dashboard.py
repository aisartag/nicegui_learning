from nicegui import ui
import logging
from core.log_loader import configExtra
# from routing import ROUTES



logger = logging.getLogger(f"{configExtra['root_name']}.{__name__}")


def DashboardView():
    logger.info(f"Dashboard avviata:{ui.context.client.id}")
    
  
    with ui.row().classes(
        "w-[60vw] justify-center items-center border-3 border-blue-600 p-4"):
        ui.label("Dashboard")

    # route = next(r for r in ROUTES if r["path"] == "/dashboard")
    # sub_links = route.get("links", [])

    # if sub_links:
    #     ui.sub_pages({r['path']: r['component'] for r in sub_links})
   
                
    
