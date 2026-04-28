from nicegui import ui
import logging
from core.log_loader import configExtra
from core.log_element_handler import LogElementHandler, ClientFilter

from layout import Layout




formatter = logging.Formatter(
    fmt="%(asctime)s - %(levelname)s - %(name)s - %(lineno)d - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


logger = logging.getLogger(f"{configExtra['root_name']}.{__name__}")
root_logger = logging.getLogger(configExtra["root_name"])


async def root():

    logger.info(f"Root avviato - log filter_by_client:{configExtra['filter_by_client']}")

    layout = Layout()

   
    ui.sub_pages(layout.get_router_root_views())
   


    # on path changed
    ui.context.client.sub_pages_router.on_path_changed(
        lambda path: layout.handle_path_change(path)
    )

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

    