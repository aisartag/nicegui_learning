import logging
from typing import Any

from core.log_loader import configExtra
from models.user import User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

logger = logging.getLogger(f'{configExtra["root_name"]}.{__name__}')


class UserRepository:
	def __init__(self, session: AsyncSession):
		self.session = session  # Riceve la sessione iniettata dal Service

	async def get_user_with_profile_by_email(self, email: str) -> User | None:
		"""Cerca un utente tramite email (Asincrono)."""
		return await self.session.scalar(select(User).options(joinedload(User.profile)).where(User.email == email))

	async def get_user_by_email(self, email: str) -> User | None:
		"""Cerca un utente tramite email (Asincrono)."""
		return await self.session.scalar(select(User).where(User.email == email))

	async def get_user_by_name(self, username: str) -> User | None:
		"""Cerca un utente tramite usrname (Asincrono)."""
		return await self.session.scalar(select(User).where(User.username == username))

	async def create(self, username: str, email: str, password_hash: str) -> User:
		"""Crea l'istanza dell'utente ed esegue il flush per ottenere l'ID."""
		new_user = User(username=username, email=email, password=password_hash)

		# 1. Aggiunge l'oggetto alla sessione (in memoria)
		self.session.add(new_user)

		# Ora 'new_user.id' è popolato e pronto per essere usato dal profilo!
		return new_user

	async def get_user_with_profile(self, user_id: int) -> User | None:
		"""Cerca un utente tramite ID (Asincrono) compreso il profilo."""
		user = await self.session.scalar(select(User).options(joinedload(User.profile)).where(User.id == user_id))
		return user

	async def get_user(self, user_id: int) -> Any:
		"""Cerca un utente tramite ID (Asincrono)."""
		user = await self.session.scalar(select(User).where(User.id == user_id))
		return user
