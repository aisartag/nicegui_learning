from nicegui import ui, app
import logging

from components.layout_master import MasterLayout
from core.log_loader import configExtra
from core.log_element_handler import LogElementHandler, ClientFilter

# from components.layout import Layout
# from routing.route_childrens import ChildrenRegistry
# from routing.route_master import MasterRoute

app.colors(
    primary="#5898d4",
    secondary="#26a69a",
    accent="#9c27b0",
    dark="#1d1d1d",
    dark_page="#121212",
    positive="#21ba45",
    negative="#c10015",
    info="#31ccec",
    warning="#f2c037",
)


formatter = logging.Formatter(
    fmt="%(asctime)s - %(levelname)s - %(name)s - %(lineno)d - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


logger = logging.getLogger(f"{configExtra['root_name']}.{__name__}")
root_logger = logging.getLogger(configExtra["root_name"])


async def root():

    # await client.connected()

    logger.info(
        f"Root avviato - log filter_by_client:{configExtra['filter_by_client']}"
    )

    logger.info(f"Inizio esecuzione root.{configExtra['filter_by_client']}")

    MasterLayout()

    # area log
    # with ui.expansion(value=True).classes("w-full h-full"):
    log_widget = ui.log(max_lines=100).classes("w-full h-40")
    handler = LogElementHandler(log_widget)
    handler.setFormatter(formatter)

    handler.addFilter(ClientFilter(ui.context.client.id))

    root_logger.addHandler(handler)
    ui.context.client.on_disconnect(lambda: logger.removeHandler(handler))  # type: ignore

    ui.button(
        "Log time",
        on_click=lambda: logger.warning(f"test log widget: {ui.context.client.id}"),
    )
