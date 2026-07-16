# ruff: noqa: E402
import logging
import sys

# from collections.abc import Callable
from pathlib import Path

# from typing import Any, Protocol, cast
from nicegui import app, ui

# aggiungo la cartella src al path
src_path = str(Path(__file__).parent / 'src')
if src_path not in sys.path:
	sys.path.insert(0, src_path)
print(sys.path)


# moduli locali


from src.core.logger_setup import logger_init
from src.core.paths_enum import AVATARS_STATIC_URL, Paths
from src.core.setting_setup import SettingInit
from src.database.connect import db_init
from src.main import root

# init logger
logger_init()

# init settings
settings = SettingInit()


root_logger = logging.getLogger(f'{settings.get_app_name()}')
root_logger.setLevel(logging.INFO)

root_logger.info(f'settings: {settings.get_app_name()} - {settings.get_log_filter_by_client()}')


async def do_startup():

	result = await db_init(reset=False)
	if not result:
		root_logger.error('Errore di rete o di autenticazione (DB Offline o credenziali errate)')
		exit(1)
	else:
		root_logger.info('on_startup:do_startup()......')
		root_logger.info('on_startup:Connessione al DB avvenuta con successo')


app.on_startup(do_startup)  # type: ignore


# Registrazione cartelle statiche
app.add_static_files('/public', Paths.ASSETS.value)
app.add_static_files(f'/{AVATARS_STATIC_URL}', Paths.AVATARS_DIR.value)


if __name__ in {'__main__', '__mp_main__'}:
	ui.run(  # type: ignore
		root,
		title='Nicegui learning',
		host='0.0.0.0',
		port=8080,
		reload=True,
		storage_secret=settings.get_security_secret(),
	)
