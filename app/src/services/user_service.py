import logging

from core.log_loader import configExtra
from models.user import User
from repositories.profile_repository import ProfileRepository
from repositories.user_repository import UserRepository
from services.crypto_service import CryptoService  # Nuovo import
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(f'{configExtra["root_name"]}.{__name__}')


class UserService:
	def __init__(self, session: AsyncSession):
		self.session = session
		self.user_repo = UserRepository(self.session)
		self.profile_repo = ProfileRepository(self.session)

	async def register_user_with_profile(
		self, username: str, email: str, password_in_chiaro: str, bio: str | None = None
	) -> User:
		"""
		Registra un nuovo utente cifrando la password e creando il profilo in modo atomico.
		"""

		logger.info(f'Registrazione di un nuovo utente: {username} {email} {password_in_chiaro}')

		async with self.session.begin():
			# 1. Controllo di business
			existing_user = await self.user_repo.get_by_email(email)
			if existing_user:
				raise ValueError(f"L'email '{email}' è già associata a un account.")

			existing_user = await self.user_repo.get_by_name(username)
			if existing_user:
				raise ValueError(f"Lo username '{username}'è già in uso.")

			# 2. CIFRATURA DELLA PASSWORD
			# Trasformiamo la stringa in chiaro in un hash non invertibile
			password_hash = CryptoService.hash_password(password_in_chiaro)

			# 3. Creazione dell'utente (passando l'hash, non la password in chiaro!)
			new_user = await self.user_repo.create(username=username, email=email, password_hash=password_hash)

			# 4. Creazione del profilo collegato via .flush() interno
			await self.profile_repo.create_for_user(user_id=new_user.id, bio=bio)

			await self.session.commit()

			return new_user
