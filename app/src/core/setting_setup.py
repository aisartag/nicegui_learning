import configparser
import uuid
from typing import TypedDict

from src.core.paths_enum import Paths


class AppConfigSection(TypedDict):
	app_name: str
	log_filter_by_client: bool


class SecurityConfigSection(TypedDict):
	secret: str
	strict_mode: bool


class UserConfigSection(TypedDict):
	theme: str


class SettingConfigDict(TypedDict):
	App: AppConfigSection
	Security: SecurityConfigSection
	User: UserConfigSection


config_defaults: SettingConfigDict = {
	'App': {'app_name': 'Sight', 'log_filter_by_client': True},
	'Security': {'secret': str(uuid.uuid4()), 'strict_mode': True},
	'User': {'theme': 'auto'},
}


class SettingInit:
	def __init__(self):
		self.config = configparser.ConfigParser()
		self.config.read(Paths.CONFIG_INI_FILE.value)

		if not self.config.has_section('App.Settings'):
			self.config.add_section('App.Settings')
			for key, value in config_defaults['App'].items():
				self.config.set('App.Settings', key, str(value))
			self.config.write(open(Paths.CONFIG_INI_FILE.value, 'w'))

		if not self.config.has_section('Security.Settings'):
			self.config.add_section('Security.Settings')
			for key, value in config_defaults['Security'].items():
				self.config.set('Security.Settings', key, str(value))
			self.config.write(open(Paths.CONFIG_INI_FILE.value, 'w'))

	def get_app_name(self):
		return self.config.get('App', 'app_name', fallback=config_defaults['App']['app_name'])

	def get_log_filter_by_client(self):
		return self.config.getboolean(
			'App', 'log_filter_by_client', fallback=config_defaults['App']['log_filter_by_client']
		)

	def get_security_secret(self):
		return self.config.get('Security.Settings', 'secret', fallback=str(config_defaults['Security']['secret']))

	def get_security_strict_mode(self):
		return self.config.getboolean(
			'Security.Settings', 'strict_mode', fallback=config_defaults['Security']['strict_mode']
		)
