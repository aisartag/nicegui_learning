import logging
from types import TracebackType
from typing import Type

from core.log_loader import configExtra
from database.engine import AsyncSessionLocal

# Assumiamo che tu abbia un ProfileRepository simile
from repositories.profile_repository import ProfileRepository
from repositories.user_repository import UserRepository

logger = logging.getLogger(f'{configExtra["root_name"]}.{__name__}')


class UnitOfWork:
	def __init__(self):
		# Manteniamo il riferimento alla fabbrica di sessioni globali
		self.session_factory = AsyncSessionLocal
		self.session = None
		users: UserRepository  # pyright: ignore[reportUnusedVariable] # noqa: F842
		profiles: ProfileRepository  # pyright: ignore[reportUnusedVariable] # noqa: F842

	async def __aenter__(self):
		"""Scatta all'apertura del blocco 'async with UnitOfWork() as uow:'"""
		# 1. Apre la sessione isolata per questa specifica richiesta/clic
		self.session = self.session_factory()

		# 2. Istanzia i repository passandogli la STESSA sessione
		# In questo modo condividono la medesima transazione atomica
		self.users = UserRepository(self.session)
		self.profiles = ProfileRepository(self.session)

		return self

	async def __aexit__(
		self, exc_type: Type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None
	):
		"""Scatta automaticamente all'uscita del blocco 'async with'"""

		# Se self.session è None per qualche motivo assurdo, non facciamo nulla
		if self.session is None:
			return

		try:
			if exc_type is not None:
				# Se il codice ha sollevato un'eccezione, annulla tutto (Rollback)
				logger.warning(f"Eccezione rilevata nell'UoW ({exc_type.__name__}): eseguo il rollback.")
				await self.session.rollback()
			else:
				# Se tutto è andato bene, salva definitivamente sul DB (Commit)
				logger.info("Nessun errore nell'UoW: eseguo il commit finale.")
				await self.session.commit()
		except Exception as e:
			logger.error(f"Errore durante la chiusura della transazione nell'UoW: {e}")
			await self.session.rollback()
			raise
		finally:
			# Chiude SEMPRE la sessione rilasciando la connessione al pool
			await self.session.close()
