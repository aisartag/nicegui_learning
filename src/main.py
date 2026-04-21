from nicegui import ui
import logging
from core.log_loader import configExtra
from views.dashboard import DashboardView
from views.settings import SettingsView
from core.log_element_handler import LogElementHandler, ClientFilter

formatter = logging.Formatter(
    fmt="%(asctime)s - %(levelname)s - %(name)s - %(lineno)d - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


logger = logging.getLogger(f"{configExtra['root_name']}.{__name__}")
root_logger = logging.getLogger(configExtra["root_name"])


def root():
    logger.info(f"Inizio esecuzione root.{configExtra['filter_by_client']}")

    with ui.header(elevated=True).classes(
        "bg-slate-800 text-slate-100 items-center px-4 items-center justify-between"
    ):
        ui.label("Nicegui 3.13.13").classes("font-bold tracking-tight")

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
