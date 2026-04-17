from nicegui import ui
import logging
from logging import Logger
from logging.handlers import RotatingFileHandler
from core.config import configuration
from core.logging.log_element_handler import LogElementHandler,ClientFilter


class LoggerSettings:
    _logger: Logger = logging.getLogger(configuration["appName"])
    _logger.setLevel(configuration["logging"]["log_level"])
    _formatter = logging.Formatter(
        "%(asctime)s - %(name)s - [%(levelname)s] - %(message)s",
        "%Y-%m-%d %H:%M:%S",
    )

    @classmethod
    def setup(cls):

        if not cls._logger.handlers:
            log_file = configuration["logging"]["log_file"]
            fh = RotatingFileHandler(
                log_file,
                maxBytes=5 * 1024 * 1024,
                backupCount=3,
                encoding="utf-8",
            )

            ch = logging.StreamHandler()

            fh.setFormatter(cls._formatter)
            ch.setFormatter(cls._formatter)

            cls._logger.addHandler(fh)  # Scrive su file
            cls._logger.addHandler(ch)

        cls._logger.info("LoggerSettings completato con successo!")
        return cls._logger

    @classmethod
    def setup_ui_logging(cls, log_element: ui.log) -> None:  # logging.Handler:
        """
        Incapsula la creazione dell'handler, l'aggiunta del filtro
        e il collegamento al logger globale.
        """
        # 1. Crea l'handler collegato all'elemento UI
        handler = LogElementHandler(log_element)
        

        ui_formatter = logging.Formatter("[%(levelname)s] %(name)15s: %(message)s")
        handler.setFormatter(ui_formatter)

        # 2. Configura il livello e il filtro
        client_id = ui.context.client.id
        handler.addFilter(ClientFilter(client_id))

        # 3. Collega al logger (es. quello di root o uno specifico)
        cls._logger.addHandler(handler)

        # 4. Gestisce automaticamente la rimozione quando il client chiude la tab
        ui.context.client.on_disconnect(lambda: cls._logger.removeHandler(handler))  # type: ignore

        # return handler
