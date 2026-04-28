from nicegui import ui
import logging
from core.log_loader import configExtra

from routing.root_children import ROUTES_ROOT_CHILDREN
# from views.report_view import ReportView
# from views.statistics_view import StatisticsView




logger = logging.getLogger(f"{configExtra['root_name']}.{__name__}")


def DashboardView():
    logger.info(f"Dashboard avviata:{ui.context.client.id}")

    with ui.row().classes(
        "w-[60vw] justify-center items-center border-3 border-blue-600 p-4"
    ):
        ui.label(f"Dashboard Path Request: {ui.context.client.request.url.path}")
         
        ui.label(f"Dashboard Path Page: {__name__.split('.')[-1]}")

    
    route = next((r for r in ROUTES_ROOT_CHILDREN if r["root"] == '/dashboard'), None)
    childrens = route["childrens"] if route is not None else []
    
    if len(childrens) > 0:
        ui.sub_pages({r["path"]: r["component"] for r in childrens})
    
    # for children in childrens:
    #     # ui.label(children["label"])
    #     ui.label(f"Path: {children['path']}") 
    #     ui.label(f"Component: {(children['component']).__name__}") #ui.label(f"Component: {children['component']}") #children["component"].__name__)
    

   
    # ui.sub_pages({"/dashboard/report": ReportView, "/dashboard/statistics": StatisticsView})

   