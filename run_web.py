import sys
from pathlib import Path
from  nicegui import ui
   


# Aggiunge la cartella 'src' al percorso di ricerca di Python
# ovvero il sys.path.insert(0....) 0 in testa
src_path = str(Path(__file__).parent / "src" )
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from core.boot import bootstrap
from core.logger.logset import LoggerSettings
from core.config import Config
from components.layouts.main_layout import layout

# Se il bootstrap fallisce, l'app non deve nemmeno provare a partire
if not bootstrap():
    sys.exit(1)



def build_ui():
    
    
    Config().load()

    logger = LoggerSettings().setup()
    logger.info(f"Inizio build_ui: {logger.name}")

    layout(logger)


ui.run(build_ui, port=8080, title="My App Web")  # type: ignore