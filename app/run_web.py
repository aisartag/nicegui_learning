# ruff: noqa: E402
import logging
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any, Protocol, cast

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


# Registrazione cartelle statiche
# Icone, loghi
app.add_static_files('/public', str(Path(__file__).parent / 'assets'))
app.add_static_files(
	'/uploads', str(Path(__file__).parent.parent / 'data_storage/avatars')
)  # Avatar dinamici degli utenti


# from starlette.middleware.sessions import SessionMiddleware

# # 1. Recuperi la chiave dall'ambiente Docker (o usi un fallback locale)
# CHIAVE_SEGRETA = os.environ.get('MY_APP_SECRET', 'pizzeche')

# # 2. Configuri il middleware con la chiave e forzi la scadenza alla chiusura della scheda
# app.add_middleware(SessionMiddleware, secret_key=CHIAVE_SEGRETA, max_age=None)
# root_logger.info(f'secret_key.{CHIAVE_SEGRETA}')


class NiceGuiRunCallable(Protocol):
	def __call__(
		self: Callable[..., Any],
		*,
		native: bool = ...,
		title: str = ...,
		reload: bool = ...,
		port: int = ...,
		host: str = ...,
		storage_secret: str = ...,
	) -> None: ...


run_app = cast(NiceGuiRunCallable, ui.run)  # type: ignore[reportUnknownMemberType]


if __name__ in {'__main__', '__mp_main__'}:
	run_app(  # type: ignore
		root,
		title='Nicegui learning',
		host='0.0.0.0',
		port=8080,
		reload=True,
		storage_secret='pizzeche',
	)
