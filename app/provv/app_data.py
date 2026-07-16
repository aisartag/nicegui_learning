import sys
from pathlib import Path


def get_internal_path(relative_path: str):
	if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
		return Path(sys._MEIPASS) / relative_path  # type: ignore
	return Path(__file__).parent / relative_path


def get_external_runtime_path():
	if getattr(sys, 'frozen', False):
		return Path(sys.executable).parent
	return Path(__file__).parent
