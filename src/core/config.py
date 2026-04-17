import os
from typing import Literal, NotRequired, TypedDict
from dotenv import load_dotenv
from pathlib import Path

LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


class LoggingConfig(TypedDict):
    filter_by_client: bool
    log_level: LogLevel
    log_file: str


class DatabaseConfig(TypedDict):
    host: str
    port: int
    db: str
    user: NotRequired[str]
    password: NotRequired[str]


class ConfigSchema(TypedDict):
    appName: str
    logging: LoggingConfig
    database: NotRequired[DatabaseConfig]


env_path = Path(".") / ".env"
print(env_path)
load_dotenv(dotenv_path=env_path)

# appname = os.getenv("APPNAME", "nicegui_logger")
# print(appname)

configuration: ConfigSchema = {
    "appName": os.getenv("APPNAME", "nicegui"),
    "logging": {
        "filter_by_client": True,
        "log_level": "INFO",
        "log_file": f"{os.getenv('APPNAME', 'nicegui')}.log",
    },
}

print(configuration)