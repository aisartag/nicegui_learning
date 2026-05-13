from nicegui import ui

from components.select_theme import theme_choice
from themes.theme_manager import ThemeManager
from routing.main_root import ROUTES_ROOT

import logging
from core.log_loader import configExtra

logger = logging.getLogger(f"{configExtra['root_name']}.{__name__}")

def get_header_popup(theme_manager: ThemeManager) -> None:
  
    logger.info(f"get_header_popup avviata:{ui.context.client.id}")
    with ui.dialog().props('position=right backdrop-filter="blur(8px) brightness(40%)"') as dialog:
        logger.info(f"dialog opened:{ui.context.client.id}")
        def handle_click(path: str):
            ui.navigate.to(path)
            dialog.close()

        with ui.card().classes(
            "absolute-right h-[calc(100vh-128px)] m-2 mr-1  w-64 items-start bg-slate-100 text-slate-800 dark:bg-slate-900  dark:text-blue-200"
        ):
            with ui.row().classes("w-full"):
                ui.button(icon="close", on_click=dialog.close).props(
                    "round flat ripple"
                ).classes("ml-auto")

            ui.separator().classes("w-full")

            with ui.column().classes("w-full"):
                # soluzione con partial ??
                #    [ui.button(route["label"], on_click=partial(handle_click, route["path"])).props("flat no-caps") for route in ROUTES if route["path"] != "/"]
                [
                    ui.button(
                        route["label"],
                        on_click=lambda *, r=route: handle_click(r["path"]),
                    ).props("flat no-caps")
                    for route in ROUTES_ROOT
                    if route["path"] != "/"
                ]

            ui.separator().classes("w-full")

            with ui.column():
                ui.label("Color mode:")
                theme_choice(theme_manager)


    ui.button(icon="more_vert", on_click=dialog.open).props(
        "round flat ripple"
    ).classes("md:hidden text-blue-800 dark:text-blue-200")

   

   
