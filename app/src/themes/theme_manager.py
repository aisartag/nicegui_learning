import configparser
from typing import Dict, Literal, cast, get_args  #    , cast, Any, Dict, get_args

from nicegui import ui

from src.core.paths_enum import Paths

# Definiamo i valori ammessi per il tema (Literal è perfetto per Pyright Strict)
ThemeLiteral = Literal['light', 'dark', 'auto']


class ThemeManager:
	# Mappa delle icone (Material Icons di default in NiceGUI)
	ICONS: Dict[ThemeLiteral, str] = {
		'light': 'light_mode',
		'dark': 'dark_mode',
		'auto': 'settings_brightness',
	}

	# 1. Tipizziamo lo storage come PersistentDict
	def __init__(self) -> None:
		self.dark = ui.dark_mode()
		self.config = configparser.ConfigParser()
		self.config.read(Paths.CONFIG_INI_FILE.value)
		try:
			theme_mode = self.config.get('User.Settings', 'theme')
		except configparser.NoSectionError:
			theme_mode = 'auto'
			self.config.add_section('User.Settings')
			self.save_settings('User.Settings', 'theme', theme_mode)

		self.apply()

	@property
	def mode(self):
		return cast(ThemeLiteral, self.config.get('User.Settings', 'theme'))

	@mode.setter
	def mode(self, value: ThemeLiteral) -> None:
		self.save_settings('User.Settings', 'theme', value)
		self.apply()

	@property
	def icon(self) -> str:
		# Restituisce l'icona corretta in base al modo attuale
		return self.ICONS[self.mode]

	def apply(self) -> None:

		if self.mode == 'light':
			self.dark.disable()
		elif self.mode == 'dark':
			self.dark.enable()
		else:
			self.dark.auto()

	def cycle(self) -> None:
		# Ruota tra i 3 stati
		options = list(get_args(ThemeLiteral))
		current_idx = options.index(self.mode)
		next_mode = cast(ThemeLiteral, options[(current_idx + 1) % len(options)])
		self.mode = next_mode

	def save_settings(self, section: str, key: str, value: str) -> None:
		# Crea la sezione se non esiste
		if not self.config.has_section(section):
			self.config.add_section(section)

		self.config.set(section, key, value)

		self.config.write(open(Paths.CONFIG_INI_FILE.value, 'w'))
