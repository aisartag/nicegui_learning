# ruff: noqa: E402
import logging
import multiprocessing
import sys
from pathlib import Path

from nicegui import app, native, ui

# Configurazione finestra (fuori dal main)
app.native.window_args['transparent'] = True
app.native.window_args['resizable'] = True  # Esempio di altra opzione utile

# Aggiunge la cartella 'src' al percorso di ricerca di Python
src_path = str(Path(__file__).parent / 'src')
if src_path not in sys.path:
	sys.path.insert(0, src_path)

# moduli locali
from core.logger_setup import configExtra
from database.connect import db_init
from src.core.boot import bootstrap
from src.main import root

# if not bootstrap():
# 	sys.exit(1)

bootstrap()


async def do_startup():

	result = await db_init(reset=False)
	if not result:
		root_logger.error('Errore di rete o di autenticazione (DB Offline o credenziali errate)')
		sys.exit(1)

	root_logger.info('Connessione al DB avvenuta con successo')


app.on_startup(do_startup)  # type: ignore


root_logger = logging.getLogger(configExtra['root_name'])
root_logger.setLevel(logging.INFO)
root_logger.info('Inizio esecuzione')

# Registrazione cartelle statiche
# Icone, loghi
app.add_static_files('/public', str(Path(__file__).parent / 'assets'))
app.add_static_files(
	'/uploads', str(Path(__file__).parent.parent / 'data_storage/avatars')
)  # Avatar dinamici degli utenti


if __name__ in {'__main__', '__mp_main__'}:
	# if __name__ == '__main__':
	# Necessario per PyInstaller / Nuitka
	multiprocessing.freeze_support()

	# Avvio
	ui.run(  # type: ignore
		root,  # Passiamo la funzione che costruisce la UI
		native=True,
		reload=False,  # Obbligatorio per EXE
		title='Nicegui learning Native',
		port=native.find_open_port(),
		window_size=(800, 640),
		storage_secret='pizzeche',
	)
