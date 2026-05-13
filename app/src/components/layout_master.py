from nicegui import Client, ui, app
import logging

from components.layout_widgets import WidgetsLayout
from routing.route_master import MasterRoute
from themes.theme_manager import ThemeManager

from core.log_loader import configExtra
from utils.screen_state_old import ScreenState

from routing.route_events import childrens_emitted

logger = logging.getLogger(f"{configExtra['root_name']}.{__name__}")


class MasterLayout:
    def __init__(self) -> None:

        self.client: Client = ui.context.client

        # apply_brand_theme()
        self.theme_manager = ThemeManager(app.storage.user)

        self.is_mobile = False
        self.has_childrens = False
        self.screen_state = ScreenState(self.updated_is_mobile)

        self.current_path = self.client.request.url.path

        self.drawer: ui.left_drawer = (
            ui.left_drawer(value=False)
            .props("bordered")
            .classes("bg-slate-100 dark:bg-slate-900")
        )
        self.header: ui.header = ui.header(elevated=True)

        self.theme_manager = ThemeManager(app.storage.user)

        self.setup_ui()

        # ascolta i cambiamenti di childrens (dal routing)
        childrens_emitted.subscribe(self.handle_new_childrens)

        # not ui elements rendered here
        self.setup_routing()

    def setup_ui(self):
        """renderizza il layout  header e drawer"""
        self.header.classes(
            "items-center px-4 items-center justify-between bg-slate-100 text-slate-800 dark:bg-slate-900  dark:text-blue-200 border-b-2"
        )
        with self.header:
            #  menu hamburger
            self.hamburger = (
                ui.button(icon="menu", on_click=lambda: self.drawer.toggle())
                .props("round flat ripple")
                .classes("lt-md text-blue-800 dark:text-blue-800 dark:text-blue-200")
            )

           

            # brand
            with ui.row().classes("gt-sm items-center tracking-tight"):
                ui.link(f"Nicegui Learning", "/").classes(
                    "font-semibold px-4 py-2 no-underline text-xl text-blue-800 dark:text-blue-200"
                )

            with ui.row().classes("items-center flex-1 justify-center tracking-tight"):
                self.screen_changed() 
           

            

            with ui.row().classes("items-center gt-sm tracking-tight"):
                WidgetsLayout.render_menu_master_as_buttons()

                # toggle dark mode
                ui.button(on_click=self.theme_manager.cycle).bind_icon_from(
                    self.theme_manager, "icon"
                ).props("round ripple flat").classes("text-blue-800 dark:text-blue-200")

            WidgetsLayout.render_menu_as_dropdown(self.theme_manager)

        with ui.column().classes(
            "w-full min-h-[calc(100vh-384px)] border-2 border-blue-600 items-center justify-start bg-slate-100 dark:bg-slate-800"
        ):
            ui.label("Main Content Area").classes("m-2 font-bold text-xl")
            ui.sub_pages(MasterRoute.as_nicegui_dict())

        with self.drawer:
            ui.label("Menu di navigazione")
    
    
    @ui.refreshable_method
    def screen_changed(self) -> None:
        ui.icon(
            name=("s_mobile_friendly" if self.is_mobile else "s_desktop_windows"),
            color="primary",
        ).classes("text-2xl")

    def setup_routing(self):
        """
        setup routing e subscribe al emitter childrens_emitted"""

        # attiva listener per i cambiamenti di path e aggiorna la route
        logger.info(f"MasterRoute.setup call current_path: {self.current_path}")
        MasterRoute.setup(self.current_path)

    def handle_new_childrens(self, childrens: list[dict[str, str]] | None):
        """
        aggiorna lo stato dello schermo mobile (callback da ScreenState)"""

        logger.info(f"handle_new_childrens: {childrens} - {self.client.id}")
        if childrens is None:
            return

        self.has_childrens = len(childrens) > 0

        self.drawer.clear()

        if self.has_childrens:
            with self.drawer:
                WidgetsLayout.render_menu_for_childrens_as_buttons(childrens, self.drawer.toggle)

        self.updated_is_mobile(self.is_mobile)
      
    def updated_is_mobile(self, is_mobile: bool):
        """
        # aggiorna lo stato dello schermo mobile (callback da ScreenState)"""
        self.is_mobile = is_mobile
        # logger.info(f"updated_is_mobile: {self.is_mobile}-{self.client.id}")

        if self.is_mobile:
            self.drawer.props("behavior=mobile")
        else:
            self.drawer.props("behavior=desktop")

        # self.drawer.value = False
        self.drawer.value = False if self.is_mobile else self.has_childrens
        self.hamburger.set_visibility(self.has_childrens)
        
        self.screen_changed.refresh()
        WidgetsLayout.set_mobile(self.is_mobile)