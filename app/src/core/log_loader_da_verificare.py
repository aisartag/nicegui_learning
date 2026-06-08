import logging.config
import os

import yaml


def setup_logging():
	# Rileva l'ambiente dal Docker Compose (default: development)
	env = os.getenv('ENV', 'development')
	config_path = 'app/logging_config.yaml'

	if os.path.exists(config_path):
		with open(config_path, 'r') as f:
			config = yaml.safe_load(f)

		# 🧠 LOGICA JEDI: Modifica i log in base all'ambiente senza toccare il file fisico
		if env == 'production':
			# In produzione: zittiamo SQLAlchemy e alziamo il livello generale
			config['root']['level'] = 'WARNING'
			if 'sqlalchemy.engine' in config['loggers']:
				config['loggers']['sqlalchemy.engine']['level'] = 'WARNING'
		else:
			# In sviluppo: lasciamo INFO o DEBUG per vedere le query SQL
			config['root']['level'] = 'INFO'
			if 'sqlalchemy.engine' in config['loggers']:
				config['loggers']['sqlalchemy.engine']['level'] = 'INFO'

		# Applica la configurazione modificata al volo
		logging.config.dictConfig(config)
	else:
		logging.basicConfig(level=logging.INFO)


# Inizializza i log prima di qualsiasi altra operazione
setup_logging()


# Ti conviene modificare il percorso nel file YAML in filename: "logs/placeholder.log" (o come l'ho rinominato io logs/sight.log).
#  In questo modo i file di log scritti dal container verranno salvati direttamente
# nella cartella ./logs del tuo computer reale, permettendoti di leggerli comodamente
# senza entrare nel container!Se provi a lanciare docker compose up --build con questa modifica,
#  noti che le query di SQLAlchemy continuano a comparire o il terminale si è finalmente stabilizzato mostrando solo le informazioni essenziali?
