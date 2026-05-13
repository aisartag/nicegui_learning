from collections.abc import Callable
from typing import Any, List
from nicegui import ui

from components.select_theme import theme_choice
from routing.route_master import MasterRoute
from themes.theme_manager import ThemeManager


from functools import partial
from typing import Callable, List
from nicegui import ui


class WidgetsLayout:

    is_mobile = False

    @classmethod
    def set_mobile(cls, is_mobile: bool):
        cls.is_mobile = is_mobile

    @classmethod
    def render_menu_master_as_buttons(cls, callback: Callable[[], Any] | None = None):
        # 1. Definiamo la logica interna (helper)
        def _handle_click(path: str, cb: Callable[[], Any] | None):
            ui.navigate.to(path)
            if cb:
                cb()

        routes = MasterRoute.get_router_links()
        btnList: List[ui.button] = []

        for route in routes:
            if route["path"] != "/":
                # 2. Usiamo partial per collegare i dati specifici
                handler = partial(_handle_click, route["path"], callback)

                btn = (
                    ui.button(route["label"], on_click=handler)
                    .props("no-caps flat")
                    .classes(
                        "px-4 py-2 font-bold text-lg text-blue-800 dark:text-blue-200"
                    )
                )
                btnList.append(btn)

        return btnList

    @classmethod
    def render_menu_for_childrens_as_buttons(
        cls, routes: List[dict[str, str]], callback: Callable[[], Any] ):
        # 1. Definiamo la logica interna (helper)
        def _handle_click(path: str, cb: Callable[[], Any] ):
            ui.navigate.to(path)
            if  cls.is_mobile:
                cb()

        # routes = MasterRoute.get_router_links()
        btnList: List[ui.button] = []

        for route in routes:
            if route["path"] != "/":
                # 2. Usiamo partial per collegare i dati specifici
                handler = partial(_handle_click, route["path"], callback)

                btn = (
                    ui.button(route["label"], on_click=handler)
                    .props("no-caps flat")
                    .classes(
                        "px-4 py-2 font-bold text-lg text-blue-800 dark:text-blue-200"
                    )
                )
                btnList.append(btn)

        return btnList

    @classmethod
    def render_menu_as_dropdown(cls, theme_manager: ThemeManager):
        """
        Renderizza il menu con i link della route come dropdown"""
        # h-[calc(100vh-128px)]

        with ui.dialog().props(
            'position=right backdrop-filter="blur(8px) brightness(40%)"'
        ) as dialog:
            with ui.card().classes(
                "absolute-right m-2 mr-1 !h-min-co  w-64 items-start bg-slate-100 text-slate-800 dark:bg-slate-900  dark:text-blue-200"
            ).style("height: 600px"):
                with ui.row().classes("w-full"):
                    ui.button(icon="close", on_click=dialog.close).props(
                        "round flat ripple"
                    ).classes("ml-auto")

                ui.separator().classes("w-full")

                with ui.column().classes("w-full"):
                    cls.render_menu_master_as_buttons(dialog.close)

                ui.separator().classes("w-full")

                with ui.row().classes("items-baseline"):
                    ui.label("Theme:").classes("text-lg")
                    theme_choice(theme_manager, dialog)

        ui.button(icon="more_vert", on_click=dialog.open).props(
            "round flat ripple"
        ).classes("lt-md text-blue-800 dark:text-blue-200")
