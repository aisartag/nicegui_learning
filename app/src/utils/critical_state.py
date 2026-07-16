import asyncio
import logging

from nicegui import app, ui

logger = logging.getLogger(__name__)


async def secure_shutdown():
	# 1. Mostra un avviso visivo all'utente (rimarrà visibile sulla pagina "congelata")
	ui.notify('Il server si sta spegnendo a causa di un errore critico...', type='negative', close_button=True)

	# 2. Registra l'errore nel logger
	logger.error('Errore critico rilevato: avvio dello shutdown del sistema.=====================')

	# 3. Forza il logger a scrivere immediatamente i dati su disco/terminale
	for handler in logging.getLogger().handlers:
		handler.flush()

	# 4. Attendi un brevissimo istante per assicurarsi che i pacchetti WebSocket e i log siano partiti
	await asyncio.sleep(1)

	# 5. Spegni l'applicazione in modo pulito
	app.shutdown()
