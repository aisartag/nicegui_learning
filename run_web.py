import sys
from pathlib import Path
from nicegui import ui


# Aggiunge la cartella 'src' al percorso di ricerca di Python
# ovvero il sys.path.insert(0....) 0 in testa
src_path = str(Path(__file__).parent / "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from core.boot import bootstrap
from components.layouts.main_layout import layout


# Se il bootstrap fallisce, l'app non deve nemmeno provare a partire
if not bootstrap():
    sys.exit(1)




layout()

ui.run(layout, port=8080, title="My App Web")  # type: ignore
