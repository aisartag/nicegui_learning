import os
from typing import TypedDict, List, Dict, Optional


class ConfigExtra(TypedDict):
    root_name:str
    filter_by_client: bool
    max_ui_lines: int


class FormatterConfig(TypedDict):
    format: str
    datefmt: Optional[str]


class HandlerConfig(TypedDict, total=False):
    # total=False perché le chiavi cambiano tra StreamHandler e FileHandler
    class_: str  # Nota: 'class' è parola riservata, logging usa 'class' o '()'
    formatter: str
    level: str
    filename: str
    maxBytes: int
    backupCount: int
    encoding: str
    stream: str


class LoggerConfig(TypedDict, total=False):
    level: str
    handlers: List[str]
    propagate: bool


class LoggingConfigDict(TypedDict):
    version: int
    disable_existing_loggers: bool
    config_extra: ConfigExtra  # Il tuo strapuntino tipizzato
    formatters: Dict[str, FormatterConfig]
    handlers: Dict[str, HandlerConfig]
    root: LoggerConfig
    loggers: Dict[str, LoggerConfig]


configExtra: ConfigExtra = {"root_name": "sight", "filter_by_client": True, "max_ui_lines": 100}




# Esempio di utilizzo nel setup
def setup_logging() -> None | str:
    import yaml
    import logging.config
    from core.paths import ProjectPaths

    # 1. Assicurati che le cartelle esistano
    # ProjectPaths.ensure_dirs()

    config_path = ProjectPaths.CONFIGS / "logging_config.yaml"
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            try:
                config: LoggingConfigDict = yaml.safe_load(f)
                log_full_path = str(ProjectPaths.LOGS / "app.log")
                config["handlers"]["file"]["filename"] = log_full_path
          
                configExtra.update(config.get("config_extra", {}))
                # Se devi rinominare 'class_' in 'class' per dictConfig (che lo richiede così)
                # puoi farlo qui se necessario, o usare '()' nel YAML che è un alias sicuro.
                logging.config.dictConfig(config)  # type: ignore

                return None

            except Exception as e:
                return f"Errore nella configurazione del logging: {e}"
    else:
        # Fallback se il file manca
        return f"{config_path} non trovato!" 


