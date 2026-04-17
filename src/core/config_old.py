import json
from typing import TypedDict, Literal, NotRequired
from core.settings import SettingPaths

LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

BOOTSTRAP = "bootstrap"

class LoggingConfig(TypedDict):
    filter_by_client: bool
    log_level: LogLevel
    log_file: str


class DatabaseConfig(TypedDict):
    host: str
    port: int
    username: NotRequired[str]


class ConfigSchema(TypedDict):
    appName: str
    logging: LoggingConfig
    database: NotRequired[DatabaseConfig]


class Config:
    _defaults: ConfigSchema = {
        "appName": BOOTSTRAP,
        "logging": {
            "filter_by_client": True,
            "log_level": "INFO",
            "log_file": f"{BOOTSTRAP}.log",
        },
    }

    _config:ConfigSchema = _defaults

    @classmethod
    def load(cls):

        try:
            if not SettingPaths.CONFIG_FILE.exists():
                raise FileNotFoundError(
                    f"File di configurazione {SettingPaths.CONFIG_FILE} non trovato."
                )
            with open(SettingPaths.CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            raise Exception(e)

        cls._config = cls._defaults | data

    @classmethod
    def get_config(cls):
        return cls._config
    


