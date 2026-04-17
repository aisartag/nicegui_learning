from nicegui import ui
import logging
from logging import Logger
from logging.handlers import RotatingFileHandler
from core.config import Config, BOOTSTRAP
from core.logger.log_element_handler import LogElementHandler, ClientFilter


class LoggerSettings:
    _logger: Logger = logging.getLogger(BOOTSTRAP)
    _logger.setLevel("INFO")
    _formatter = logging.Formatter(
        "%(asctime)s - %(name)s - [%(levelname)s] - %(message)s",
        "%Y-%m-%d %H:%M:%S",
    )

    @classmethod
    def setup(cls):

        config = Config.get_config()
        new_name = config["appName"]

        # if new_name != BOOTSTRAP:
        cls._logger = logging.getLogger(config["appName"])
        cls._logger.setLevel(config["logging"]["log_level"])

        # Se stiamo passando dal logger di emergenza a quello reale
        if cls._logger.name != new_name:
            # 1. Chiudiamo e rimuoviamo gli handler dal vecchio logger (bootstrap)
            for handler in cls._logger.handlers[:]:
                handler.close()
                cls._logger.removeHandler(handler)

            # 2. Cambiamo il riferimento al nuovo logger (quello definitivo)
            cls._logger = logging.getLogger(new_name)

        if not cls._logger.handlers:
            log_file = config["logging"]["log_file"]
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
        config = Config.get_config()
        handler.setLevel(config["logging"]["log_level"])
        client_id = ui.context.client.id
        handler.addFilter(ClientFilter(client_id))

        # 3. Collega al logger (es. quello di root o uno specifico)
        cls._logger.addHandler(handler)

        # 4. Gestisce automaticamente la rimozione quando il client chiude la tab
        ui.context.client.on_disconnect(lambda: cls._logger.removeHandler(handler))  # type: ignore

        # return handler
