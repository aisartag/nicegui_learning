from collections.abc import Callable
from typing import List, cast, get_args
from nicegui import ui, Client, background_tasks, app

from components.select_theme import theme_choice
from themes.palettes import apply_brand_theme
from themes.theme_manager import ThemeManager

# from routing import ROUTES, main_lnk_links
# from routing.routing_builder import RoutingBuilder, TypedRouteLink
# from routing_schema.schema import TypedRoute, ROUTES_SCHEMA

from routing.main_root import ROUTES_ROOT
from routing.paths_type import PATHS_ROOT
from routing.root_children import ROUTES_ROOT_CHILDREN


class Layout:
    def __init__(self):

        self.client: Client = ui.context.client

        apply_brand_theme()
        self.toggle_mode = ThemeManager(app.storage.user)

        with ui.header(elevated=True).classes(
            "items-center px-4 items-center justify-between"
        ):

            #  menu hamburger
            self.hamburger = (
                ui.button(icon="menu", on_click=lambda: self.drawer.toggle())
                .props("round flat color=white ripple")
                .classes("lt-md")
            )

            # brand
            ui.link("Nicegui 3.13.13", "/").classes(
                "font-bold tracking-tight px-6 py-3 text-blue-100 no-underline rounded hover:bg-blue-600 hover:underline hover:text-blue-200"
            )

            with ui.row().classes("gap-4 items-center gt-sm tracking-tight"):
                self.get_router_root_links()

                # toggle dark mode
                ui.button(on_click=self.toggle_mode.cycle).props(
                    "round flat  ripple"
                ).bind_icon_from(self.toggle_mode, "icon")

            with ui.dialog().props("position=right") as dialog:

                def handle_click(path: str):
                    ui.navigate.to(path)
                    dialog.close()

                with ui.card().classes(
                    "absolute-right h-[calc(100vh-128px)] m-2 mr-1  w-64 items-start"
                ):
                    with ui.row().classes("w-full"):
                        ui.button(icon="close", on_click=dialog.close).props(
                            "round flat color=white ripple"
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
                        theme_choice(self.toggle_mode)



            ui.button(icon="more_vert", on_click=dialog.open).props(
                "round flat color=white ripple"
            ).classes("lt-md")

        self.drawer = (
            ui.left_drawer(value=False)
            .props("permanent")
            
        )
        with self.drawer:
            ui.label("Menu di navigazione")

        with ui.column().classes("w-full min-h-[calc(100vh-384px)] border-2 border-blue-600 items-center justify-start"):
            ui.label("Main Content Area")
            ui.sub_pages(self.get_router_root_views())

        self.handle_path_change(self.get_root_path(self.client.request.url.path))

        self.client.sub_pages_router.on_path_changed(
            lambda path: self.handle_path_change(path)
        )

    def get_root_path(self, path: str) -> str:

        parts = path.strip("/").split("/")
        return f"/{parts[0]}" if parts[0] else "/"

    def handle_path_change(self, path: str):

        # verifica che sia una chiave di ROUTES_ROOT
        
        if path not in get_args(PATHS_ROOT):
            return

        route = next((r for r in ROUTES_ROOT_CHILDREN if r["root"] == path), None)
        childrens = route["childrens"] if route is not None else []

        self.drawer.clear()
        if len(childrens) > 0:
            with self.drawer:
                with ui.column().classes("w-full"):
                    for children in childrens:
                        ui.link(children["label"], path + children["path"]).classes(
                            "px-6 py-3 text-blue-100 no-underline rounded hover:bg-blue-600 hover:underline hover:text-blue-200"
                        )

        async def check_logic():
            with self.client:
                width = cast(int, await ui.run_javascript("window.innerWidth"))

                self.drawer.value = False if width < 1024 else len(childrens) > 0
                self.hamburger.set_visibility(len(childrens) > 0)

        background_tasks.create(check_logic())  # type: ignore

    def get_router_root_links(self):

        lnkList: List[ui.link] = []
        for link in ROUTES_ROOT:
            if link["path"] != "/":
                lnk = ui.link(link["label"], link["path"]).classes(
                    "px-6 py-3 no-underline rounded hover:bg-blue-600 hover:underline hover:text-blue-200"
                )
#  text-blue-100
                lnkList.append(lnk)

        # ui.notify(f"Links in main_lnk_links: {lnkList}")
        return lnkList

    def get_router_root_views(self) -> dict[str, Callable[..., None]]:
        return {r["path"]: r["component"] for r in ROUTES_ROOT}

    def get_router_childrens_views(
        self, root: PATHS_ROOT
    ) -> dict[str, Callable[..., None]]:

        route = next((r for r in ROUTES_ROOT_CHILDREN if r["root"] == root), None)
        childrens = route["childrens"] if route is not None else []

        return {r["path"]: r["component"] for r in childrens}
