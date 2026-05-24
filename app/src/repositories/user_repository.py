import logging

from core.log_loader import configExtra
from models.user import User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(f'{configExtra["root_name"]}.{__name__}')


class UserRepository:
	def __init__(self, session: AsyncSession):
		self.session = session  # Riceve la sessione iniettata dal Service

	async def get_by_email(self, email: str) -> User | None:
		"""Cerca un utente tramite email (Asincrono)."""
		# In SQLAlchemy 2.0 asincrono si usa 'select' e poi 'scalars().first()'

		return await self.session.scalar(select(User).where(User.email == email))

		# ALTERNATIVA####################################
		# query = select(User).where(User.email == email)
		# result = await self.session.execute(query)
		# return result.scalars().first()

	async def get_by_name(self, username: str) -> User | None:
		"""Cerca un utente tramite usrname (Asincrono)."""
		return await self.session.scalar(select(User).where(User.username == username))

	async def create(self, username: str, email: str, password_hash: str) -> User:
		"""Crea l'istanza dell'utente ed esegue il flush per ottenere l'ID."""
		new_user = User(username=username, email=email, password=password_hash)

		# 1. Aggiunge l'oggetto alla sessione (in memoria)
		self.session.add(new_user)

		# 2. IL TRUCCO CHIAVE: il flush invia i dati al database IMMEDIATAMENTE.
		# Postgres genera l'ID autoincrementale, ma non chiude la transazione.
		await self.session.flush()

		# Ora 'new_user.id' è popolato e pronto per essere usato dal profilo!
		return new_user
