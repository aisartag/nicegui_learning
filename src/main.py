from nicegui import ui, app
import logging
from core.log_loader import configExtra
from views.dashboard import DashboardView
from views.settings import SettingsView
from core.log_element_handler import LogElementHandler, ClientFilter
from themes.theme_manager import ThemeManager
from themes.palettes import apply_brand_theme


formatter = logging.Formatter(
    fmt="%(asctime)s - %(levelname)s - %(name)s - %(lineno)d - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


logger = logging.getLogger(f"{configExtra['root_name']}.{__name__}")
root_logger = logging.getLogger(configExtra["root_name"])



def root():
    logger.info(f"Inizio esecuzione root.{configExtra['filter_by_client']}")

    apply_brand_theme()
    manager = ThemeManager(app.storage.user)

    with ui.left_drawer().props('overlay'):
        ui.label('Overlay Drawer')

    with ui.header(elevated=True).classes(
        "bg-slate-800 text-slate-100 items-center px-4 items-center justify-between"
    ):
        with ui.row():
            ui.button(icon="menu").props("flat color=white").classes("lt-md")
        
        ui.label("MY BRAND").classes("font-bold tracking-tight")
        ui.button(icon="settings").props("flat color=white")
       
        # visible on desktop
        with ui.row().classes("gap-4  items-center  gt-sm border-1"):
            ui.label('menu 1')
            ui.label('menu 2')
        
            with ui.row().classes("gap-4 flex-items-center gt-sm"):
                ui.button(on_click=manager.cycle).props("round flat ripple").bind_icon_from(
                    manager, "icon"
                )
        # , on_click=lambda: right_drawer.toggle()
        ui.button(icon="more_vert").props(
            "flat color=white"
        ).classes("lt-md")

  
    # area outlet
    ui.sub_pages({"/": DashboardView, "/settings": SettingsView})

    # area log
    log_widget = ui.log(max_lines=50).classes("w-full h-40")
    handler = LogElementHandler(log_widget)
    handler.setFormatter(formatter)

    handler.addFilter(ClientFilter(ui.context.client.id))

    root_logger.addHandler(handler)
    ui.context.client.on_disconnect(lambda: logger.removeHandler(handler))  # type: ignore

    ui.button(
        "Log time",
        on_click=lambda: logger.warning(f"test log widget: {ui.context.client.id}"),
    )
