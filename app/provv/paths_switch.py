import os
import sys
from pathlib import Path

from platformdirs import user_config_dir, user_data_dir, user_log_dir


class PathSwitch:
	BASE_DIR = Path(__file__).parent

	@classmethod
	def get_internal_path(cls, relative_path: str):
		"""la posizione delle risorse interne dipende se siamo in ambiente native o in ambiente web"""
		if hasattr(sys, '_MEIPASS'):
			return Path(sys._MEIPASS) / relative_path  # type: ignore
		return Path(__file__).parent / relative_path

	@classmethod
	def get_external_runtime_path(cls):
		if getattr(sys, 'frozen', False):
			return Path(sys.executable).parent
		return Path(__file__).parent

	@classmethod
	def get_user_data_dir(cls):
		return user_data_dir('nicegui_learning', 'DarkSight', roaming=True)

	@classmethod
	def get_user_log_dir(cls):
		return user_log_dir('nicegui_learning', 'DarkSight')
		return Path(__file__).parent


if __name__ == '__main__':
	print(f'PathSwitch.get_user_data_dir() : {PathSwitch.get_user_data_dir()}')
	print(f'PathSwitch.get_user_log_dir() : {PathSwitch.get_user_log_dir()}')
	print(f'APPDATA: {os.environ["APPDATA"]}')
	print(f'user_config_dir: {user_config_dir("nicegui_learning", roaming=True)}')
