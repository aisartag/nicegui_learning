import logging.config
import os
from typing import Dict, List, Optional, TypedDict

import yaml
from core.paths_enum import Paths


class ConfigExtra(TypedDict):
	root_name: str
	filter_by_client: bool
	max_ui_lines: int


class FormatterConfig(TypedDict):
	format: str
	datefmt: Optional[str]


class HandlerConfig(TypedDict, total=False):
	# total=False perché le chiavi cambiano tra StreamHandler e FileHandler
	class_: str  # Nota: 'class' è parola riservata, logging usa 'class' o '()'
	formatter: str
	level: str
	filename: str
	maxBytes: int
	backupCount: int
	encoding: str
	stream: str


class LoggerConfig(TypedDict, total=False):
	level: str
	handlers: List[str]
	propagate: bool


class LoggingConfigDict(TypedDict):
	version: int
	disable_existing_loggers: bool
	config_extra: ConfigExtra  # Il tuo strapuntino tipizzato
	formatters: Dict[str, FormatterConfig]
	handlers: Dict[str, HandlerConfig]
	root: LoggerConfig
	loggers: Dict[str, LoggerConfig]


# Esempio di utilizzo nel setup
def logger_init() -> None | str:

	if os.path.exists(Paths.CONFIG_LOGGER_FILE.value):
		with open(Paths.CONFIG_LOGGER_FILE.value, 'r') as f:
			try:
				config: LoggingConfigDict = yaml.safe_load(f)
				log_full_path = str(Paths.LOGS.value / 'sight.log')
				config['handlers']['file']['filename'] = log_full_path

				# Se devi rinominare 'class_' in 'class' per dictConfig (che lo richiede così)
				# puoi farlo qui se necessario, o usare '()' nel YAML che è un alias sicuro.
				logging.config.dictConfig(config)  # type: ignore
				return None

			except Exception as e:
				logging.basicConfig(level=logging.INFO)
				logging.warning(f'Errore nella configurazione del logger: {e}')
	else:
		# Fallback se il file manca
		logging.basicConfig(level=logging.INFO)
		logging.warning(f'Errore il file di configurazione del logger: {Paths.CONFIG_LOGGER_FILE.value} non trovato.')
