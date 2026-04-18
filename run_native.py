import sys
from pathlib import Path
from nicegui import app, ui, native
import multiprocessing


# Configurazione finestra (fuori dal main)
app.native.window_args["transparent"] = True
app.native.window_args["resizable"] = True # Esempio di altra opzione utile

# Aggiunge la cartella 'src' al percorso di ricerca di Python
src_path = str(Path(__file__).parent / "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from core.boot import bootstrap
from components.layouts.main_layout import layout


# Se il bootstrap fallisce, l'app non deve nemmeno provare a partire
if not bootstrap():
    sys.exit(1)


if __name__ in {"__main__", "__mp_main__"}:
    # Necessario per PyInstaller / Nuitka
    multiprocessing.freeze_support()

    # Avvio
    ui.run( # type: ignore
        layout, # Passiamo la funzione che costruisce la UI
        native=True, 
        reload=False, # Obbligatorio per EXE
        title="Unipaths Config", 
        port=native.find_open_port(), 
        window_size=(800, 640)
    ) 
