import logging
from nicegui import ui
from core.log_loader import configExtra

class LogElementHandler(logging.Handler):
    """A logging handler that emits messages to a log element."""

    def __init__(self, element: ui.log, level: int = logging.NOTSET) -> None:
        self.element = element
        super().__init__(level)

    def emit(self, record: logging.LogRecord) -> None:
        try:
            msg = self.format(record)
            self.element.push(msg)

        except Exception:
            self.handleError(record)


class ClientFilter(logging.Filter):
    def __init__(self, owner_id: str):
        super().__init__()
        self.owner_id = owner_id

    def filter(self, record: logging.LogRecord) -> bool:
        if not configExtra["filter_by_client"]:
            return True
        try:
            return ui.context.client.id == self.owner_id
        except:
            return False