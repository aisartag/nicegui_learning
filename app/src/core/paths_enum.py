import os
import sys
from enum import Enum
from pathlib import Path

# ------------------------------------core---src----app
_INTERNAL_BASE_PATH = Path(__file__).resolve().parent.parent.parent
_EXTERNAL_BASE_PATH = _INTERNAL_BASE_PATH.parent


def _get_internal_base__path() -> Path:
	"""Restituisce la cartella interna (asset compressi) se compilato, o la root se in sviluppo."""
	if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
		return Path(sys._MEIPASS)  # type: ignore
	return _INTERNAL_BASE_PATH


def _get_external_runtime_path(local: bool | None = None) -> Path:
	"""Restituisce la cartella user/APPLOCALDATA o APPDATA."""
	if getattr(sys, 'frozen', False):
		if local is None:
			return Path(sys.executable).parent
		else:
			return _get_appdata_path(local)
	return _EXTERNAL_BASE_PATH


def _get_appdata_path(local: bool = False) -> Path:
	"""Restituisce la cartella in AppData (Windows) o Home (Mac/Linux)."""
	nome_app = 'DarkSight'
	if os.name == 'nt':
		var = 'LOCALAPPDATA' if local else 'APPDATA'
		base = Path(os.getenv(var, Path.home() / 'AppData' / ('Local' if local else 'Roaming')))
	else:
		base = Path.home() / ('.config' if not local else '.local/share')
	return base / nome_app


AVATARS_STATIC_URL = 'avatars'


class Paths(Enum):
	# Radici calcolate in modo pulito
	_BASE_DIR = _get_internal_base__path()
	_EXE_DIR = _get_external_runtime_path()
	_ROAMING_DIR = _get_external_runtime_path(local=False)
	_LOCAL_DIR = _get_external_runtime_path(local=True)

	# Chiavi dell'Enum
	ASSETS = 1
	LOGS = 2
	CONFIG_DIR = 3
	CONFIG_LOGGER_FILE = 4
	CONFIG_INI_FILE = 5
	DATA_STORAGE_DIR = 6
	AVATARS_DIR = 7
	APP_STORAGE_USER_DIR = 8
	WEBVIEW_CACHE_DIR = 9

	@property
	def value(self) -> Path:
		if self == Paths.ASSETS:
			return Paths._BASE_DIR.value / 'assets'

		if self == Paths.LOGS:
			path = Paths._LOCAL_DIR.value / 'logs'
			path.mkdir(parents=True, exist_ok=True)
			return path

		if self == Paths.CONFIG_DIR:
			path = Paths._ROAMING_DIR.value / 'config'
			path.mkdir(parents=True, exist_ok=True)
			return path

		if self == Paths.CONFIG_LOGGER_FILE:
			return Paths.CONFIG_DIR.value / 'logging_config.yaml'

		if self == Paths.CONFIG_INI_FILE:
			file = Paths.CONFIG_DIR.value / 'settings.ini'
			file.touch(exist_ok=True)
			return file

		if self == Paths.DATA_STORAGE_DIR:
			path = Paths._ROAMING_DIR.value / 'data_storage'
			path.mkdir(parents=True, exist_ok=True)
			return path

		if self == Paths.AVATARS_DIR:
			path = Paths.DATA_STORAGE_DIR.value / AVATARS_STATIC_URL
			path.mkdir(parents=True, exist_ok=True)
			return path

		if self == Paths.APP_STORAGE_USER_DIR:
			path = Paths._ROAMING_DIR.value / '.nicegui'
			path.mkdir(parents=True, exist_ok=True)
			return path

		if self == Paths.WEBVIEW_CACHE_DIR:
			path = Paths._LOCAL_DIR.value / 'webview_cache'
			path.mkdir(parents=True, exist_ok=True)
			return path

		return super().value
