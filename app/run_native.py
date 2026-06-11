# ruff: noqa: E402

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
from src.main import root

# if __name__ in {'__main__', '__mp_main__'}:
if __name__ == '__main__':
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
