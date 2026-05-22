from nicegui import ui
import logging
from core.log_loader import configExtra

from routing.route_childrens import ChildrenRegistry

# from views.report_view import ReportView
# from views.statistics_view import StatisticsView


logger = logging.getLogger(f"{configExtra['root_name']}.{__name__}")

NAME = "Dashboard"


def DashboardView():
    logger.info(f"{NAME} avviata:{ui.context.client.id}")

    with ui.row().classes("w-full justify-center items-center border-2 border-red-600"):
        with ui.card().classes("m-auto"):
            with ui.card_section():
                with ui.row().classes(
                    "w-[60vw] justify-center items-center border-3 border-blue-600 p-4"
                ):
                    ui.label(NAME)

            with ui.card_actions():
                ui.button(
                    "Invia Info",
                    on_click=lambda: logger.info(f"Un messaggio informativo da {NAME}"),
                )
                ui.button(
                    "Invia Errore",
                    on_click=lambda: logger.error(
                        f"Qualcosa è andato storto! da {NAME}"
                    ),
                )

            # if hasattr(ChildrenRegistry,CHILDREN_ATTRIBUTE):
            #     childrens = ChildrenRegistry.as_nicegui_dict(CHILDREN_ATTRIBUTE)
            #     logger.info(f"childrens:{childrens}")
            #     if childrens:
            #         ui.sub_pages(childrens)
            #     else:
            #         logger.warning(f"non ci sono childrens per {NAME} - {ui.context.client.id}")
            # else:
            #     logger.error(f'{CHILDREN_ATTRIBUTE} non trovati per {NAME} - {ui.context.client.id}')

            childrens = ChildrenRegistry.as_nicegui_dict("DASHBOARD_CHILDREN")
            if childrens:
                ui.sub_pages(childrens)
            else:
                logger.warning(
                    f"non ci sono childrens per {NAME} - {ui.context.client.id}"
                )
