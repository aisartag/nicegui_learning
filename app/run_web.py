# ruff: noqa: E402
import logging
import sys
from pathlib import Path

from nicegui import app, ui

# aggiungo la cartella src al path
src_path = str(Path(__file__).parent / 'src')
if src_path not in sys.path:
	sys.path.insert(0, src_path)
print(sys.path)


# moduli locali
from database.connect import do_connection
from src.core.boot import bootstrap
from src.core.log_loader import configExtra
from src.main import root

if not bootstrap():
	sys.exit(1)


async def do_startup():

	result = await do_connection(reset=False)
	if not result:
		root_logger.error('Errore di rete o di autenticazione (DB Offline o credenziali errate)')
		exit(1)

	root_logger.info('Connessione al DB avvenuta con successo')


app.on_startup(do_startup)  # type: ignore


root_logger = logging.getLogger(configExtra['root_name'])
root_logger.setLevel(logging.INFO)
root_logger.info('Inizio esecuzione')


if __name__ in {'__main__', '__mp_main__'}:
	ui.run(  # type: ignore
		root,
		title='Nicegui learning',
		host='0.0.0.0',
		port=8080,
		reload=True,
		storage_secret='pizzeche',
	)
