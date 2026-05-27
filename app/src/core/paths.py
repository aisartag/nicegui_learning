from pathlib import Path


class ProjectPaths:
	# Determina la root del progetto (2 livelli sopra questo file, assumendo sia in utility/paths.py)
	ROOT = Path(__file__).resolve().parent.parent.parent.parent
	APPROOT = Path(__file__).resolve().parent.parent.parent

	DATA = ROOT / 'data'
	LOGS = ROOT / 'logs'
	MODELS = ROOT / 'models'
	CONFIGS = APPROOT / 'configs'
	STATIC = APPROOT / 'static'

	@classmethod
	def ensure_dirs(cls) -> None | str:
		"""Crea tutte le cartelle di output all'avvio e verifica l'esistenza di quelle di input."""
		# Cartelle che l'app DEVE creare se mancano (OUTPUT)
		cls.LOGS.mkdir(parents=True, exist_ok=True)
		cls.DATA.mkdir(parents=True, exist_ok=True)
		cls.MODELS.mkdir(parents=True, exist_ok=True)

		# Controllo per la cartella di CONFIGURAZIONE (INPUT)
		if not cls.CONFIGS.exists():
			return f'ERRORE CRITICO: La cartella {cls.CONFIGS} non esiste!'

		if not cls.STATIC.exists():
			return f'ERRORE CRITICO: La cartella {cls.STATIC} non esiste!'

		return None


# Utilizzo nel tuo setup_logging:
if ProjectPaths.ensure_dirs() is None:
	log_path = ProjectPaths.LOGS / 'app.log'
