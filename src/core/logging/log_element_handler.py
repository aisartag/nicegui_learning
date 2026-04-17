import logging
from nicegui import ui
from core.config import configuration


class LogElementHandler(logging.Handler):
    """A logging handler that emits messages to a log element."""

    def __init__(self, element: ui.log, level: int = logging.NOTSET) -> None:
        self.element = element
        super().__init__(level)

    def emit(self, record: logging.LogRecord) -> None:
        try:
            msg = self.format(record)
            self.element.push(msg)
            # ui.notify(msg, position='top')

        except Exception:
            self.handleError(record)


class ClientFilter(logging.Filter):
    def __init__(self, owner_id: str):
        super().__init__()
        self.owner_id = owner_id

    def filter(self, record: logging.LogRecord) -> bool:
        # filter_by_client = config["logging"]["filter_by_client"]
        # ui.notify( f"filter_by_client: {filter_by_client}", position='top-right')
        if not configuration["logging"]["filter_by_client"]:
            return True
        try:
            return ui.context.client.id == self.owner_id
        except:
            return False
