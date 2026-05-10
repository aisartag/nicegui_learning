import sys
from pathlib import Path
from nicegui import ui
import logging


# aggiungo la cartella src al path
src_path = str(Path(__file__).parent / "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)
print(sys.path)

# moduli locali
from src.core.log_loader import configExtra
from src.core.boot import bootstrap
from src.main import root

if not bootstrap():
    sys.exit(1)

root_logger = logging.getLogger(configExtra["root_name"])
root_logger.setLevel(logging.INFO)
root_logger.info("Inizio esecuzione")


if __name__ in {"__main__", "__mp_main__"}:
    ui.run(root, title="Nicegui learning", host="0.0.0.0", port=8080, reload=True, storage_secret="pizzeche")  # type: ignore

