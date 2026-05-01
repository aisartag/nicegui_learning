from collections.abc import Callable
from typing import List, cast, get_args
from nicegui import ui, Client, background_tasks, app

from components.header_popup import get_header_popup

# from components.select_theme import theme_choice
from themes.theme_manager import ThemeManager


from routing.main_root import ROUTES_ROOT
from routing.paths_type import PATHS_ROOT
from routing.root_children import ROUTES_ROOT_CHILDREN

from core.log_loader import configExtra
import logging

logger = logging.getLogger(f"{configExtra['root_name']}.{__name__}")


class Layout:
    def __init__(self):

        self.client: Client = ui.context.client

        # apply_brand_theme()
        self.theme_manager = ThemeManager(app.storage.user)

        # with ui.header(elevated=True).classes(
        #     "items-center px-4 items-center justify-between text-red-900 dark:bg-slate-900  dark:text-blue-200"
        # ):

        with ui.header(elevated=False).classes(
            "items-center px-4 items-center justify-between bg-slate-100 text-slate-800 dark:bg-slate-900  dark:text-blue-200"
        ):

            #  menu hamburger
            self.hamburger = (
                ui.button(icon="menu", on_click=lambda: self.drawer.toggle())
                .props("round flat ripple")
                .classes("lt-md text-blue-800 dark:text-blue-200")
            )

            # brand
            ui.link("Nicegui Learning", "/").classes(
                "font-bold tracking-tight px-6 py-3 no-underline text-xl text-blue-800 dark:text-blue-200"
            )

            with ui.row().classes("gap-4 items-center gt-sm tracking-tight"):
                self.get_router_root_btns()

                # toggle dark mode
                ui.button(on_click=self.theme_manager.cycle).bind_icon_from(
                    self.theme_manager, "icon"
                ).props("round ripple flat").classes("text-blue-800 dark:text-blue-200")

            get_header_popup(self.theme_manager)

        with ui.column().classes(
            "w-full min-h-[calc(100vh-384px)] border-2 border-blue-600 items-center justify-start bg-slate-100 dark:bg-slate-800"
        ):
            ui.label("Main Content Area").classes("m-2 font-bold text-xl")
            ui.sub_pages(self.get_router_root_views())

        self.drawer = ui.left_drawer(value=False).classes(
            "bg-slate-100 dark:bg-slate-900"
        )  # .props("permanent")
        with self.drawer:
            ui.label("Menu di navigazione")

        self.handle_path_change(self.get_root_path(self.client.request.url.path))

        self.client.sub_pages_router.on_path_changed(
            lambda path: self.handle_path_change(path)
        )

    def handle_path_change(self, path: str):

        # verifica che sia una chiave di ROUTES_ROOT

        if path not in get_args(PATHS_ROOT):
            logger.info(
                f"handle_path_change changed to: {path} not in {get_args(PATHS_ROOT)}"
            )
            return

        logger.info(f" handle_path_change changed to: {path}")

        route = next((r for r in ROUTES_ROOT_CHILDREN if r["root"] == path), None)
        childrens = route["childrens"] if route is not None else []

        logger.info(
            f" handle_path_change changed have childrens: {len(childrens)} {path}"
        )
        self.drawer.clear()
        if len(childrens) > 0:

            with self.drawer:
                with ui.column().classes("w-full"):
                    for children in childrens:
                        if children["path"] == "/":
                            continue
                        ui.link(children["label"], path + children["path"]).classes(
                            "px-6 py-3 no-underline text-blue-800 dark:text-blue-200"  # text-blue-800 dark:text-blue-200
                        ).on("click", self.drawer.toggle)

        async def check_logic():
            with self.client:
                width = cast(int, await ui.run_javascript("window.innerWidth"))

                self.drawer.value = False if width < 1024 else len(childrens) > 0
                self.hamburger.set_visibility(len(childrens) > 0)

        background_tasks.create(check_logic())  # type: ignore

    def get_root_path(self, path: str) -> str:

        parts = path.strip("/").split("/")
        return f"/{parts[0]}" if parts[0] else "/"

    def get_router_root_links(self):

        lnkList: List[ui.link] = []
        for link in ROUTES_ROOT:
            if link["path"] != "/":
                lnk = ui.link(link["label"], link["path"]).classes(
                    "px-6 py-3 no-underline rounded hover:bg-blue-600 hover:underline hover:text-blue-200"
                )

                lnkList.append(lnk)

        return lnkList

    def get_router_root_btns(self):

        def navigate_to(path: str):
            ui.navigate.to(path)

        btnList: List[ui.button] = []
        for route in ROUTES_ROOT:
            if route["path"] != "/":
                btn = (
                    ui.button(
                        route["label"],
                        on_click=lambda *, r=route["path"]: navigate_to(r),
                    )
                    .props("no-caps flat")
                    .classes("px-6 py-3 text-blue-800 dark:text-blue-200")
                )

                btnList.append(btn)

        return btnList

    def get_router_root_views(self) -> dict[str, Callable[..., None]]:
        return {r["path"]: r["component"] for r in ROUTES_ROOT}

    def get_router_childrens_views(
        self, root: PATHS_ROOT
    ) -> dict[str, Callable[..., None]]:

        route = next((r for r in ROUTES_ROOT_CHILDREN if r["root"] == root), None)
        childrens = route["childrens"] if route is not None else []

        return {r["path"]: r["component"] for r in childrens}
