# ruff: noqa: E402

import logging
import multiprocessing
import os
import sys
from pathlib import Path

from nicegui import app, native, ui

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


root_logger = logging.getLogger(f'{settings.get_app_name()}.{__name__}')
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


# Imposta la dimensione della finestra
app.native.window_args['width'] = 900
app.native.window_args['height'] = 640
app.native.window_args['transparent'] = True  # Imposta la finestra come trasparente
app.native.window_args['resizable'] = True  # Imposta la finestra come ridimensionabile

# Imposta reload=False per la compilazione
if __name__ == '__main__':
	multiprocessing.freeze_support()  # first statement in main guard

	os.environ['NICEGUI_STORAGE_PATH'] = str(Paths.APP_STORAGE_USER_DIR.value)

	# 1. Configura pywebview per NON cancellare i cookie alla chiusura
	app.native.start_args['private_mode'] = False

	app.native.start_args['storage_path'] = str(Paths.WEBVIEW_CACHE_DIR.value)

	ui.run(  # type: ignore
		root,
		native=True,
		reload=False,
		title='Nicegui learning Native',
		port=native.find_open_port(),
		storage_secret=settings.get_security_secret(),
	)
